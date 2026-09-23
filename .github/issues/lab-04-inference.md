---
title: "[LAB-04] Inference Math: Sampling, Quantization & Loss Analysis"
labels: ["area: foundations", "type: implementation", "type: math-heavy"]
assignee: "RogerioLS"
---

## 🎯 Objetivo
Estudar a matemática por trás da geração de texto, o impacto da quantização na precisão e o dimensionamento de hardware (VRAM para pesos e KV Cache).

## 📝 Tarefas
- [x] Implementar amostragem autoregressiva: Temperature Scaling, Top-k e Top-p (Nucleus).
- [x] Implementar quantização linear uniforme (FP32 -> INT8/INT4) e medição de SQNR.
- [x] Implementar cálculo de Cross-Entropy, Entropia de Shannon e Perplexidade.
- [x] Implementar calculadora analítica de VRAM para pesos e KV Cache.

## ✅ Critérios de Aceite
- [x] Módulo modular sob SOLID em `projects/a_llm_basics/src/lab_04_inference/`.
- [x] Suíte de 23 testes unitários com pytest em `projects/a_llm_basics/tests/test_inference.py`.
- [x] Notebook interativo com suporte a Google Colab e documentação técnica em MkDocs.
