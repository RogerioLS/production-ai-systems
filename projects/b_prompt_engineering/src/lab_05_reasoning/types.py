"""Domain models and data structures for LAB-05 Prompt Reasoning Patterns."""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PromptRole(str, Enum):
    """Canonical chat completion message roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ChatMessage(BaseModel):
    """Structured representation of a single chat turn."""

    role: PromptRole
    content: str
    name: Optional[str] = None


class Exemplar(BaseModel):
    """In-context learning demonstration pair (Input -> Output) with optional explanation."""

    input_text: str = Field(..., description="Query or problem presented in exemplar")
    output_text: str = Field(..., description="Target answer or ground truth")
    reasoning: Optional[str] = Field(
        default=None, description="Intermediate Chain-of-Thought reasoning steps"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata tags (domain, difficulty)"
    )


class ToolDefinition(BaseModel):
    """Specification of an executable tool for autonomous ReAct cycles."""

    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Documentation describing tool usage and arguments")
    parameters_schema: Dict[str, Any] = Field(
        default_factory=dict, description="JSON Schema for required arguments"
    )
    handler: Optional[Callable[..., Any]] = Field(
        default=None, description="Python callable executed when tool is invoked"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ReActStep(BaseModel):
    """Single step in an autonomous ReAct loop."""

    step_number: int
    thought: str = Field(..., description="Internal deduction and rationale")
    action_tool: Optional[str] = Field(default=None, description="Tool called in this step")
    action_input: Optional[Dict[str, Any]] = Field(
        default=None, description="Arguments passed to tool"
    )
    observation: Optional[str] = Field(
        default=None, description="Environment feedback returned by tool"
    )


class ReActResult(BaseModel):
    """Final outcome of an autonomous ReAct task execution."""

    task: str
    final_answer: str
    steps: List[ReActStep] = Field(default_factory=list)
    total_steps: int
    success: bool
    execution_time_seconds: float = 0.0


class ConsensusResult(BaseModel):
    """Result of Self-Consistency stochastic sampling & majority voting."""

    candidate_answers: List[str]
    winning_answer: str
    confidence_score: float = Field(
        ..., description="Frequency of winning answer over total valid samples (0.0 to 1.0)"
    )
    vote_distribution: Dict[str, int]
    shannon_entropy: float = Field(
        ..., description="Information entropy metric of the answer distribution"
    )
