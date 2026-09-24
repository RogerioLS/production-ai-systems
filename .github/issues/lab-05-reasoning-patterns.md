---
title: "[LAB-05] Prompt Reasoning Patterns: Few-Shot, CoT, Self-Consistency & ReAct"
labels: ["area: prompt-engineering", "type: implementation", "type: research"]
assignee: "RogerioLS"
---

## 🎯 Objetivo
Implementar e avaliar empiricamente os principais padrões cognitivos de prompting (Zero-Shot, Few-Shot In-Context Learning, Chain-of-Thought, Self-Consistency com Majority Voting e ReAct), mensurando ganhos de acurácia, dispersão de raciocínio, consumo de tokens e latência.

## 🛠️ Especificação Técnica
1. **Padrões de Raciocínio (OOP & SOLID):**
   - `FewShotEngine`: Seleção dinâmica de demonstradores com formatação parametrizável.
   - `ChainOfThoughtEngine`: Indução de passos dedutivos passo-a-passo.
   - `SelfConsistencyEngine`: Amostragem estocástica com votação por maioria (*Majority Voting*) e cálculo de entropia/consenso.
   - `ReActEngine`: Ciclo cognitivo autônomo `Thought -> Action -> Observation -> Final Answer`.
2. **Benchmark Comparativo:**
   - Avaliação sistemática de acurácia em problemas complexos (matemática, lógica simbólica e finanças).
   - Medição de custo (tokens) vs taxa de acerto.

## 📝 Tarefas
- [ ] Implementar `PromptTemplate` modular e tipado com interpolação segura.
- [ ] Implementar `FewShotPrompt` com suporte a seleção estática e dinâmica de exemplos.
- [ ] Implementar `ChainOfThought` com raciocínio intermediário estruturado.
- [ ] Implementar `SelfConsistency` com amostragem múltipla e consolidação por consenso estatístico.
- [ ] Implementar `ReActLoop` com execução de ferramentas simuladas (calculator, stock-lookup).
- [ ] Desenvolver suíte completa de testes com `pytest` e structured logging com `loguru`.

## ✅ Critérios de Aceite
- [ ] Módulo sob arquitetura SOLID em `projects/b_prompt_engineering/src/lab_05_reasoning/`.
- [ ] Testes unitários com cobertura >= 90% em `projects/b_prompt_engineering/tests/test_reasoning.py`.
- [ ] Notebook interativo e documentação completa com gráficos de dispersão e custo.
