"""Domain exceptions for LAB-05 Prompt Reasoning Patterns."""


class ReasoningError(Exception):
    """Base exception for all prompt reasoning failures."""


class TemplateError(ReasoningError):
    """Raised when prompt template validation, variable substitution, or syntax fails."""


class ExemplarSelectionError(ReasoningError):
    """Raised when in-context exemplar retrieval or formatting fails."""


class SelfConsistencyError(ReasoningError):
    """Raised when majority voting consensus fails or sample counts are invalid."""


class ReActExecutionError(ReasoningError):
    """Raised when ReAct autonomous thought-action loop exceeds steps or fails tool invocation."""


class ToolNotFoundError(ReActExecutionError):
    """Raised when an autonomous agent attempts to call an unregistered tool."""
