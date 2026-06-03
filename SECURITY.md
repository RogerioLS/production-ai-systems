# Security Policy

## Supported Versions

Currently, only the latest version of the repository is supported.

## Reporting a Vulnerability

If you find a security vulnerability, please do NOT open an issue. Instead, report it to the maintainer directly.

## Secret Management

We use `detect-secrets` in our pre-commit hooks to prevent accidental leakage of API keys or credentials. Always use `.env` files and never commit them.
