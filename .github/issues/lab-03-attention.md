---
title: "[LAB-03] Attention from Scratch: PyTorch Linear Algebra"
labels: ["area: foundations", "type: implementation", "type: math-heavy"]
assignee: "RogerioLS"
---

## 🎯 Objetivo
Construir o bloco de Self-Attention (Q, K, V) puro em PyTorch para compreender a complexidade quadrática e o mecanismo autoregressivo causal.

## 📝 Tarefas
- [x] Implementar Scaled Dot-Product Attention em PyTorch puro.
- [x] Implementar Multi-Head Attention (MHA) com projeções lineares e split de cabeças.
- [x] Implementar máscara causal autoregressiva com triângulo superior infinito negativo.
- [x] Gerar heatmaps visuais das matrizes de pesos de atenção.

## ✅ Critérios de Aceite
- [x] Módulo modular sob SOLID em `projects/a_llm_basics/src/lab_03_attention/`.
- [x] Suíte de testes unitários com pytest em `projects/a_llm_basics/tests/test_attention.py`.
- [x] Notebook interativo com suporte a Google Colab.
