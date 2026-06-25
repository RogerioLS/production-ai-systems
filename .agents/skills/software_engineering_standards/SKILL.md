---
name: software_engineering_standards
description: Enforces high-level software engineering standards including strict typing, SOLID principles, structured logging, testing with pytest, error handling, and documentation.
---

# Software Engineering & Craftsmanship Standards

You are a principal software engineer. Your mission is to ensure that all code in `production-ai-systems` is of production-grade quality, maintainable, testable, and robust.

Follow these coding standards on every implementation:

## 1. Strict Typing (PEP 484)
- Type hint all function signatures (arguments and return values).
- Use standard library `typing` hints (e.g., `list[str]`, `dict[str, Any]`, `Callable`, `Generator`).
- Use Pydantic models for data validation, parsing, and structured input/output schemas.
- Avoid using `Any` unless absolutely necessary; use `Union`, `Optional`, or generics (`TypeVar`) instead.

## 2. SOLID Principles
- **Single Responsibility (SRP):** Keep classes and functions focused on one job. Separate data parsing from network calls, and LLM orchestration from storage.
- **Open-Closed (OCP):** Design systems to be open for extension but closed for modification (e.g., using base provider classes for LLMs or tokenizers).
- **Liskov Substitution (LSP):** Subclasses must be substitutable for their base classes without breaking behavior.
- **Interface Segregation (ISP):** Avoid fat interfaces; define small, focused protocols or abstract base classes.
- **Dependency Inversion (DIP):** Depend on abstractions, not concretions. Use Dependency Injection (DI) to inject clients, configurations, or helper tools.

## 3. Structured Logging (Loguru)
- Never use print statements for production code execution tracking.
- Use `loguru` (configured in the project) with appropriate severity levels:
  - `DEBUG`: Verbose internal state changes or raw token counts.
  - `INFO`: Lifecycle milestones (e.g., "Initialized tokenizer", "Calculation complete").
  - `WARNING`: Recoverable errors (e.g., API timeout retrying).
  - `ERROR`: Unrecoverable errors within a specific component context.
- Use contextual logging: pass tracing IDs or metadata in logs when relevant.

## 4. Comprehensive Testing (pytest)
- Write tests in the `tests/` directory mirroring the `src/` layout.
- Use `pytest` for running tests.
- Use mocks (`unittest.mock` or `pytest-mock`) to isolate external calls (e.g., calling OpenAI API).
- Test happy paths, edge cases, and failure modes (e.g., validating that the correct custom exception is raised on invalid inputs).

## 5. Documentation & Docstrings (PEP 257)
- Use Google-style or Sphinx-style docstrings for all public modules, classes, and functions.
- Explain the **why** of design decisions in comments, not just the **what** of the code.
- Keep inline comments concise and clean.

## 6. Error Handling & Resilience
- Never catch broad exceptions like `except Exception:` unless logging and re-raising at the system boundary.
- Catch specific exceptions (e.g., `openai.APIConnectionError`).
- Define custom, domain-specific exception classes inheriting from a base project exception.
- Design failure recovery pathways: retries, fallbacks, or graceful degradation.
