# Contributing to Production AI Systems

## Standards

- **Conventional Commits**: Please use the conventional commit format for your commits.
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation updates
  - `refactor:` for code changes that neither fix a bug nor add a feature
  - `test:` for adding missing tests or correcting existing tests
- **TDD (Test-Driven Development)**: Encourage writing tests before or alongside code.
- **ADRs (Architectural Decision Records)**: If you make a significant architectural decision, please document it in `docs/adr/`.

## Setup

1. Clone the repository.
2. Run `make install` to set up the environment and pre-commit hooks.
3. Use `make check` to ensure code quality before pushing.
