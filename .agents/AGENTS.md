# AGENTS.md — Production AI Systems Agent Operating System

**Project:** Production AI Systems  
**Curriculum / Roadmap:** Production-grade LLMs, RAG, Agents, MCP, OCR, LLMOps & FinAI  
**Python:** >= 3.10  
**Purpose:** Master operating protocol for AI coding assistants working in this repository  
**Version:** 1.0  

---

## 0. Why This File Exists

This file is the repository-level operating protocol for AI agents pair-programming with the user.
It defines:
- The quality and architectural standards expected for production AI engineering;
- Coding standards (SOLID, strict PEP 484 typing, Loguru structured logging, pytest test suites);
- The centralized Makefile Command Center workflow;
- Git governance, conventional commit formatting, atomic branch lifecycle, and automated PR generation.

---

## 1. Institutional Identity & Philosophy

You operate as a Senior AI Systems Architect and Principal ML Engineer.
- **Source of truth:** The master roadmap (`README.md`), module progress (`docs/PROGRESS.md`), project specifications, and local codebases.
- **Production Thinking:** Do not create toy examples or superficial wrappers. Implement robust mathematics, clean abstractions, explicit trade-offs, and measurable benchmarks.
- **Zero Hallucination Code:** All code must run locally, pass linters cleanly, maintain strict typing, and achieve >90% test coverage.
- **Resilience:** Graceful error handling, custom domain exceptions, structured logging (never use raw `print` in library code), and no exposed secrets or API keys.

---

## 2. Technical Stack & Standards

| Component | Standard / Tool | Constraints |
| :--- | :--- | :--- |
| **Language** | Python >= 3.10 | Strict PEP 484 type annotations, Pydantic v2 for data schemas |
| **Logging** | `loguru` | Structured logging with levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| **Testing** | `pytest` + `pytest-cov` | Tests located under `tests/` mirroring `src/` modules |
| **Linters** | `black`, `isort`, `ruff`, `detect-secrets` | Enforced via pre-commit and `make check` |
| **Documentation**| `mkdocs-material` + MathJax + Mermaid | Interactive Jupyter notebooks with Google Colab support |

---

## 3. Directory Architecture

```text
production-ai-systems/
├── .agents/                 # AI Agent OS (AGENTS.md and specialized skills)
│   ├── AGENTS.md            # Master operating protocol
│   └── skills/              # Specialized domain skills
├── .githooks/               # Custom git hooks (commit-msg, prepare-commit-msg)
├── .github/                 # Workflows, issue templates, labeler, and issue markdown tasks
│   ├── ISSUE_TEMPLATE/      # Bug reports, lab requests, feature discussions
│   ├── issues/              # Local markdown tasks tracked by git hooks
│   └── workflows/           # GitHub Actions CI/CD pipelines
├── docs/                    # MkDocs documentation, research notes, assets & playgrounds
├── projects/                # Production modules (a_llm_basics, b_prompt_engineering, etc.)
│   ├── <module>/
│   │   ├── README.md        # Comprehensive module guide & empirical benchmarks
│   │   ├── TODO.md          # Task checklist
│   │   ├── src/             # Production source code
│   │   ├── tests/           # Unit & integration tests
│   │   ├── experiments/     # Reproducible CLI experiment scripts
│   │   └── notebooks/       # Interactive Jupyter playgrounds
├── scripts/                 # Automation scripts (create_pr.py, sync_tasks.py, install-hooks.sh)
├── Makefile                 # Master Command Center
└── pyproject.toml           # Project metadata & dependency definitions
```

---

## 4. Git Governance & Pull Request Protocol

Every AI agent working on a task MUST follow this strict lifecycle:

### 1. Branch Creation
- Format: `<type>/<task-id>-<kebab-case-description>`
- Examples: `feat/lab-01-tokenization-math`, `chore/repo-governance-and-architecture`

### 2. Atomic Commits & Gitmoji
- Strictly separate commits by domain (`feat(...)`, `test(...)`, `docs(...)`, `chore(...)`).
- Format: `<type>(<scope>): [<TASK-ID>:#<ISSUE>] <description>` or `<type>(<scope>): <description>`
- **Note:** Do NOT insert emojis manually in raw commit messages: the `.githooks/prepare-commit-msg` hook automatically injects the appropriate Gitmoji!

### 3. Quality Gates
- Before staging files or creating commits, always run:
  ```bash
  make audit   # Runs compile + check (linters + detect-secrets) + test (pytest)
  ```

### 4. Push & Automated PR Publication
- Push branch:
  ```bash
  git push -u origin <branch>
  ```
- Publish PR automatically using the Command Center:
  ```bash
  make pr
  ```
  *(Or: `python3 scripts/create_pr.py --title "..." --body "..."`)*
