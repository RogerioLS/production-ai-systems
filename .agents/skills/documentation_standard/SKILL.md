---
name: documentation_standard
description: Enforces the unified layout, structure, and visual standards for the Production AI Systems documentation.
---

# Documentation Standard v1.0

This skill defines the technical, structural, and visual standards for all documentation pages within the **Production AI Systems** project. All future modules and chapters must strictly follow this format.

---

## 🏗️ Master Page Template

Every content page (e.g., `docs/notes/*.md`) must follow this exact section structure:

```markdown
---
tags:
  - 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced
  - 💻 Interactive Playgrounds (if applicable)
  - 🔬 Math & Theory (if applicable)
---

# [Module Number] - [Chapter Title]: [Sub-title]

## 🎯 Learning Objectives
After reading this chapter, you will be able to:
* [Objective 1]
* [Objective 2]

---

## 🎓 Prerequisites
To get the most out of this chapter, we recommend:
* [Prerequisite 1]

---

## 🧠 Level 1: Intuition & Concepts
[A high-level, clear intuition of the concept. Use analogies, plain language, and Mermaid diagrams.]

---

## 💻 Level 2: Implementation
[Show clean, production-ready, SOLID code snippets representing the implementation of the concepts.]

---

## 📐 Level 3: Mathematical Foundations
[Deep mathematical derivations, equations in LaTeX, loss functions, and probability matrices.]
[CRITICAL: Encapsulate this section inside a collapsible note to keep the page clean for beginner readers.]

??? note "📐 LAB-XX: Mathematical Foundations"
    ### [Formula/Derivation Title]
    $$[LaTeX Equation]$$

---

## 🔬 Level 4: Research Notes (Origin Papers)
[Academic references mapping the concepts to seminal papers in the ML literature.]

---

## 🏭 Production Insights
[Real-world trade-offs, deployment issues, cost optimizations, latency warnings, and architecture limits.]
[CRITICAL: Always use the success admonition block style with the factory emoji.]

!!! note "🏭 [Production Insight Title]"
    * **[Sub-point 1]:** Description...

---

## 📊 LAB-XX: Empirical Results
[Tables comparing benchmarks, tokens, costs, or clustering metrics obtained from local or cloud experiments.]

---

## 🎨 Visualizations
[Static charts, convergence animations (GIFs), or 3D rotations displaying the geometric or topological space.]

---

--8<-- "includes/templates/playground_card_[module].md"

---

## 🧪 Try It Yourself (Experiments)
[Guided tasks for the reader to run inside the Jupyter Playgrounds to observe parameter variations.]

---

## 🧭 Related Concepts
[Knowledge Graph connections pointing to other modules or technical concepts.]
* **[Concept 1]:** Connection description.
* **[Concept 2]:** Connection description.
```

---

## 🧱 Reusable Elements Rules

1. **No Duplicate Code/HTML:** Never duplicate complex HTML buttons or layouts across pages.
2. **Snippet Storage:** Save all reusable elements under `docs/includes/templates/` as markdown files.
3. **Snippet Inclusion:** Include them in pages using the snippet syntax:
   `--8<-- "includes/templates/filename.md"`
4. **MkDocs Configuration:** The `exclude_docs` setting in `mkdocs.yml` must explicitly ignore the `includes/**` path as a multiline string to avoid warnings. The `base_path` for `pymdownx.snippets` must be set to `["docs"]`.

---

## 🎨 Styling Standards

### Admonition Types
Use only official Material for MkDocs admonitions:
* `!!! note` (For standard details/info)
* `!!! success` (For **Production Insights**)
* `!!! warning` (For alerts or common pitfalls)
* `!!! example` (For **Interactive Playgrounds** cards)

### Call-to-Action Buttons
For notebooks, Colab, or GitHub links, use native theme buttons (utilizing the `attr_list` extension):
* **Primary Button (Filled):** `[Text](URL){ .md-button .md-button--primary }`
* **Secondary Button (Outline):** `[Text](URL){ .md-button }`
