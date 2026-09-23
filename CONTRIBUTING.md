# Contributing Guidelines — Production AI Systems

Welcome to the **Production AI Systems** project! We follow rigorous software engineering, production reliability, and clean code standards.

---

## 🛠️ Centralized Workflow with Makefile

We use an interactive **Makefile Command Center** to standardize all development, linting, testing, and execution tasks. Always prefer using `make` commands rather than invoking raw shell commands:

| Command | Purpose | When to Use |
| :--- | :--- | :--- |
| `make help` | Displays the interactive command menu with descriptions | Anytime you need a quick command refresher |
| `make onboarding` | Shows the best practices and Git governance banner | First-time setup or onboarding new developers |
| `make install` | Installs project dependencies and configures Git hooks | First-time project setup |
| `make compile` | Verifies Python syntax compilation across all files | Fast syntax validation |
| `make check` | Runs full pre-commit linters (Black, Isort, Ruff, Secrets) | **Before staging files or creating commits** |
| `make test` | Executes all unit and integration test suites | After any code modification |
| `make audit` | Runs the full verification suite (`compile` + `check` + `test`) | Before pushing or opening a Pull Request |
| `make pr` | Publishes an automated GitHub Pull Request with issue links | When ready to submit branch for review |
| `make sync-tasks` | Synchronizes GitHub issues into local `.github/issues/` | To refresh local task templates |
| `make docs-serve` | Launches local MkDocs server on port 8009 | While authoring documentation or playgrounds |
| `make docs-deploy` | Builds and deploys documentation to GitHub Pages | To publish updated documentation |
| `make clean` | Removes temporary cache files (`__pycache__`, `.pytest_cache`, etc.) | Workspace hygiene |

---

## 🏷️ Branch, Commit & Task Naming Governance

To ensure full traceability between the **GitHub Kanban**, **Pull Requests**, and **Git History**, all branches and commit messages follow strict conventions.

### 🌿 1. Branch Naming Format:
```text
<type>/<task-id>-<short-description-in-kebab-case>
```
- **Valid Examples**:
  - `feat/lab-01-tokenization-math`
  - `feat/lab-02-embeddings`
  - `feat/lab-03-attention`
  - `feat/lab-04-inference-math`
  - `chore/repo-governance-and-architecture`

---

### 📝 2. Commit Message Format:
```text
<type>(<scope>): [<TASK-ID>:#<ISSUE_NUM>] <short description in lowercase>
```
- **Valid Task Examples**:
  - `feat(foundations): [LAB-01:#2] benchmark tokenization compression`
  - `feat(foundations): [LAB-03:#4] implement scaled dot product attention`
  - `docs(notes): [LAB-04:#5] document inference math and kv cache vram`
- **Valid Non-Task / Infrastructure Examples**:
  - `chore(infra): [INFRA] configure pre-commit hooks and command center`
  - `docs(meta): [DOCS] update contributing guidelines and security policy`
  - `fix(env): [HOTFIX] resolve conda python compatibility`

### 📋 Allowed Reserved Tags (for non-task changes):
`[INFRA]`, `[CHORE]`, `[DOCS]`, `[FIX]`, `[HOTFIX]`, `[SECURITY]`, `[GLOBAL]`, `[CONFIG]`, `[DEPS]`, `[ENV]`, `[RELEASE]`

*Note: Gitmojis (`✨`, `📝`, `🔧`, etc.) are automatically prepended by `.githooks/prepare-commit-msg`.*

---

## 🧪 Testing & Code Quality Expectations

1. **Strict Typing:** All function signatures must include PEP 484 type hints.
2. **SOLID Architecture:** Modular separation between computation, data schemas, and API clients.
3. **Structured Logging:** Use `loguru` exclusively. No raw `print` statements in production libraries.
4. **Resilience:** Explicit error handling with custom domain exceptions.
5. **No Secrets:** `detect-secrets` runs on every pre-commit to safeguard API keys and environment variables.
