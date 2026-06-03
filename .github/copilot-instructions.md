# Copilot Instructions — Production AI Systems

This repository is a learning and implementation roadmap for production-grade AI systems.

The main focus areas are:

- LLM applications
- RAG pipelines
- AI Agents
- MCP servers
- OCR and Document Intelligence
- Multimodal AI
- LLMOps
- Financial AI systems

## General Principles

Always favor:

- simple first implementation
- clear architecture
- reproducible examples
- production-oriented thinking
- explicit trade-offs
- measurable outputs
- documentation close to the code

Avoid:

- overengineering
- framework-driven design
- unnecessary abstractions
- tutorial-only implementations
- toy examples without evaluation

## Repository Standards

Every project should contain:

```text
README.md
TODO.md
architecture.md
requirements.txt
src/
notebooks/
experiments/
tests/
```

## Definition of Done

A task is complete only when:

- code runs locally
- minimal documentation exists
- an example is reproducible
- outputs are validated
- trade-offs are documented
- next steps are clear

## Preferred Stack

Use Python as the primary language.

Preferred tools:

- FastAPI
- Pydantic
- AsyncIO
- OpenAI SDK
- Ollama
- LiteLLM
- LlamaIndex
- LangGraph
- Qdrant
- pgvector
- PyMuPDF
- PaddleOCR
- MLflow
- Docker
