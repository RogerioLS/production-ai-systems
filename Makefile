# ==============================================================================
#                 PRODUCTION AI SYSTEMS — MASTER COMMAND CENTER
# ==============================================================================

PYTHON := python3

# ANSI Color Codes & Formatting
RESET   := \033[0m
BOLD    := \033[1m
DIM     := \033[2m
CYAN    := \033[36m
GREEN   := \033[32m
YELLOW  := \033[33m
RED     := \033[31m
MAGENTA := \033[35m
BLUE    := \033[34m
WHITE   := \033[97m

.PHONY: help install onboarding compile check test audit pr sync-tasks docs-serve docs-deploy clean

help:
	@printf "$(CYAN)┌──────────────────────────────────────────────────────────────────────────────┐\n$(RESET)"
	@printf "$(CYAN)│$(RESET) $(BOLD)$(MAGENTA)             PRODUCTION AI SYSTEMS — COMMAND CENTER                            $(RESET) $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)├──────────────────────────────────────────────────────────────────────────────┤\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make help$(RESET)       $(DIM)─$(RESET) Show this interactive help menu                           $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make onboarding$(RESET) $(DIM)─$(RESET) Show best practices & Git governance banner               $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make install$(RESET)    $(DIM)─$(RESET) Install dependencies & configure custom git hooks          $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make compile$(RESET)    $(DIM)─$(RESET) Compile Python syntax across all project files             $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make check$(RESET)      $(DIM)─$(RESET) Run pre-commit linters (Black, Isort, Ruff, Secrets)       $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make test$(RESET)       $(DIM)─$(RESET) Run all unit & integration test suites                      $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make audit$(RESET)      $(DIM)─$(RESET) Full audit: compile + check + test                          $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make pr$(RESET)         $(DIM)─$(RESET) Publish automated GitHub Pull Request with Closes #ID     $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make sync-tasks$(RESET) $(DIM)─$(RESET) Synchronize GitHub issues to local .github/issues/        $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make docs-serve$(RESET) $(DIM)─$(RESET) Launch MkDocs documentation server on port 8009         $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make docs-deploy$(RESET)$(DIM)─$(RESET) Build & deploy MkDocs documentation to gh-pages          $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)│$(RESET)  $(BOLD)$(GREEN)make clean$(RESET)      $(DIM)─$(RESET) Remove temporary cache and build artifacts                 $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)├──────────────────────────────────────────────────────────────────────────────┤\n$(RESET)"
	@printf "$(CYAN)│$(RESET)           $(BOLD)$(WHITE)🔥 Built for Production AI Systems by $(YELLOW)@RogerioLS$(WHITE)$(RESET)                    $(CYAN)│\n$(RESET)"
	@printf "$(CYAN)└──────────────────────────────────────────────────────────────────────────────┘\n$(RESET)"

onboarding:
	@bash scripts/install-hooks.sh --banner-only

install:
	@printf "$(BOLD)$(BLUE)📦 [INSTALL] Installing project dependencies and configuring git hooks...$(RESET)\n"
	@$(PYTHON) -m pip install -e ".[dev,docs]"
	@bash scripts/install-hooks.sh
	@printf "$(GREEN)✔ Dependencies installed and Git hooks configured successfully!$(RESET)\n"

compile:
	@printf "$(BOLD)$(MAGENTA)⚡ [COMPILE] Verifying Python syntax compilation...$(RESET)\n"
	@$(PYTHON) -m py_compile $$(find source projects tests scripts -name "*.py" 2>/dev/null)
	@printf "$(GREEN)✔ Syntax compilation successful!$(RESET)\n"

check:
	@printf "$(BOLD)$(YELLOW)🔍 [CHECK] Running linters and pre-commit checks...$(RESET)\n"
	@black .
	@isort .
	@ruff check . --fix
	@pre-commit run --all-files
	@printf "$(GREEN)✔ All linter checks passed! Ready for git commit.$(RESET)\n\n"

test:
	@printf "$(BOLD)$(BLUE)🚀 [TESTS] Running all unit test suites...$(RESET)\n"
	@PYTHONPATH=. pytest tests/ projects/

audit: compile check test
	@printf "\n$(BOLD)$(GREEN)======================================================================$(RESET)\n"
	@printf "$(BOLD)$(GREEN)   ✅ FULL AUDIT COMPLETE: Code is compliant, formatted & tested!    $(RESET)\n"
	@printf "$(BOLD)$(GREEN)======================================================================$(RESET)\n\n"

pr:
	@printf "$(BOLD)$(CYAN)🚀 [PR] Publishing automated GitHub Pull Request...$(RESET)\n"
	@$(PYTHON) scripts/create_pr.py

sync-tasks:
	@printf "$(BOLD)$(CYAN)🔄 [SYNC] Synchronizing GitHub issues to local task files...$(RESET)\n"
	@$(PYTHON) scripts/sync_tasks.py
	@printf "$(GREEN)✔ Tasks successfully synchronized!$(RESET)\n"

docs-serve:
	@fuser -k 8009/tcp || true
	@mkdocs serve -a 127.0.0.1:8009

docs-deploy:
	@mkdocs gh-deploy --clean

clean:
	@printf "$(BOLD)$(RED)🧹 [CLEAN] Removing temporary cache and build files...$(RESET)\n"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -delete
	@find . -type f -name ".secrets.baseline" -delete
	@printf "$(GREEN)✔ Clean completed successfully.$(RESET)\n\n"
