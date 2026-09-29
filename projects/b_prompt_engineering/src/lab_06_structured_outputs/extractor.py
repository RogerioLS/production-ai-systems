"""Industrial structured output extractor with self-healing reflection loops."""

import time
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

from loguru import logger
from pydantic import BaseModel, ValidationError

from projects.b_prompt_engineering.src.lab_06_structured_outputs.exceptions import (
    SelfHealingExhaustedError,
    StructuredOutputError,
    SyntaxParseError,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.parsers import (
    RobustJSONParser,
    XMLTagParser,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.prompt_builders import (
    SchemaPromptBuilder,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.schemas import (
    ExtractionResult,
    ExtractionStrategy,
)

T = TypeVar("T", bound=BaseModel)
LLMCallable = Callable[[List[Dict[str, str]]], str]


class StructuredOutputExtractor(Generic[T]):
    """Orchestrates structured data extraction with multi-strategy support and

    Self-Healing reflection loops for automatic error recovery.
    """

    def __init__(
        self,
        target_model: Type[T],
        strategy: ExtractionStrategy = ExtractionStrategy.JSON_SCHEMA_STRICT,
        max_retries: int = 3,
        llm_callable: Optional[LLMCallable] = None,
    ) -> None:
        self.target_model = target_model
        self.strategy = strategy
        self.max_retries = max(1, max_retries)
        self.llm_callable = llm_callable
        self.prompt_builder = SchemaPromptBuilder()

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Invokes the registered LLM callable or raises an error if unconfigured."""
        if self.llm_callable is None:
            raise StructuredOutputError(
                "No LLM callable provided. Inject an LLM client or callable function."
            )
        return self.llm_callable(messages)

    def extract(
        self,
        text: str,
        context: Optional[str] = None,
        raise_on_failure: bool = False,
    ) -> ExtractionResult[T]:
        """Executes structured data extraction with automated Self-Healing reflection loops."""
        start_time = time.perf_counter()
        raw_outputs: List[str] = []
        validation_errors: List[str] = []

        system_prompt = self.prompt_builder.build_system_prompt(self.target_model, self.strategy)
        user_prompt = self.prompt_builder.build_user_prompt(text, context)
        current_messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(
            f"Starting extraction for model {self.target_model.__name__} "
            f"using strategy '{self.strategy.value}' (max_retries={self.max_retries})"
        )

        for attempt in range(1, self.max_retries + 1):
            logger.debug(f"Executing extraction attempt {attempt}/{self.max_retries}...")

            try:
                raw_output = self._call_llm(current_messages)
                raw_outputs.append(raw_output)

                # Step 1: Syntactic parsing
                if self.strategy == ExtractionStrategy.XML_TAGS:
                    parsed_dict = XMLTagParser.parse(
                        raw_output, root_tag=self.target_model.__name__.lower()
                    )
                else:
                    parsed_dict = RobustJSONParser.parse(raw_output)

                # Step 2: Pydantic runtime schema validation
                validated_instance = self.target_model.model_validate(parsed_dict)
                elapsed = time.perf_counter() - start_time

                logger.info(
                    f"Extraction succeeded on attempt {attempt}/{self.max_retries} "
                    f"in {elapsed:.3f}s."
                )

                return ExtractionResult(
                    data=validated_instance,
                    strategy=self.strategy,
                    attempts=attempt,
                    is_success=True,
                    raw_outputs=raw_outputs,
                    validation_errors=validation_errors,
                    execution_time_seconds=elapsed,
                )

            except (SyntaxParseError, ValidationError) as exc:
                err_msg = f"Attempt {attempt} failed: {exc}"
                logger.warning(err_msg)
                validation_errors.append(err_msg)

                # Prepare self-healing reflection messages for the next retry iteration
                if attempt < self.max_retries:
                    logger.info(
                        f"Initiating Self-Healing reflection loop (attempt {attempt + 1})..."
                    )
                    current_messages = self.prompt_builder.build_repair_messages(
                        original_prompt=user_prompt,
                        failed_raw_output=raw_outputs[-1] if raw_outputs else "",
                        error_details=str(exc),
                        attempt=attempt,
                        model_cls=self.target_model,
                    )

        # Reflection attempts exhausted
        elapsed = time.perf_counter() - start_time
        logger.error(
            f"Structured extraction failed after {self.max_retries} attempts "
            f"for {self.target_model.__name__}."
        )

        if raise_on_failure:
            raise SelfHealingExhaustedError(
                message=f"Failed to extract valid {self.target_model.__name__} after "
                f"{self.max_retries} attempts.",
                attempts=self.max_retries,
                history=validation_errors,
                raw_output=raw_outputs[-1] if raw_outputs else None,
            )

        return ExtractionResult(
            data=None,
            strategy=self.strategy,
            attempts=self.max_retries,
            is_success=False,
            raw_outputs=raw_outputs,
            validation_errors=validation_errors,
            execution_time_seconds=elapsed,
        )

    def extract_with_instructor(
        self,
        client: Any,
        text: str,
        model_name: str = "gpt-4o-mini",
        context: Optional[str] = None,
        **kwargs: Any,
    ) -> ExtractionResult[T]:
        """Integrates Instructor for native Tool/Function Calling extraction."""
        start_time = time.perf_counter()
        raw_outputs: List[str] = []

        try:
            import instructor

            # Ensure client is patched with instructor
            patched_client = (
                instructor.from_openai(client)
                if not hasattr(client, "chat") or not hasattr(client.chat.completions, "create")
                else client
            )

            prompt = self.prompt_builder.build_user_prompt(text, context)
            response: T = patched_client.chat.completions.create(
                model=model_name,
                response_model=self.target_model,
                messages=[
                    {
                        "role": "system",
                        "content": ("Extract information strictly adhering to the schema."),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_retries=self.max_retries,
                **kwargs,
            )

            elapsed = time.perf_counter() - start_time
            return ExtractionResult(
                data=response,
                strategy=ExtractionStrategy.INSTRUCTOR,
                attempts=1,
                is_success=True,
                raw_outputs=[str(response)],
                validation_errors=[],
                execution_time_seconds=elapsed,
            )

        except Exception as exc:
            elapsed = time.perf_counter() - start_time
            err_msg = f"Instructor extraction failed: {exc}"
            logger.error(err_msg)
            return ExtractionResult(
                data=None,
                strategy=ExtractionStrategy.INSTRUCTOR,
                attempts=1,
                is_success=False,
                raw_outputs=raw_outputs,
                validation_errors=[err_msg],
                execution_time_seconds=elapsed,
            )
