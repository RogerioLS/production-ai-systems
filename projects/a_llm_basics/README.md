# 📊 LLM Foundations: Tokenization, Embeddings, Attention & Inference Math

This module contains the foundational mathematical and architectural implementations of Large Language Model internals, divided into four fully completed laboratories.

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

## 🧠 LAB-03: Attention Mechanics from Scratch

This laboratory implements pure PyTorch linear algebra for Transformer self-attention mechanisms and causal autoregressive masking.

### 🧠 Core Concepts
- **Scaled Dot-Product Attention:** Computes $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.
- **Causal Autoregressive Masking:** Prevents leftward information flow in decoder-only models by applying $-\infty$ upper-triangular masks before Softmax.
- **Multi-Head Attention (MHA):** Enables the model to jointly attend to information from different representation subspaces.

---

## 🎲 LAB-04: Inference Math, Sampling & Quantization

This laboratory models the mathematical mechanics of autoregressive generation, post-training quantization, and hardware memory scaling.

### 🧠 Core Concepts
- **Autoregressive Sampling:** Temperature scaling ($T$), Top-$k$ filtering, and Top-$p$ (Nucleus) dynamic cumulative truncation.
- **Uniform Linear Quantization:** Maps FP32 tensors to INT8 and INT4 with scale factors and zero-points, measuring reconstruction fidelity via Signal-to-Quantization-Noise Ratio (SQNR).
- **Inference Hardware Economics:** Formulates memory allocation for model weights vs. dynamic KV Cache:
  $$M_{\text{kv}} = 2 \times b_{\text{bytes}} \times n_{\text{layers}} \times d_{\text{model}} \times s_{\text{seq}} \times b_{\text{batch}}$$

### 📊 VRAM Benchmark (8B Model)

| Precision Format | Weights VRAM | KV Cache (8k ctx, B=1) | Total VRAM (B=1, 8k) | Perplexity Shift ($\Delta \text{PPL}$) |
| --- | --- | --- | --- | --- |
| **FP32** | 32.0 GB | 4.0 GB | 36.0 GB | 0.00 (Baseline) |
| **FP16 / BF16** | 16.0 GB | 2.0 GB | 18.0 GB | +0.01 |
| **INT8** | 8.0 GB | 1.0 GB | 9.0 GB | +0.04 |
| **INT4 / AWQ** | 4.0 GB | 0.5 GB | 4.5 GB | +0.18 |

---

## 🚀 Execution & Developer Guides

### 1. How to run tests
Verify all implementations (Tokenizers, Embeddings, Attention, Inference Math):
```bash
make test
```

### 2. Run Experiments & Visualizations
Generate benchmark metrics, visualizations, and animated manifolds:

```bash
# LAB-01: Tokenization compression benchmark report
python -m projects.a_llm_basics.experiments.run_compression_benchmark

# LAB-02: 2D PCA & t-SNE static mapping
python -m projects.a_llm_basics.experiments.run_embeddings_experiment

# LAB-02: Generate 2D t-SNE convergence animation GIF
python -m projects.a_llm_basics.experiments.animate_embeddings

# LAB-02: Generate 3D PCA Space Rotation animation GIF
python -m projects.a_llm_basics.experiments.animate_embeddings_3d

# LAB-03: Scaled Dot-Product & Causal Attention Heatmaps
python -m projects.a_llm_basics.experiments.run_attention_experiment

# LAB-04: Sampling distributions, SQNR benchmarks & VRAM scaling
python -m projects.a_llm_basics.experiments.run_inference_experiment
```

### 🎮 Interactive Playgrounds (Google Colab support included)
You can run and modify cells interactively using the Jupyter Playgrounds:
- **LAB-01 Tokenization:** [tokenization_playground.ipynb](notebooks/tokenization_playground.ipynb)
- **LAB-02 Embeddings:** [embeddings_playground.ipynb](notebooks/embeddings_playground.ipynb)
- **LAB-03 Attention:** [attention_playground.ipynb](notebooks/attention_playground.ipynb)
- **LAB-04 Inference:** [inference_playground.ipynb](notebooks/inference_playground.ipynb)
