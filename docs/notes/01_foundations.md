# 01 - Foundations: Large Language Models

## 🎯 Objective
Deep understanding of model internals, inference, tokenization math, embedding geometry, and self-attention mechanics.

## 📚 Concepts & Math Alignment
### 1. Tokenization as Statistical Compression
Tokenization is a fundamental data compression task. Given a corpus, we learn a vocabulary $V$ that maps variable-length sequences of characters to integer IDs. The compression efficiency is defined by:
$\text{Compression Ratio} = \frac{\text{Bytes of UTF-8 Text}}{\text{Tokens Generated}}$

- **BPE (Byte Pair Encoding):** Merges the most frequent adjacent byte/token pairs iteratively. Used in GPT-4 (`cl100k_base`), GPT-4o (`o200k_base`), Llama, and Claude.
- **WordPiece:** Merges the pair that maximizes the likelihood of the corpus under a unigram model, maximizing the mutual information:
  $\text{Score}(A, B) = \frac{\text{count}(A, B)}{\text{count}(A) \times \text{count}(B)}$

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

## 💻 API & Code Reference

Below is the technical documentation automatically generated from the docstrings of our LAB-01 implementation:

::: projects.a_llm_basics.src.tokenizer_math
    options:
      handler: python
      show_source: true

---

## 🛠️ Resources & References

Below are the academic references and technical guides used in this module, structured in a technical post-card format:

<style>
.blog-override-posts {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 20px;
}

.blog-override-post {
  padding: 12px 20px 12px 14px;
  margin-top: 10px;
  border: 1px solid transparent;
  border-left: 4px solid var(--md-primary-fg-color, #3f51b5);
  cursor: pointer;
  display: block;
  text-decoration: none !important;
  color: inherit !important;
}

.blog-override-post .blog-post-title {
  color: #3f51b5 !important;
  font-size: 1.15rem;
  font-weight: 500;
  margin-top: 0;
  margin-bottom: .35rem;
  line-height: 1.3;
}

.blog-post-description {
  color: var(--md-typeset-color);
  font-size: 0.85rem;
  margin-top: 0.4rem;
  margin-bottom: 0;
}

.blog-override-post:hover {
  border: 1px solid #e8e8e877;
  box-shadow: 3px 4px 10px #e8e8e8;
}

.blog-override-post,
.blog-override-post>* {
  transition: all 0.3s ease-in-out;
}

.blog-override-post:hover>* {
  transform: translateX(30px);
}

.blog-post-description,
.blog-post-extra {
  opacity: 0.8;
}

.blog-override-post:hover .blog-post-description,
.blog-override-post:hover .blog-post-extra {
  opacity: 1;
}

.blog-override-post:hover .blog-post-title {
  color: #ff9800 !important;
}

.blog-post-extra {
  font-size: 0.78rem;
  color: #777;
  font-weight: 700;
  margin-bottom: .45rem;
}

.blogging-tags-grid {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 5px;
}

.blogging-tags-grid code {
  background-color: #f5eee8;
  color: #222 !important;
  border-radius: 5px;
  font-family: monospace;
  font-size: .65rem;
  font-weight: 700;
  padding: .08rem .24rem;
  transition: color 0.15s ease;
}

.blogging-tags-grid code:hover {
  color: #ff9800 !important;
}

@media only screen and (max-width: 1000px) {
  .blog-override-post,
  .blog-override-post>* {
    transition: none;
  }

  .blog-override-post:hover>* {
    transform: none;
  }

  .blog-override-post {
    padding: 30px 0 30px 0;
    border: none;
    cursor: pointer;
  }

  .blog-override-post:hover {
    border: none;
    box-shadow: none;
  }

  .blog-post-description,
  .blog-post-extra,
  .blog-override-post:hover .blog-post-description,
  .blog-override-post:hover .blog-post-extra {
    opacity: 1;
  }
}

/* Dark Mode Slate Support */
[data-md-color-scheme="slate"] .blog-override-post:hover {
  border-color: #334155;
  box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.4);
}
[data-md-color-scheme="slate"] .blog-override-post .blog-post-title {
  color: #818cf8 !important;
}
[data-md-color-scheme="slate"] .blog-override-post:hover .blog-post-title {
  color: #ff9800 !important;
}
[data-md-color-scheme="slate"] .blogging-tags-grid code {
  background-color: #334155;
  color: #cbd5e1 !important;
}
[data-md-color-scheme="slate"] .blogging-tags-grid code:hover {
  color: #ff9800 !important;
}
[data-md-color-scheme="slate"] .blog-post-extra {
  color: #94a3b8;
}
</style>

<div class="blog-override-posts">

  <!-- Attention Is All You Need -->
  <a href="https://arxiv.org/abs/1706.03762" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Attention Is All You Need</h3>
    <div class="blog-post-extra">
      <b>Vaswani et al. · </b>
      <span>2017-06-12</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#architecture</code>
      <code>#transformers</code>
      <code>#attention</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">The seminal paper introducing the Transformer architecture, replacing recurrent and convolutional neural networks with self-attention mechanism layers.</p>
  </a>

  <!-- BPE Paper -->
  <a href="https://arxiv.org/abs/1508.07909" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Neural Machine Translation of Rare Words with Subword Units</h3>
    <div class="blog-post-extra">
      <b>Sennrich et al. · </b>
      <span>2015-08-31</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#tokenization</code>
      <code>#bpe</code>
      <code>#nlp</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">The original paper adapting Byte Pair Encoding (BPE) for word segmentation in machine translation, solving the out-of-vocabulary words problem.</p>
  </a>

  <!-- Hugging Face Guide -->
  <a href="https://huggingface.co/docs/tokenizers/index" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Hugging Face Tokenizers Guide</h3>
    <div class="blog-post-extra">
      <b>Hugging Face Team · </b>
      <span>2020-03-10</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#tokenization</code>
      <code>#tooling</code>
      <code>#guide</code>
    </div>
    <p class="blog-post-description">Practical implementation details, benchmarks, and algorithms for BPE, WordPiece, and SentencePiece tokenizers.</p>
  </a>

  <!-- Ollama & LiteLLM Integration Docs -->
  <a href="https://litellm.ai" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Ollama & LiteLLM Integration Docs</h3>
    <div class="blog-post-extra">
      <b>LiteLLM Team · </b>
      <span>2023-10-01</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#local-inference</code>
      <code>#apis</code>
      <code>#tooling</code>
    </div>
    <p class="blog-post-description">Guide on running local LLM inference engines and wrapping them with OpenAI-compatible routing for development fallbacks.</p>
  </a>

</div>
