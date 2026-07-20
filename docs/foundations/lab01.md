---
tags:
  - 🟢 Beginner
  - 💻 Interactive Playgrounds
  - 🔬 Math & Theory
---

# LAB-01: Tokenization Math of Compression

## 🎯 Learning Objectives
After completing this laboratory, you will be able to:

* Explain the difference between BPE and WordPiece subword tokenization algorithms.
* Calculate token compression ratios (Bytes per Token) across distinct text domains.
* Analyze the economic and latency impact of vocabulary size on multilingual systems ("Token Tax").
* Design abstract OOP interfaces for multi-model tokenizer clients.

---

## 🎓 Prerequisites
We recommend having:

* Basic Python OOP knowledge.
* Basic understanding of string encoding (UTF-8).
* Loguru and Tiktoken installed in your environment.

---

## 🧠 Level 1: Intuition & Concepts

Large Language Models do not read raw strings. A **Tokenizer** cuts text into smaller units called **Tokens**, mapping them to integer IDs within a fixed vocabulary. Frame this as a statistical data compression task: we want to represent the text using as few tokens as possible without losing semantic content.

### BPE (Byte Pair Encoding)
BPE iteratively merges the most frequent adjacent character or token pairs. It builds vocabularies bottom-up, starting from individual bytes. It is the base tokenizer algorithm for GPT-4, Llama, and Claude.

### WordPiece
Used by BERT, WordPiece merges pairs that maximize the likelihood of the training corpus under a unigram model, focusing on mutual information rather than pure raw count.

---

## 💻 Level 2: Implementation

Here is our clean, SOLID implementation wrapping tokenizer clients:

```python
from abc import ABC, abstractmethod

class BaseTokenizer(ABC):
    @abstractmethod
    def encode(self, text: str) -> list[int]:
        """Converts text into a list of token IDs."""
        pass

    @abstractmethod
    def decode(self, ids: list[int]) -> str:
        """Converts token IDs back to a string."""
        pass
```

We wrap OpenAI's `tiktoken` and Hugging Face's `transformers` under this interface, enabling unified benchmark runs via `TokenizationAnalyzer`.

---

## 📐 Level 3: Mathematical Foundations

??? note "📐 LAB-01: Tokenizer Algorithms Math"
    ### Byte Pair Encoding (BPE)
    BPE selects the most frequent adjacent token pair to merge at each vocabulary expansion step:

    $$\text{Merged Pair} = \arg\max_{A, B \in V} \text{Count}(A, B)$$

    ### WordPiece Score
    WordPiece maximizes corpus likelihood by selecting the pair that maximizes their combined probability relative to their individual occurrences:

    $$\text{Score}(A, B) = \frac{\text{count}(A, B)}{\text{count}(A) \times \text{count}(B)}$$

---

## 🔬 Level 4: Research Notes (Origin Papers)
* **Byte Pair Encoding:** Sennrich et al. (2015) adapted BPE for subword segmentation in machine translation, solving the out-of-vocabulary (OOV) problem ([Sennrich et al., 2015](index.md#ref-bpe)).
* **Hugging Face Tokenizers:** For advanced implementation details, consult the Hugging Face Tokenizer guides ([HF Guide](index.md#ref-huggingface)).

---

## 🏭 Production Insights

!!! success "🏭 The Portuguese Token Tax"
    * **Character Encoding Tax:** Older tokenizers split non-English letters (like `ç`, `ã`) into multiple bytes. GPT-4o (`o200k_base`) expanded its vocabulary to 200k, optimizing character merges. This resulted in a **17.5% reduction in token count** for Portuguese texts compared to GPT-4, directly lowering API latency and cost.
    * **JSON Tool Calling Overhead:** Serializing structured payloads for agent tool calls limits compression to ~2.7 B/T. Keep JSON function schemas minimal to avoid context exhaustion.

---

## 📊 LAB-01: Empirical Results

We benchmarked the tokenizers on a standardized multi-domain corpus:

### 1. Compression Ratio (Bytes per Token)
*Higher is better.*

| Domain | GPT-4o (`o200k_base`) | GPT-4 (`cl100k_base`) | GPT-2 (`gpt2`) | BERT (`bert-uncased`) |
| --- | --- | --- | --- | --- |
| **Plain English** | 5.200 B/T | 5.200 B/T | 5.200 B/T | 5.200 B/T |
| **Portuguese (PT-BR)** | **5.848 B/T** | **4.825 B/T** | 3.063 B/T | 3.509 B/T |
| **Structured JSON** | 2.735 B/T | 2.735 B/T | 2.548 B/T | 2.114 B/T |
| **Numeric / Tabular** | 1.737 B/T | 1.737 B/T | 2.000 B/T | 1.886 B/T |
| **Emojis / Special Chars** | 2.077 B/T | 1.620 B/T | 1.446 B/T | 10.125 B/T* |

*\*Note: BERT's high emoji compression ratio is a false positive due to replacing unrecognized emojis with `[UNK]`, resulting in semantic loss.*

### 2. Generated Token Footprints
*Lower is better.*

| Domain | UTF-8 Bytes | GPT-4o (`o200k_base`) | GPT-4 (`cl100k_base`) | GPT-2 (`gpt2`) | BERT (`bert-uncased`) |
| --- | --- | --- | --- | --- | --- |
| **Plain English** | 156 B | 30 t | 30 t | 30 t | 30 t |
| **Portuguese (PT-BR)** | 193 B | **33 t** | **40 t** | 63 t | 55 t |
| **Structured JSON** | 186 B | 68 t | 68 t | 73 t | 88 t |

---

--8<-- "includes/templates/a_llm_basics/playground_card_tokenization.md"

---

## 🧪 Try It Yourself (Experiments)
1. **Analyze Token Splitting:** Open the playground notebook and encode long words like *"anticonstitucionalmente"*. Observe how the different BPE vocabularies split syllables.
2. **Text Ingestion Cost Estimator:** Write a custom paragraph in French or Spanish, run the analyzer, and compare the byte-to-token footprint against Plain English.

---

## 🧭 Related Concepts
* **Embedding Spaces:** Mapping these token IDs to continuous dense vectors.
* **Context Windows:** The maximum limit of tokens a model can ingest in a single forward pass.
* **Embedding Retrieval:** Storing token vectors inside indexing databases.
