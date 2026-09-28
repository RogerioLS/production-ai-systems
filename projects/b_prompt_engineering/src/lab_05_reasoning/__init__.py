"""Public API exports for LAB-05: Prompt Reasoning Patterns."""

from projects.b_prompt_engineering.src.lab_05_reasoning.chain_of_thought import (
    ChainOfThoughtPromptEngine,
    SelfConsistencyEngine,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import (
    ExemplarSelectionError,
    ReActExecutionError,
    ReasoningError,
    SelfConsistencyError,
    TemplateError,
    ToolNotFoundError,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.few_shot import FewShotPromptEngine
from projects.b_prompt_engineering.src.lab_05_reasoning.react import ReActEngine
from projects.b_prompt_engineering.src.lab_05_reasoning.templates import (
    ChatPromptTemplate,
    PromptTemplate,
)
from projects.b_prompt_engineering.src.lab_05_reasoning.types import (
    ChatMessage,
    ConsensusResult,
    Exemplar,
    PromptRole,
    ReActResult,
    ReActStep,
    ToolDefinition,
)

__all__ = [
    # Exceptions
    "ReasoningError",
    "TemplateError",
    "ExemplarSelectionError",
    "SelfConsistencyError",
    "ReActExecutionError",
    "ToolNotFoundError",
    # Data Models
    "PromptRole",
    "ChatMessage",
    "Exemplar",
    "ToolDefinition",
    "ReActStep",
    "ReActResult",
    "ConsensusResult",
    # Engines & Templates
    "PromptTemplate",
    "ChatPromptTemplate",
    "FewShotPromptEngine",
    "ChainOfThoughtPromptEngine",
    "SelfConsistencyEngine",
    "ReActEngine",
]
