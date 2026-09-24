# 🎯 Module 02: Prompt Engineering, Structured Outputs & Spec-Driven Development

This module provides enterprise-grade implementations of advanced prompt engineering techniques, deterministic structured data extraction, and contract-first Spec-Driven Development (SDD).

---

## 🧭 Laboratory Roadmap

### 1. 🧠 [LAB-05: Prompt Reasoning Patterns](docs/prompt_engineering/lab05.md)
Systematic implementation and empirical evaluation of reasoning strategies:
- Zero-Shot vs Few-Shot In-Context Learning (dynamic selection)
- Chain-of-Thought (CoT) structured decomposition
- Self-Consistency with stochastic sampling & Majority Voting
- Autonomous ReAct (`Thought -> Action -> Observation -> Final Answer`) loops

### 2. 🧱 [LAB-06: Structured Outputs & Schema Enforcement](docs/prompt_engineering/lab06.md)
Guaranteed structural compliance and resilient extraction:
- Pydantic v2 schemas with strict validators
- Native JSON Schema enforcement vs XML delimited prompting
- Self-Healing / Reflection error correction loops with dynamic feedback

### 3. 💼 [LAB-07: Production Financial Asset Extractor](docs/prompt_engineering/lab07.md)
Production-grade financial document parsing:
- Corporate Balance Sheet extraction (Assets, Liabilities, Equity, EBITDA)
- Banking credit proposal parser (CET, amortization schedules, collateral)
- Deterministic accounting consistency validation

### 4. 📐 [LAB-08: Spec-Driven Development (OpenSpec)](docs/prompt_engineering/lab08.md)
Contract-first AI engineering:
- Declarative `.spec.yaml` contracts
- Automated model and test suite synthesis
- Runtime compliance auditing for agent interactions
