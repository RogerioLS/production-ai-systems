---
tags:
  - 🟢 Beginner
  - 💻 Interactive Playgrounds
  - 🔬 Math & Theory
---

# 01 - Foundations: Large Language Models

Welcome to the **Foundations of Large Language Models** module. This module explores the transition from mathematical operations to emergent AI phenomena, focusing on subword segmentation, vector spaces, and latent manifold representations.

---

## 🧭 Module Roadmap & Laboratories

To keep the material focused and structured, we have divided this module into two distinct, highly technical laboratories:

### 1. 📊 [LAB-01: Tokenization Math of Compression](a_llm_basics/01_tokenization.md)
Benchmarks BPE vs WordPiece tokenizers, analyzes the character footprint of structured data (JSON), and quantifies the multilingual "Token Tax" on non-English text.

* **Core concepts:** subword segmentation, compression ratio, byte representation.
* **Interactive Playground:** [tokenization_playground.ipynb](../../notebooks/a_llm_basics/tokenization_playground.ipynb)

### 2. 📐 [LAB-02: Embedding Geometry & Semantic Search](a_llm_basics/02_embeddings.md)
Explores the Manifold Hypothesis in high-dimensional vector spaces, implements Cosine Similarity manually, and visualizes word clusters in 2D and 3D.

* **Core concepts:** metric spaces, cosine vs. Euclidean distances, PCA, t-SNE, semantic search indexing.
* **Interactive Playground:** [embeddings_playground.ipynb](../../notebooks/a_llm_basics/embeddings_playground.ipynb)

---

## 🛠️ Resources & References

Below are the academic references and technical guides used in this module, styled in a technical post-card format:

### 📄 Academic & Seminal Papers

<div class="blog-override-posts">

  <!-- Attention Is All You Need -->
  <a id="ref-attention" href="https://arxiv.org/abs/1706.03762" target="_blank" class="blog-override-post">
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
  <a id="ref-bpe" href="https://arxiv.org/abs/1508.07909" target="_blank" class="blog-override-post">
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

  <!-- t-SNE Reference -->
  <a id="ref-tsne" href="https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Visualizing Data using t-SNE</h3>
    <div class="blog-post-extra">
      <b>Laurens van der Maaten, Geoffrey Hinton · </b>
      <span>2008-11-01</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#probabilistic-modeling</code>
      <code>#dimensionality-reduction</code>
      <code>#t-sne</code>
      <code>#paper</code>
    </div>
    <p class="blog-post-description">The landmark paper introducing t-Distributed Stochastic Neighbor Embedding, showcasing its ability to preserve local neighborhood topologies compared to linear methods.</p>
  </a>

</div>

### 📖 Technical References & Guides

<div class="blog-override-posts">

  <!-- Hugging Face Guide -->
  <a id="ref-huggingface" href="https://huggingface.co/docs/tokenizers/index" target="_blank" class="blog-override-post">
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
  <a id="ref-litellm" href="https://litellm.ai" target="_blank" class="blog-override-post">
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

  <!-- Manifold Hypothesis Reference -->
  <a id="ref-manifold" href="https://en.wikipedia.org/wiki/Manifold_hypothesis" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">The Manifold Hypothesis (Wikipedia)</h3>
    <div class="blog-post-extra">
      <b>Wikipedia & Community · </b>
      <span>Mathematical Concept</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#math</code>
      <code>#topology</code>
      <code>#manifold-hypothesis</code>
      <code>#reference</code>
    </div>
    <p class="blog-post-description">Deep dive into why high-dimensional data distributions tend to concentrate near lower-dimensional, non-linear manifolds, which forms the mathematical foundation of neural embeddings.</p>
  </a>

  <!-- PCA Reference -->
  <a id="ref-pca" href="https://en.wikipedia.org/wiki/Principal_component_analysis" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Principal Component Analysis (PCA)</h3>
    <div class="blog-post-extra">
      <b>Karl Pearson · </b>
      <span>1901-07-01</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#linear-algebra</code>
      <code>#dimensionality-reduction</code>
      <code>#pca</code>
      <code>#reference</code>
    </div>
    <p class="blog-post-description">Historical paper and mathematical proof detailing the process of projecting high-dimensional points onto orthogonal eigenvectors to maximize variance.</p>
  </a>

  <!-- Cosine Similarity Reference -->
  <a id="ref-cosine-similarity" href="https://en.wikipedia.org/wiki/Cosine_similarity" target="_blank" class="blog-override-post">
    <h3 class="blog-post-title">Cosine Similarity & Vector Spaces</h3>
    <div class="blog-post-extra">
      <b>Wikipedia & Community · </b>
      <span>Linear Algebra Metric</span>
    </div>
    <div class="blogging-tags-grid">
      <code>#linear-algebra</code>
      <code>#metric-space</code>
      <code>#cosine-similarity</code>
      <code>#reference</code>
    </div>
    <p class="blog-post-description">Overview of cosine similarity, its mathematical formulation, and its application in high-dimensional information retrieval and metric vector spaces.</p>
  </a>

</div>
