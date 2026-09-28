"""In-Context Learning (Few-Shot) engine with static and dynamic exemplar selectors."""

from typing import Callable, List, Optional

from loguru import logger

from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import ExemplarSelectionError
from projects.b_prompt_engineering.src.lab_05_reasoning.types import Exemplar


class FewShotPromptEngine:
    """Orchestrates In-Context Learning (ICL) exemplar formatting and selection.

    Supports:
    - Structured exemplar formatting with optional Chain-of-Thought reasoning steps.
    - Deterministic prefix/suffix assembly.
    - Dynamic exemplar selector callbacks (e.g. semantic similarity, keyword match).
    """

    def __init__(
        self,
        prefix: str = "Here are a few examples to follow:",
        suffix: str = "Now solve the following problem:\nInput: {query}\nOutput:",
        exemplar_separator: str = "\n\n",
        include_reasoning: bool = True,
    ) -> None:
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.exemplar_separator: str = exemplar_separator
        self.include_reasoning: bool = include_reasoning
        self._exemplar_pool: List[Exemplar] = []

    def register_exemplar(self, exemplar: Exemplar) -> None:
        """Adds a single demonstration exemplar to the internal pool."""
        self._exemplar_pool.append(exemplar)

    def register_exemplars(self, exemplars: List[Exemplar]) -> None:
        """Bulk registers demonstration exemplars."""
        self._exemplar_pool.extend(exemplars)

    def format_single_exemplar(self, exemplar: Exemplar) -> str:
        """Formats an exemplar into a standardized text block."""
        parts = [f"Input: {exemplar.input_text}"]
        if self.include_reasoning and exemplar.reasoning:
            parts.append(f"Reasoning: {exemplar.reasoning}")
        parts.append(f"Output: {exemplar.output_text}")
        return "\n".join(parts)

    def build_prompt(
        self,
        query: str,
        k: Optional[int] = None,
        selector: Optional[Callable[[str, List[Exemplar], int], List[Exemplar]]] = None,
    ) -> str:
        """Builds a full few-shot prompt with selected exemplars.

        Args:
            query: The user input or question to solve.
            k: Maximum number of exemplars to include (defaults to all if None).
            selector: Optional callable taking (query, pool, k) returning selected Exemplars.
        """
        if not query or not query.strip():
            raise ExemplarSelectionError("Query for few-shot prompt cannot be empty.")

        pool = list(self._exemplar_pool)
        if not pool:
            logger.warning(
                "No exemplars registered in FewShotPromptEngine. Falling back to zero-shot."
            )
            selected: List[Exemplar] = []
        else:
            limit = k if k is not None and k > 0 else len(pool)
            if selector:
                try:
                    selected = selector(query, pool, limit)
                except Exception as err:
                    raise ExemplarSelectionError(f"Custom exemplar selector failed: {err}") from err
            else:
                selected = pool[:limit]

        exemplar_blocks = [self.format_single_exemplar(ex) for ex in selected]
        formatted_examples = self.exemplar_separator.join(exemplar_blocks)

        sections: List[str] = []
        if self.prefix:
            sections.append(self.prefix)
        if formatted_examples:
            sections.append(formatted_examples)
        sections.append(self.suffix.format(query=query))

        final_prompt = "\n\n".join(sections)
        logger.debug(f"Constructed few-shot prompt with {len(selected)} exemplars.")
        return final_prompt
