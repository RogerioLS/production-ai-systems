# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Enterprise-grade repository governance, automated Git hooks (`commit-msg`, `prepare-commit-msg`), and onboarding banner.
- Master Command Center `Makefile` with ANSI colors, `make help`, `make audit`, `make pr`, and `make sync-tasks`.
- GitHub issue templates (`bug_report.yml`, `lab_request.yml`, `feature_discussion.yml`).
- Automated PR labeler configuration and branch linting workflow.

---

## [0.1.0] - 2026-09-23

### Added
- **Module 01: LLM Foundations (`projects/a_llm_basics/`)**:
  - `[LAB-01]` Tokenization Compression Benchmark (BPE vs WordPiece, Portuguese Token Tax calculation).
  - `[LAB-02]` Embedding Geometry & Manifold Hypothesis (Cosine metric spaces, PCA/t-SNE dimensionality reduction, semantic search engine).
  - `[LAB-03]` Attention from Scratch (Scaled Dot-Product, Multi-Head Attention, causal autoregressive masking in pure PyTorch).
  - `[LAB-04]` Inference Math & Quantization (Autoregressive sampling with Temperature, Top-k, Top-p; Uniform Linear INT8/INT4 Quantization & SQNR; Perplexity & KV Cache VRAM calculator).
- 43 automated unit tests with 100% pass rate in `pytest`.
- 4 interactive Jupyter Playgrounds with full Google Colab support.
- MkDocs technical documentation, MathJax LaTeX equations, and animated visual assets.
