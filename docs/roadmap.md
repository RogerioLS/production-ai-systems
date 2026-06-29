# Roadmap & Module Progression

This page outlines the curriculum and sequential projects designed to build deep, production-grade expertise in AI systems.

---

## 🗺️ Learning Path

The roadmap is structured sequentially. Each module serves as a mathematical or architectural foundation for the next.

```mermaid
flowchart TD
    A[01. LLM Foundations] --> B[02. Prompt Engineering]
    B --> C[03. Structured Outputs]
    C --> D[04. RAG Systems]
    D --> E[05. OCR & Document Intelligence]
    E --> F[06. AI Agents]
    F --> G[07. Model Context Protocol]
    G --> H[08. LLMOps & Observability]
    H --> I[09. Fine-Tuning]
    I --> J[10. Multimodal AI]
    J --> K[11. Financial AI Systems]

    style A fill:#4CAF50,stroke:#388E3C,color:#fff
    style B fill:#FF9800,stroke:#F57C00,color:#fff
    style C fill:#FF9800,stroke:#F57C00,color:#fff
    style D fill:#FF9800,stroke:#F57C00,color:#fff
    style E fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style F fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style G fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style H fill:#F44336,stroke:#D32F2F,color:#fff
    style I fill:#F44336,stroke:#D32F2F,color:#fff
    style J fill:#2196F3,stroke:#1976D2,color:#fff
    style K fill:#009688,stroke:#00796B,color:#fff
```

---

## 📊 Module Classification & Complexity

To optimize the learning curve, each topic is classified by difficulty level and estimated duration.

| Module | Topic | Difficulty | Est. Timeline | Focus Area |
| :--- | :--- | :---: | :---: | :--- |
| **01** | Foundations & Math of LLMs | 🟢 Easy | 2 weeks | BPE/WordPiece, Embedding Space, Attention Blocks |
| **02** | Prompt Engineering | 🟢 Easy | 1 week | Few-shot, COT, XML/JSON schemas |
| **03** | Structured Outputs | 🟢 Easy | 1 week | Pydantic validation, Instructor, Guardrails |
| **04** | RAG (Retrieval-Augmented) | 🟡 Medium | 3 weeks | Hybrid Search, Chunking, Re-ranking, Vector DBs |
| **05** | OCR & Parsing | 🟡 Medium | 2 weeks | Unstructured data extraction, Docling, LayoutLM |
| **06** | AI Agents & State Machines | 🟠 Hard | 4 weeks | LangGraph, Reasoning loops, Memory, Orchestration |
| **07** | MCP (Model Context Protocol) | 🟠 Hard | 2 weeks | API endpoints, Secure tool sandboxing, Tool Registry |
| **08** | LLMOps | 🔴 Expert | 4 weeks | Monitoring (Phoenix, LangSmith), Security, Evals |
| **09** | Fine-Tuning | 🔴 Expert | 3 weeks | LoRA, QLoRA, PEFT, Distillation |

---

## 🧭 Project Architecture Principles

Every project implemented throughout this roadmap must strictly adhere to the following delivery standards:
- **Zero Placeholder Code:** All APIs, data structures, and tests must be complete and executable.
- **Strict Linting & Formats:** Pre-commit checks via Black, Isort, and Ruff must pass seamlessly.
- **Robust Verification:** Every module must contain reproducible benchmark scripts and at least 90% pytest unit test coverage.
- **Clean Documentation:** Code rationales, mathematical proofs, and trade-off considerations must be logged inside the respective module's `README.md`.
