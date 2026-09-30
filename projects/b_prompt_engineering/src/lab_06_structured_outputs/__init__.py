"""LAB-06: Structured Outputs, Schema Enforcement & Self-Healing Reflection Loops."""

from projects.b_prompt_engineering.src.lab_06_structured_outputs.benchmarking import (
    StrategyBenchmark,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.exceptions import (
    SchemaValidationError,
    SelfHealingExhaustedError,
    StructuredOutputError,
    SyntaxParseError,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.extractor import (
    StructuredOutputExtractor,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.parsers import (
    RobustJSONParser,
    XMLTagParser,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.prompt_builders import (
    SchemaPromptBuilder,
)
from projects.b_prompt_engineering.src.lab_06_structured_outputs.schemas import (
    BenchmarkReport,
    ContractObligation,
    ContractParty,
    CurrencyCode,
    ExtractionAttempt,
    ExtractionResult,
    ExtractionStrategy,
    FinancialContract,
    PartyType,
)

__all__ = [
    "StructuredOutputError",
    "SyntaxParseError",
    "SchemaValidationError",
    "SelfHealingExhaustedError",
    "PartyType",
    "CurrencyCode",
    "ExtractionStrategy",
    "ContractParty",
    "ContractObligation",
    "FinancialContract",
    "ExtractionAttempt",
    "ExtractionResult",
    "BenchmarkReport",
    "RobustJSONParser",
    "XMLTagParser",
    "SchemaPromptBuilder",
    "StructuredOutputExtractor",
    "StrategyBenchmark",
]
