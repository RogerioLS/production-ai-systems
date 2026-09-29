"""Comparative benchmarking suite for evaluating structured output extraction strategies."""

from typing import Callable, Dict, List, Type

from loguru import logger
from pydantic import BaseModel

from projects.b_prompt_engineering.src.lab_06_structured_outputs.extractor import (
    StructuredOutputExtractor,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.schemas import (
    BenchmarkReport,
    ExtractionStrategy,
)


class StrategyBenchmark:
    """Empirical evaluator comparing extraction reliability, recovery rates,

    and failure modes across prompt-based and structured extraction strategies.
    """

    def __init__(self, target_model: Type[BaseModel]) -> None:
        self.target_model = target_model

    def evaluate_strategy(
        self,
        strategy: ExtractionStrategy,
        test_cases: List[str],
        llm_callable_factory: Callable[[str], Callable[[List[Dict[str, str]]], str]],
        max_retries: int = 3,
    ) -> BenchmarkReport:
        """Evaluates a single strategy across a suite of test cases."""
        total_runs = len(test_cases)
        successful_runs = 0
        total_attempts = 0
        total_latency = 0.0
        syntax_errors = 0
        schema_errors = 0

        logger.info(f"Running benchmark for strategy '{strategy.value}' with {total_runs} cases...")

        for test_text in test_cases:
            callable_fn = llm_callable_factory(test_text)
            extractor = StructuredOutputExtractor(
                target_model=self.target_model,
                strategy=strategy,
                max_retries=max_retries,
                llm_callable=callable_fn,
            )

            res = extractor.extract(test_text)
            total_attempts += res.attempts
            total_latency += res.execution_time_seconds

            if res.is_success:
                successful_runs += 1
            else:
                for err in res.validation_errors:
                    if (
                        "SyntaxParseError" in err
                        or "JSONDecodeError" in err
                        or "Failed to parse" in err
                    ):
                        syntax_errors += 1
                    else:
                        schema_errors += 1

        success_rate = (successful_runs / total_runs * 100.0) if total_runs > 0 else 0.0
        avg_attempts = (total_attempts / total_runs) if total_runs > 0 else 0.0
        avg_latency = (total_latency / total_runs) if total_runs > 0 else 0.0

        return BenchmarkReport(
            strategy=strategy,
            total_runs=total_runs,
            successful_runs=successful_runs,
            success_rate_pct=round(success_rate, 2),
            avg_attempts=round(avg_attempts, 2),
            avg_latency_seconds=round(avg_latency, 4),
            syntax_errors=syntax_errors,
            schema_errors=schema_errors,
        )

    @staticmethod
    def generate_markdown_table(reports: List[BenchmarkReport]) -> str:
        """Formats a comparative markdown table summarizing benchmark outcomes."""
        header = (
            "| Estratégia de Extração | Taxa de Sucesso (%) | Méd. Tentativas | "
            "Erros Sintáticos | Erros de Schema | Latência Média (s) |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: |\n"
        )
        rows: List[str] = []
        for r in reports:
            rows.append(
                f"| **{r.strategy.value}** | {r.success_rate_pct}% | {r.avg_attempts} | "
                f"{r.syntax_errors} | {r.schema_errors} | {r.avg_latency_seconds}s |"
            )
        return header + "\n".join(rows)
