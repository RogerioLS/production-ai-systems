"""Governance Linter for Branch Names and Commit Messages (Production AI Systems).

Validates branch names and commit messages against institutional repository standards.
When executed in GitHub Actions CI, automatically verifies compliance for Pull Requests.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

BRANCH_REGEX = re.compile(
    r"^(feat|fix|docs|test|refactor|chore|ci|build|perf)/"
    r"(lab-[0-9]{2}|infra|hotfix|[a-z0-9-]+)(-[a-z0-9-]+)*$|^dependabot/.*$"
)

COMMIT_REGEX = re.compile(
    r"^([^:]* )?(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([a-zA-Z0-9_\/-]+\))?:\s*\[([a-zA-Z0-9_:#-]+)\]\s*(.+)$"
)

RESERVED_TAGS = {
    "INFRA",
    "CHORE",
    "DOCS",
    "FIX",
    "HOTFIX",
    "GLOBAL",
    "CONFIG",
    "SECURITY",
    "COMMUNITY",
    "DEPS",
    "RELEASE",
    "ENV",
}


def validate_branch_name(branch_name: str) -> Tuple[bool, str]:
    """Validates branch name format against naming conventions."""
    if not branch_name or branch_name in ("main", "master"):
        return True, ""

    if not BRANCH_REGEX.match(branch_name):
        msg = (
            f"❌ **Invalid Branch Name:** `{branch_name}`\n\n"
            f"**Required Format:** `<type>/<task-id>-<short-description-in-kebab-case>`\n\n"
            f"**Valid Examples:**\n"
            f"- `feat/lab-01-tokenization-math`\n"
            f"- `feat/lab-02-embeddings`\n"
            f"- `chore/repo-governance-and-architecture`\n"
            f"- `fix/hotfix-inference-vram`\n"
        )
        return False, msg

    return True, ""


def validate_commit_message(commit_msg: str, issues_dir: Path) -> Tuple[bool, str]:
    """Validates single commit message against Conventional Commits and Task IDs."""
    first_line = commit_msg.strip().splitlines()[0] if commit_msg.strip() else ""

    # Allow merge and rebase commits
    if (
        first_line.startswith("Merge ")
        or first_line.startswith("Revert ")
        or re.match(r"^[0-9]+\.[0-9]+\.[0-9]+", first_line)
    ):
        return True, ""

    match = COMMIT_REGEX.match(first_line)
    if not match:
        msg = (
            f"❌ **Invalid Commit Message:** `{first_line}`\n\n"
            f"**Required Format (Bracketed Task ID is strictly mandatory):**\n"
            f"- `<type>(<scope>): [<TASK-ID>:#<NUM>] <description in lowercase>`\n"
            f"- `<type>(<scope>): [<TASK-ID>] <description in lowercase>`\n"
            f"- `<type>(<scope>): [<RESERVED-TAG>] <description in lowercase>`\n\n"
            f"**Valid Examples:**\n"
            f"- `feat(foundations): [LAB-01:#2] benchmark tokenization compression`\n"
            f"- `chore(infra): [INFRA] configure pre-commit hooks and command center`\n"
        )
        return False, msg

    # Validate task tag
    raw_tag = match.group(4)
    if raw_tag:
        task_tag = raw_tag.split(":")[0].upper()
        if task_tag not in RESERVED_TAGS:
            if not re.match(r"^[a-zA-Z0-9_-]+:#[0-9]+$", raw_tag):
                msg = (
                    f"❌ **Task Commits Must Include GitHub Issue Number:** `[{raw_tag}]`\n\n"
                    f"**Required Format for Project Tasks:**\n"
                    f"`<type>(<scope>): [<TASK-ID>:#<ISSUE_NUM>] <description in lowercase>`\n\n"
                    f"**Valid Example:**\n"
                    f"`feat(foundations): [LAB-01:#2] benchmark tokenization compression`"
                )
                return False, msg

            if issues_dir.exists():
                lower_tag = task_tag.lower()
                matching = list(issues_dir.glob(f"*{lower_tag}*"))
                if not matching:
                    msg = (
                        f"❌ **Unknown Task ID:** `[{task_tag}]`\n\n"
                        f"The task does not exist as a markdown specification in "
                        f"`.github/issues/`.\n"
                        f"If this is an infrastructure/chore change, use a reserved tag:\n"
                        f"`[INFRA]`, `[CHORE]`, `[DOCS]`, `[ENV]`."
                    )
                    return False, msg

    return True, ""


def get_commits_between(base: str, head: str) -> List[str]:
    """Retrieves subject lines of commits between base and head branches."""
    cmd = ["git", "log", f"origin/{base}..{head}", "--oneline"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to local branches
        cmd = ["git", "log", f"{base}..{head}", "--oneline"]
        res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        return []

    lines = []
    for line in res.stdout.strip().splitlines():
        if line.strip():
            # Remove commit hash prefix
            parts = line.strip().split(" ", 1)
            lines.append(parts[1] if len(parts) > 1 else parts[0])
    return lines


def main() -> int:
    """CLI entrypoint for branch and commit linter."""
    parser = argparse.ArgumentParser(description="Lint branch names and commit messages.")
    parser.add_argument("--branch", type=str, help="Branch name to validate.")
    parser.add_argument("--base", type=str, default="main", help="Base branch.")
    parser.add_argument("--pr-number", type=str, help="GitHub PR number if running in CI.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    issues_dir = repo_root / ".github" / "issues"

    branch = args.branch or os.environ.get("GITHUB_HEAD_REF", "")
    if not branch:
        # Detect locally
        res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        branch = res.stdout.strip()

    valid_branch, branch_err = validate_branch_name(branch)
    if not valid_branch:
        print(branch_err, file=sys.stderr)
        return 1

    commits = get_commits_between(args.base, branch)
    for commit in commits:
        valid_commit, commit_err = validate_commit_message(commit, issues_dir)
        if not valid_commit:
            print(commit_err, file=sys.stderr)
            return 1

    print("✔ All branch naming and commit conventions are compliant!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
