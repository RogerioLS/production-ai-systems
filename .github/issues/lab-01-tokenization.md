---
title: "[LAB-01] Setup Environment and Tokenization Experiment"
labels: ["foundations", "lab"]
assignee: "rogerio-silva"
---

## 🎯 Description
Initialize the structural environment for the `01_llm_basics` project and implement the first experiment comparing different tokenization strategies.

## 🛠️ Technical Implementation
1. **Directory Structure**: Verify if `projects/01_llm_basics/` contains `src/`, `notebooks/`, and `tests/`.
2. **Requirements**: Install the base libraries: `tiktoken`, `transformers`, `numpy`.
3. **Core Utility**: Refine `src/tokenizer_utils.py` to support multiple encodings:
    - `cl100k_base` (GPT-4)
    - `p50k_base` (GPT-3.5)
    - HuggingFace Proxy for Llama/Claude models.

## 🧪 Experiments
- Compare the number of tokens for technical texts in Portuguese vs English.
- Calculate the "Tokenization Efficiency" (Characters per Token).

## ✅ Definition of Done
- [x] Folder structure created.
- [x] `requirements.txt` defined.
- [x] Initial `tokenizer_utils.py` implemented.
- [ ] Requirements installed in the virtual environment.
- [ ] Successful execution of `tokenizer_utils.py` with custom text.
