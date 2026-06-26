# 01 - Foundations: Large Language Models

## 🎯 Objective
Deep understanding of model internals, inference, tokenization math, embedding geometry, and self-attention mechanics.

## 📚 Concepts & Math Alignment
### 1. Tokenization as Statistical Compression
Tokenization is a fundamental data compression task. Given a corpus, we learn a vocabulary $V$ that maps variable-length sequences of characters to integer IDs. The compression efficiency is defined by:
$$\text{Compression Ratio} = \frac{\text{Bytes of UTF-8 Text}}{\text{Tokens Generated}}$$

- **BPE (Byte Pair Encoding):** Merges the most frequent adjacent byte/token pairs iteratively. Used in GPT-4 (`cl100k_base`), GPT-4o (`o200k_base`), Llama, and Claude.
- **WordPiece:** Merges the pair that maximizes the likelihood of the corpus under a unigram model, maximizing the mutual information:
  $$\text{Score}(A, B) = \frac{\text{count}(A, B)}{\text{count}(A) \times \text{count}(B)}$$

---

## 📊 LAB-01: Tokenization Benchmark Results

We compared the tokenizers across various domains. Here is the empirical evaluation:

### 1. Compression Ratio (Bytes per Token)
*Higher is more efficient (fewer tokens used per byte).*

| Domain | GPT-4o (`o200k_base`) | GPT-4 (`cl100k_base`) | GPT-2 (`gpt2`) | BERT (`bert-uncased`) |
| --- | --- | --- | --- | --- |
| **Plain English** | 5.200 B/T | 5.200 B/T | 5.200 B/T | 5.200 B/T |
| **Portuguese (PT-BR)** | **5.848 B/T** | **4.825 B/T** | 3.063 B/T | 3.509 B/T |
| **Structured JSON** | 2.735 B/T | 2.735 B/T | 2.548 B/T | 2.114 B/T |
| **Numeric / Tabular** | 1.737 B/T | 1.737 B/T | 2.000 B/T | 1.886 B/T |
| **Emojis / Special Chars** | 2.077 B/T | 1.620 B/T | 1.446 B/T | 10.125 B/T* |

*\*Note: BERT's high ratio on Emojis is an artifact of replacing all unrecognized emojis with a single `[UNK]` token, representing a loss of information, whereas GPT models encode them natively without information loss.*

### 2. Token Counts (Total Tokens Generated)
*Lower token count means lower latency and API cost.*

| Domain | UTF-8 Bytes | GPT-4o (`o200k_base`) | GPT-4 (`cl100k_base`) | GPT-2 (`gpt2`) | BERT (`bert-uncased`) |
| --- | --- | --- | --- | --- | --- |
| **Plain English** | 156 B | 30 t | 30 t | 30 t | 30 t |
| **Portuguese (PT-BR)** | 193 B | **33 t** | **40 t** | 63 t | 55 t |
| **Structured JSON** | 186 B | 68 t | 68 t | 73 t | 88 t |
| **Numeric / Tabular** | 66 B | 38 t | 38 t | 33 t | 35 t |
| **Emojis / Special Chars** | 81 B | 39 t | 50 t | 56 t | 8 t |

---

## 💡 Key Architectural Insights

1. **The Portuguese Token Tax Reduction:**
   GPT-4o (`o200k_base`) uses a larger vocabulary of 200,000 tokens compared to GPT-4's 100,000. In Portuguese, this results in a **17.5% reduction in token count** (from 40 tokens to 33 tokens). For production systems processing large documents in Portuguese, migrating to GPT-4o or a model with a similar expanded vocabulary directly yields 17.5% cost savings and lower latency.

2. **JSON & Structured Tool Calling Overhead:**
   Structured JSON parsing has a compression ratio of only ~2.7 B/T compared to ~5.2 B/T for English text. Since agent workflows rely heavily on JSON schemas for Tool Calling, this structural overhead represents a significant cost driver in multi-agent routing.

3. **Digit Splitting in Finance:**
   Numeric data is tokenized at a very low compression ratio (~1.7 B/T). Tokenizers split numbers into individual or pairs of digits to allow the model to generalize math operations better, but this increases the token footprint of financial tabular data.

---

## 🛠️ Resources & References
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [BPE Paper: Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)
- [Hugging Face Tokenizers Guide](https://huggingface.co/docs/tokenizers/index)
- [Ollama & LiteLLM Integration Docs](https://litellm.ai)
