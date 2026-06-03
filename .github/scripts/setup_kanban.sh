#!/bin/bash

# Pegar o nome do repositório atual (owner/repo)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# 1. Criar Milestone via API
echo "🎯 Criando Milestone: 01. LLM Foundations no repo $REPO..."
gh api repos/$REPO/milestones -f title="01. LLM Foundations" -f description="Fundamentos matemáticos e mecânicos de LLMs para engenharia de ML."

# 2. Criar Labels
echo "🏷️ Criando Labels profissionais..."
gh label create "area: foundations" --color "3498db" --description "Conceitos base e fundamentais" --force
gh label create "type: research" --color "95a5a6" --description "Pesquisa acadêmica e teoria matemática" --force
gh label create "type: implementation" --color "2ecc71" --description "Desenvolvimento de código e LABs" --force
gh label create "type: math-heavy" --color "e74c3c" --description "Foco em Álgebra Linear e Teoria da Informação" --force

# 3. Criar Issues (Tasks)
echo "🚀 Populando o Kanban com as tasks do Módulo 01..."

# Task 1
gh issue create \
  --title "[LAB-01] Tokenization: Math of Compression (BPE vs WordPiece)" \
  --milestone "01. LLM Foundations" \
  --label "area: foundations,type: research,type: math-heavy" \
  --body "## 🎯 Objetivo
Analisar a tokenização como um problema de compressão estatística e Teoria da Informação.

## 📝 Tarefas
- [ ] Implementar análise de eficiência de compressão (bytes por token).
- [ ] Validar o impacto matemático de caracteres especiais na janela de contexto.
- [ ] Comparar vocabulários (Tiktoken vs HF Tokenizers).

## ✅ Critérios de Aceite
- Script em \`projects/01_llm_basics/src/tokenizer_math.py\`.
- Relatório de compression ratio no README do lab."

# Task 2
gh issue create \
  --title "[LAB-02] Embedding Geometry: The Manifold Hypothesis Visualization" \
  --milestone "01. LLM Foundations" \
  --label "area: foundations,type: implementation,type: math-heavy" \
  --body "## 🎯 Objetivo
Visualizar como a álgebra linear em alta dimensão faz emergir o significado semântico.

## 📝 Tarefas
- [ ] Gerar embeddings para dataset financeiro.
- [ ] Aplicar PCA/t-SNE para redução de dimensionalidade.
- [ ] Validar operações vetoriais semânticas (Analogias).

## ✅ Critérios de Aceite
- Notebook interativo com Plotly.
- Prova de preservação semântica no manifold."

# Task 3
gh issue create \
  --title "[LAB-03] Attention from Scratch: PyTorch Linear Algebra" \
  --milestone "01. LLM Foundations" \
  --label "area: foundations,type: implementation,type: math-heavy" \
  --body "## 🎯 Objetivo
Construir o bloco de Self-Attention (Q, K, V) puro para entender a complexidade quadrática.

## 📝 Tarefas
- [ ] Implementar Scaled Dot-Product Attention em PyTorch.
- [ ] Visualizar Heatmaps das matrizes de atenção.
- [ ] Simular impacto do KV Cache na memória.

## ✅ Critérios de Aceite
- Módulo PyTorch funcional.
- Gráficos de matriz de atenção gerados."

# Task 4
gh issue create \
  --title "[LAB-04] Inference Math: Sampling, Quantization & Loss Analysis" \
  --milestone "01. LLM Foundations" \
  --label "area: foundations,type: implementation" \
  --body "## 🎯 Objetivo
Estudar a matemática por trás da geração e o impacto da quantização na precisão.

## 📝 Tarefas
- [ ] Visualizar logprobs vs Temperatura.
- [ ] Analisar erro de quantização (FP32 -> INT8).
- [ ] Calcular Cost-per-FLOP em diferentes modelos.

## ✅ Critérios de Aceite
- Script de análise de Loss Landscape.
- Comparativo de precisão pós-quantização."

echo "✅ Tudo pronto! Suas tasks estão no GitHub."
