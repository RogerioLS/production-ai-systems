# ADR 0001: Initial Repository and Codebase Layout

## Status
Accepted

## Date
2026-05-27

## Context
We need to establish a repository layout for the `production-ai-systems` roadmap that accommodates:

- Multiple independent coding projects representing learning modules.
- Centralized configurations for code quality, formatting, and linters.
- A unified documentation system compiled via MkDocs.
- Easy extensibility as the roadmap progresses towards advanced, production-grade applications.

## Decision
We adopt a multi-module monorepo structure with the following layout:

- **`projects/`:** Contains isolated directories for each module (e.g., `projects/a_llm_basics/`, `projects/b_prompt_engineering/`).
- **Module Structure:** Each module contains:
  - `src/` for source code.
  - `tests/` for `pytest` unit/integration tests.
  - `experiments/` for running benchmarks, visualizers, or prototyping notebooks.
  - `TODO.md` and `README.md` for task tracking and module-specific reflections.
- **Centralized Quality Gate:** Shared configurations for coding standards (Black, Isort, Ruff, Pre-Commit hooks) and test automation run via a centralized root `Makefile` and `pyproject.toml`.
- **Package Imports:** Package directories are named using alphabetical prefixes (e.g., `a_llm_basics` instead of `01_llm_basics`) to allow standard Python imports without syntax violations.

## Consequences
- **Positive:** High isolation between different roadmap projects, preventing code pollution while sharing standard root configurations.
- **Positive:** Clean integration with MkDocs, compile-ready by mapping the documentation pages directly in the global config.
- **Negative:** Requires running Python modules explicitly (using `PYTHONPATH=.` or `python -m`) from the root directory to properly resolve import paths.
