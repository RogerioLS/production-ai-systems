"""Prompt Template system with static verification, typing, and safe formatting."""

import re
from typing import Any, List, Set

from loguru import logger

from projects.b_prompt_engineering.src.lab_05_reasoning.exceptions import TemplateError
from projects.b_prompt_engineering.src.lab_05_reasoning.types import ChatMessage, PromptRole


class PromptTemplate:
    """Production-grade string template with variable schema validation.

    Ensures that prompts cannot be formatted with missing parameters, protecting
    production pipelines from raw '{variable}' leakages into model API payloads.
    """

    def __init__(self, template: str, role: PromptRole = PromptRole.USER) -> None:
        if not template or not template.strip():
            raise TemplateError("Prompt template string cannot be empty.")
        self.raw_template: str = template
        self.role: PromptRole = role
        self.variables: Set[str] = self._extract_variables(template)
        logger.debug(
            f"Initialized PromptTemplate (Role: {self.role.value}) with "
            f"variables: {sorted(self.variables)}"
        )

    @staticmethod
    def _extract_variables(text: str) -> Set[str]:
        """Extracts all '{var_name}' placeholders using regular expressions."""
        matches = re.findall(r"\{([a-zA-Z0-9_]+)\}", text)
        return set(matches)

    def format(self, **kwargs: Any) -> str:
        """Formats the template string after verifying all required variables exist."""
        provided = set(kwargs.keys())
        missing = self.variables - provided
        if missing:
            raise TemplateError(
                f"Missing required template variables: {sorted(missing)}. "
                f"Required: {sorted(self.variables)}, Provided: {sorted(provided)}"
            )

        try:
            formatted = self.raw_template.format(**kwargs)
            return formatted
        except Exception as err:
            raise TemplateError(f"Error during prompt template substitution: {err}") from err

    def format_message(self, **kwargs: Any) -> ChatMessage:
        """Formats template directly into a structured ChatMessage turn."""
        content = self.format(**kwargs)
        return ChatMessage(role=self.role, content=content)


class ChatPromptTemplate:
    """Multi-turn conversational prompt template combining System, User, and Assistant turns."""

    def __init__(self, messages: List[PromptTemplate]) -> None:
        if not messages:
            raise TemplateError("ChatPromptTemplate requires at least one PromptTemplate turn.")
        self.messages: List[PromptTemplate] = messages
        self.variables: Set[str] = set()
        for msg in self.messages:
            self.variables.update(msg.variables)

    def format_messages(self, **kwargs: Any) -> List[ChatMessage]:
        """Formats all conversation turns against provided variable values."""
        provided = set(kwargs.keys())
        missing = self.variables - provided
        if missing:
            raise TemplateError(
                f"Missing required chat variables: {sorted(missing)}. "
                f"Required: {sorted(self.variables)}, Provided: {sorted(provided)}"
            )

        return [msg.format_message(**kwargs) for msg in self.messages]

    def to_single_prompt(self, **kwargs: Any) -> str:
        """Flattens chat turns into a single unified text prompt."""
        formatted_turns = self.format_messages(**kwargs)
        lines = []
        for turn in formatted_turns:
            lines.append(f"[{turn.role.value.upper()}]\n{turn.content}")
        return "\n\n".join(lines)
