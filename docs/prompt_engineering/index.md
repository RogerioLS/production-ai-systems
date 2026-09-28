---
tags:
  - 🟡 Intermediate
  - 💻 Interactive Playgrounds
  - 🔬 Math & Theory
---

# 02 - Prompt Engineering: Reasoning, Structured Outputs & SDD

Welcome to the **Prompt Engineering & Structured Outputs** module. This module bridges high-level semantic steering and deterministic software engineering: exploring cognitive prompting patterns, schema enforcement via Pydantic v2, and contract-first Spec-Driven Development (SDD).

---

## 🧭 Module Roadmap & Laboratories

To keep the material structured, rigorous, and production-oriented, this module is divided into four comprehensive laboratories:

### 1. 🧠 [LAB-05: Prompt Reasoning Patterns: Few-Shot, CoT, Self-Consistency & ReAct](lab05.md)
Implements and benchmarks cognitive reasoning induction: Zero-Shot, Few-Shot In-Context Learning (dynamic selection), Chain-of-Thought, Self-Consistency with Shannon Entropy consensus, and autonomous ReAct agent loops.

* **Core concepts:** In-Context Learning, Zero-Shot CoT, Majority Voting, Shannon Entropy, Tool Execution loops.
* **Interactive Playground:** [reasoning_playground.ipynb](reasoning_playground.ipynb)

### 2. 🧱 [LAB-06: Structured Outputs: Pydantic v2, Instructor & Schema Enforcement](lab06.md)
Industrial pipeline for structured data extraction with runtime schema validation, OpenAI Tool Calling/JSON mode, XML tag prompting, and Self-Healing / Reflection error recovery loops.

* **Core concepts:** Pydantic v2 validation, JSON Schema, XML delimiters, Self-Healing reflection loops.
* **Interactive Playground:** [structured_outputs_playground.ipynb](structured_outputs_playground.ipynb)

### 3. 💼 [LAB-07: Production Application: Financial Asset & Proposal Extractor](lab07.md)
Production-grade financial document extraction pipeline parsing corporate balance sheets (Assets, Liabilities, EBITDA) and bank credit proposals with deterministic accounting consistency checks (`Assets == Liabilities + Equity`).

* **Core concepts:** Domain modeling, financial parsing, mathematical consistency validation, confidence scoring.
* **Interactive Playground:** [financial_extractor_playground.ipynb](financial_extractor_playground.ipynb)

### 4. 📐 [LAB-08: Spec-Driven Development: OpenSpec & Contract Compliance](lab08.md)
Contract-first AI engineering: formal declarative specifications (`.spec.yaml`), automated Pydantic model generation, and runtime compliance auditing via `SpecComplianceChecker`.

* **Core concepts:** Contract-first design, OpenSpec, schema generation, runtime compliance verification.
* **Interactive Playground:** [spec_driven_playground.ipynb](spec_driven_playground.ipynb)

---

## 🛠️ Resources & References

Below are the academic references and technical guides used in this module, styled in our standardized post-card format:

### 📄 Academic & Seminal Papers

<div class="blog-override-posts">

  <!-- Few-Shot Paper -->
  <a id="ref-fewshot" href="https://arxiv.org/abs/2005.14165" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Language Models are Few-Shot Learners</h3>
    <div class="blog-post-extra">
      <b>Brown et al. (OpenAI) · </b>
      <span>2020-05-28</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#in-context-learning</code>
      <code>#few-shot</code>
      <code>#prompting</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">The seminal GPT-3 paper introducing In-Context Learning (ICL) as an emergent capability of autoregressive models without weight updating.</p>
  </a>

  <!-- Chain of Thought Paper -->
  <a id="ref-cot" href="https://arxiv.org/abs/2201.11903" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Chain-of-Thought Prompting Elicits Reasoning in Large Language Models</h3>
    <div class="blog-post-extra">
      <b>Wei et al. (Google Research) · </b>
      <span>2022-01-28</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#reasoning</code>
      <code>#chain-of-thought</code>
      <code>#cot</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">Demonstrates that generating a series of intermediate reasoning steps dramatically improves the ability of large models to perform complex arithmetic, commonsense, and symbolic reasoning.</p>
  </a>

  <!-- Zero-Shot CoT Paper -->
  <a id="ref-zeroshot-cot" href="https://arxiv.org/abs/2205.11916" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Large Language Models are Zero-Shot Reasoners</h3>
    <div class="blog-post-extra">
      <b>Kojima et al. · </b>
      <span>2022-05-24</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#zero-shot</code>
      <code>#reasoning</code>
      <code>#prompting</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">Introduces the classic trigger phrase 'Let\'s think step by step', unlocking multi-step deduction without needing task-specific few-shot exemplars.</p>
  </a>

  <!-- Self-Consistency Paper -->
  <a id="ref-self-consistency" href="https://arxiv.org/abs/2203.11171" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Self-Consistency Improves Chain of Thought Reasoning in Language Models</h3>
    <div class="blog-post-extra">
      <b>Wang et al. (Google Research) · </b>
      <span>2022-03-21</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#self-consistency</code>
      <code>#majority-voting</code>
      <code>#consensus</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">Proposes sampling a diverse set of reasoning paths via non-zero temperature and marginalizing out reasoning paths to find the consensus answer via majority vote.</p>
  </a>

  <!-- ReAct Paper -->
  <a id="ref-react" href="https://arxiv.org/abs/2210.03629" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">ReAct: Synergizing Reasoning and Acting in Language Models</h3>
    <div class="blog-post-extra">
      <b>Yao et al. (Princeton & Google) · </b>
      <span>2022-10-06</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#react</code>
      <code>#agents</code>
      <code>#tool-use</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">Combines reasoning traces and task-specific actions in an interleaved loop, allowing LLMs to interact with external environments and tools dynamically.</p>
  </a>

</div>

### 📖 Technical References & Guides

<div class="blog-override-posts">

  <!-- Pydantic v2 Documentation -->
  <a id="ref-pydantic" href="https://docs.pydantic.dev/latest/" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Pydantic v2 Documentation</h3>
    <div class="blog-post-extra">
      <b>Samuel Colvin & Pydantic Team · </b>
      <span>2023-06-30</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#pydantic</code>
      <code>#validation</code>
      <code>#schemas</code>
      <code>#guide</code>
    </div>
    <p class="blog-post-description">High-performance data validation and parsing using Python type hints, powered by the Rust-based pydantic-core engine.</p>
  </a>

  <!-- Instructor Library -->
  <a id="ref-instructor" href="https://python.useinstructor.com/" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Instructor: Structured LLM Outputs</h3>
    <div class="blog-post-extra">
      <b>Jason Liu · </b>
      <span>2023-11-15</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#structured-outputs</code>
      <code>#instructor</code>
      <code>#tool-calling</code>
      <code>#guide</code>
    </div>
    <p class="blog-post-description">Python library built on Pydantic to enforce typed JSON outputs from LLMs with automatic retries and validation hooks.</p>
  </a>

  <!-- OpenSpec Framework -->
  <a id="ref-openspec" href="https://openspec.dev/" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">OpenSpec: Contract-First Specification Standard</h3>
    <div class="blog-post-extra">
      <b>OpenSpec Community · </b>
      <span>2024-01-10</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#openspec</code>
      <code>#sdd</code>
      <code>#contracts</code>
      <code>#guide</code>
    </div>
    <p class="blog-post-description">Standardized declarative framework for defining AI agent behaviors, contracts, and evaluation benchmarks prior to implementation.</p>
  </a>

</div>
