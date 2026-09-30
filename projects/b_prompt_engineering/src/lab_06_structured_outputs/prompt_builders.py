"""Prompt generation utilities for schema enforcement, XML tags, and Self-Healing error repair."""

import json
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from projects.b_prompt_engineering.src.lab_06_structured_outputs.schemas import ExtractionStrategy


class SchemaPromptBuilder:
    """Constructs extraction and reflection prompts conditioned on target Pydantic schemas."""

    @staticmethod
    def build_system_prompt(
        model_cls: Type[BaseModel],
        strategy: ExtractionStrategy = ExtractionStrategy.JSON_SCHEMA_STRICT,
    ) -> str:
        """Generates appropriate system instructions based on the extraction strategy."""
        schema_dict = model_cls.model_json_schema()
        schema_json = json.dumps(schema_dict, indent=2)

        if strategy == ExtractionStrategy.JSON_SCHEMA_STRICT:
            return (
                "You are an expert enterprise data extraction engine.\n"
                "Your objective is to extract structured information strictly conforming to the "
                "following JSON Schema.\n\n"
                f"### TARGET JSON SCHEMA:\n{schema_json}\n\n"
                "CRITICAL INSTRUCTIONS:\n"
                "1. Return ONLY a single valid JSON object adhering strictly to the schema above.\n"
                "2. Do NOT add conversational pleasantries, notes, or markdown formatting.\n"
                "3. Ensure all required fields are present and properly typed.\n"
                "4. All dates must match ISO 8601 (YYYY-MM-DD).\n"
                "5. Numerical values must be clean floating point numbers or integers."
            )

        if strategy == ExtractionStrategy.XML_TAGS:
            root_name = model_cls.__name__.lower()
            return (
                "You are an expert enterprise data extraction engine.\n"
                "Your objective is to extract structured data formatted within strict XML tags.\n"
                f"Wrap the entire extraction in a root `<{root_name}>...</{root_name}>` tag.\n"
                "Each field from the target schema must be enclosed in its respective tag.\n"
                "For nested lists, use `<item>` tags within the parent tag.\n\n"
                f"### TARGET SCHEMA REFERENCE:\n{schema_json}\n\n"
                "CRITICAL INSTRUCTIONS:\n"
                "1. Return ONLY valid, well-formed XML matching the schema.\n"
                "2. No preamble or postamble outside the XML tags.\n"
                "3. All dates must be ISO YYYY-MM-DD format."
            )

        # RAW_JSON strategy
        return (
            "You are a helpful data extraction assistant.\n"
            "Extract the relevant fields from the provided document into a clean JSON object.\n"
            f"Expected fields: {list(schema_dict.get('properties', {}).keys())}."
        )

    @staticmethod
    def build_user_prompt(text: str, context: Optional[str] = None) -> str:
        """Formats the input document and optional contextual directives."""
        parts: List[str] = []
        if context:
            parts.append(f"### CONTEXTUAL METADATA:\n{context}\n")
        parts.append(f"### SOURCE DOCUMENT TO EXTRACT:\n{text}")
        return "\n".join(parts)

    @staticmethod
    def build_repair_messages(
        original_prompt: str,
        failed_raw_output: str,
        error_details: str,
        attempt: int,
        model_cls: Type[BaseModel],
    ) -> List[Dict[str, str]]:
        """Constructs Self-Healing reflection dialogue re-injecting the validation traceback."""
        schema_json = json.dumps(model_cls.model_json_schema(), indent=2)
        system_msg = (
            "You are an automated self-healing error recovery system for data extraction.\n"
            "Your previous extraction attempt failed schema validation or syntax parsing.\n"
            "Analyze the validation errors carefully, inspect the previous invalid output, and "
            "generate a corrected, valid JSON response that satisfies every schema constraint."
        )

        user_msg = (
            f"### ORIGINAL EXTRACTION TASK:\n{original_prompt}\n\n"
            f"### ATTEMPT #{attempt} FAILED OUTPUT:\n{failed_raw_output}\n\n"
            f"### VALIDATION / SYNTAX ERROR DETAILS:\n{error_details}\n\n"
            f"### TARGET JSON SCHEMA:\n{schema_json}\n\n"
            "Please fix all reported errors and provide the complete, corrected JSON object."
        )

        return [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]
