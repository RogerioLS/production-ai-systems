#!/usr/bin/env bash
# ==============================================================================
#           PRODUCTION AI SYSTEMS - GIT HOOKS INSTALLER & ONBOARDING
# ==============================================================================

set -e

# ANSI Color Codes & Formatting
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
CYAN="\033[36m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
MAGENTA="\033[35m"
BLUE="\033[34m"
WHITE="\033[97m"

if [ "$1" != "--banner-only" ]; then
    GIT_DIR=$(git rev-parse --git-dir 2>/dev/null || true)

    if [ -z "$GIT_DIR" ]; then
        echo -e "${RED}❌ Error: Not a git repository.${RESET}"
        exit 1
    fi

    echo -e "${BOLD}${BLUE}🔧 Configuring custom git hooks path...${RESET}"
    git config core.hooksPath .githooks
    chmod +x .githooks/* 2>/dev/null || true

    echo -e "${GREEN}✅ Git hooks successfully configured to '.githooks'.${RESET}"
fi

echo ""
printf "${CYAN}┌──────────────────────────────────────────────────────────────────────────────┐\n${RESET}"
printf "${CYAN}│${RESET}  ${BOLD}${MAGENTA}       🚀 PRODUCTION AI SYSTEMS — ONBOARDING & BEST PRACTICES              ${RESET} ${CYAN}│\n${RESET}"
printf "${CYAN}├──────────────────────────────────────────────────────────────────────────────┤\n${RESET}"
printf "${CYAN}│${RESET}  ${BOLD}${YELLOW}🌿 1. BRANCH NAMING CONVENTION:${RESET}                                             ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     Format:   ${GREEN}<type>/<task-id>-<description-in-kebab-case>${RESET}                   ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     Examples: ${WHITE}feat/lab-01-tokenization-math${RESET} ${DIM}|${RESET} ${WHITE}feat/lab-02-embeddings${RESET}         ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}               ${WHITE}chore/repo-governance-and-architecture${RESET}                         ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}                                                                              ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}  ${BOLD}${YELLOW}📝 2. CONVENTIONAL TASK COMMITS:${RESET}                                            ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     Format:   ${GREEN}<type>(<scope>): [<TASK-ID>:#<ISSUE>] <description>${RESET}            ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     Examples: ${WHITE}feat(foundations): [LAB-01:#2] benchmark token compression${RESET}     ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}               ${WHITE}chore(infra): [INFRA] configure automated git hooks${RESET}            ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${DIM}(Gitmoji is automatically injected by prepare-commit-msg hook!)${RESET}          ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}                                                                              ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}  ${BOLD}${YELLOW}🧪 3. QUALITY GATES & COMMANDS:${RESET}                                             ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${BOLD}${GREEN}make check${RESET}      ${DIM}─${RESET} Run black, isort, ruff & detect-secrets                ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${BOLD}${GREEN}make test${RESET}       ${DIM}─${RESET} Run full test suite with pytest & coverage             ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${BOLD}${GREEN}make audit${RESET}      ${DIM}─${RESET} Full audit: syntax compile + linters + unit tests      ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${BOLD}${GREEN}make pr${RESET}         ${DIM}─${RESET} Automated GitHub Pull Request publication              ${CYAN}│\n${RESET}"
printf "${CYAN}│${RESET}     ${BOLD}${GREEN}make help${RESET}       ${DIM}─${RESET} Interactive CLI command center                         ${CYAN}│\n${RESET}"
printf "${CYAN}├──────────────────────────────────────────────────────────────────────────────┤\n${RESET}"
printf "${CYAN}│${RESET}           ${BOLD}${WHITE}🔥 Built for Production AI Systems by ${YELLOW}@RogerioLS${WHITE}${RESET}                   ${CYAN}│\n${RESET}"
printf "${CYAN}└──────────────────────────────────────────────────────────────────────────────┘\n${RESET}"
echo ""
