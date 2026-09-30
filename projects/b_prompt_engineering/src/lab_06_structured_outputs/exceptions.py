"""Domain exceptions for structured output extraction and validation."""

from typing import List, Optional


class StructuredOutputError(Exception):
    """Base exception for all structured output processing errors."""

    def __init__(self, message: str, raw_output: Optional[str] = None) -> None:
        super().__init__(message)
        self.raw_output = raw_output


class SyntaxParseError(StructuredOutputError):
    """Raised when the raw model output cannot be parsed into valid JSON or XML."""

    def __init__(
        self,
        message: str,
        raw_output: Optional[str] = None,
        parser_type: str = "json",
    ) -> None:
        super().__init__(message, raw_output=raw_output)
        self.parser_type = parser_type


class SchemaValidationError(StructuredOutputError):
    """Raised when parsed data fails Pydantic schema validation."""

    def __init__(
        self,
        message: str,
        errors: List[str],
        raw_output: Optional[str] = None,
    ) -> None:
        super().__init__(message, raw_output=raw_output)
        self.errors = errors


class SelfHealingExhaustedError(StructuredOutputError):
    """Raised when self-healing reflection loop reaches max retries without success."""

    def __init__(
        self,
        message: str,
        attempts: int,
        history: List[str],
        raw_output: Optional[str] = None,
    ) -> None:
        super().__init__(message, raw_output=raw_output)
        self.attempts = attempts
        self.history = history
