# 📊 LLM Basics: Tokenization & Embedding Geometry

This module contains the foundational mathematical and architectural implementations of Large Language Model internals, divided into two completed laboratories.

---

## 🟢 LAB-01: Tokenization Compression Benchmark

This laboratory benchmarks Byte Pair Encoding (BPE) vs WordPiece tokenization efficiency across different domains and languages.

### 📊 Empirical Benchmark Results

#### 1. Compression Ratio (Bytes / Token)
*Higher is better. A higher ratio means more text bytes compressed into fewer tokens.*

| Category | GPT-4o (o200k_base) | GPT-4 (cl100k_base) | GPT-2 (gpt2) | BERT (bert-uncased) |
| --- | --- | --- | --- | --- |
| **Plain English** | 5.200 B/T | 5.200 B/T | 5.200 B/T | 5.200 B/T |
| **Portuguese (PT-BR)** | **5.848 B/T** | **4.825 B/T** | 3.063 B/T | 3.509 B/T |
| **Structured JSON** | 2.735 B/T | 2.735 B/T | 2.548 B/T | 2.114 B/T |
| **Numeric / Tabular** | 1.737 B/T | 1.737 B/T | 2.000 B/T | 1.886 B/T |
| **Emojis / Special Chars** | 2.077 B/T | 1.620 B/T | 1.446 B/T | 10.125 B/T* |

*\*Note: BERT's high ratio on Emojis is an artifact of replacing unrecognized emojis with a single `[UNK]` token, causing information loss. GPT models encode them natively.*

### 💡 Key Insights
- **Portuguese Token Tax Reduction:** The expansion of the vocabulary to 200,000 tokens in GPT-4o (`o200k_base`) yielded a **17.5% reduction in token usage** for PT-BR text compared to GPT-4.
- **JSON Overhead:** Structured data has a compression ratio of only ~2.7 B/T, signifying significant token footprint overhead in agent tool calling loops.

---

## 📐 LAB-02: Embedding Geometry & Manifold Hypothesis

This laboratory explores how high-dimensional vector spaces represent semantic meaning and how they can be projected into human-interpretable manifolds.

### 🧠 Core Concepts
- **Manifold Hypothesis:** High-dimensional data concentrates near lower-dimensional, non-linear manifolds. Neural embeddings represent words as coordinates on these manifolds.
- **Cosine Similarity:** Measures the angular difference between vectors, avoiding the *curse of dimensionality* that degrades Euclidean distance metrics in high dimensions.
- **Dimensionality Reduction:** Uses linear projection (**PCA**) to preserve global variance, and probabilistic mapping (**t-SNE**) to preserve local neighborhood structures.

### 📊 Semantic Metric Evaluation
Using a 100-dimensional category-based vector space, we evaluated semantic coherence:
- **Average Similarity within same category (Intra):** `0.5945`
- **Average Similarity across different categories (Inter):** `-0.0131`
- **Discriminative Margin:** **`0.6077`** (validates perfect semantic cluster separation).

---

## 🚀 Execution & Developer Guides

### 1. How to run tests
Verify all implementations (Tokenizers, Embeddings, Reducers, Search Engine):
```bash
make test
```

### 2. Run Experiments & Visualizations
Generate benchmark metrics and visual manifolds:

```bash
# Run tokenization benchmark report
python -m projects.a_llm_basics.experiments.run_compression_benchmark

# Run 2D PCA & t-SNE static mapping
python -m projects.a_llm_basics.experiments.run_embeddings_experiment

# Generate 2D t-SNE Morphogenesis convergence animation GIF
python -m projects.a_llm_basics.experiments.animate_embeddings

# Generate 3D PCA Space Rotation animation GIF
python -m projects.a_llm_basics.experiments.animate_embeddings_3d
```

### 🎮 Interactive Playgrounds (Google Colab support included)
You can run and modify cells interactively using the Jupyter Playgrounds. Opening them in Colab automatically clones the repo and configures the environment:
- **Tokenization:** [tokenization_playground.ipynb](notebooks/tokenization_playground.ipynb)
- **Embeddings:** [embeddings_playground.ipynb](notebooks/embeddings_playground.ipynb)
