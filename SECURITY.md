# Security Policy — Production AI Systems

## 🛡️ Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

---

## 🔒 Secret Management & LLM API Safety

In AI engineering, security of credentials, API endpoints, and model weights is paramount:

1. **Zero Secret Ingestion:**
   - Never commit `.env` files, OpenAI API keys, Anthropic tokens, database credentials, or cloud access keys.
   - All commits are verified locally by `detect-secrets` during `make check`.
2. **Environment Variables:**
   - Store sensitive keys in local `.env` files (ignored in `.gitignore`).
   - Use `python-dotenv` and Pydantic `BaseSettings` for secure runtime configuration.
3. **Model & Data Sandboxing:**
   - Never execute untrusted LLM-generated code without containerized sandboxing.
   - When integrating tool use or MCP servers, validate inputs against strict Pydantic schemas.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within this repository:

1. **Do NOT open a public issue.**
2. Please contact the project maintainer directly via GitHub Security Advisories or email at `rogerio_288@hotmail.com`.
3. Provide a clear description, reproduction steps, and potential impact.
4. We will review and provide a patch promptly.
