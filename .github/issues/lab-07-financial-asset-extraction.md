---
title: "[LAB-07] Production Application: Financial Asset & Proposal Extractor"
labels: ["area: prompt-engineering", "type: implementation"]
assignee: "RogerioLS"
---

## 🎯 Objetivo
Desenvolver uma aplicação de nível de produção para extração, classificação e consolidação de propostas de crédito e balanços patrimoniais corporativos a partir de textos brutos não estruturados.

## 🛠️ Especificação Técnica
1. **Domínio Financeiro:**
   - Extração de Balanço Patrimonial (Ativo Circulante, Passivo, Patrimônio Líquido, EBITDA, Dívida Líquida).
   - Parsing de Propostas de Crédito Bancário (Taxas CET, Prazos, Garantias, Amortização SAC/Price).
2. **Arquitetura de Produção:**
   - Validações contábeis determinísticas pós-extração (e.g. `Ativo == Passivo + PL`).
   - Geração de confidence score para cada campo extraído e sinalização de anomalias contábeis.

## 📝 Tarefas
- [ ] Modelar esquemas Pydantic v2 do domínio contábil/financeiro.
- [ ] Implementar motor de extração em lote com logging de latência e consumo de tokens.
- [ ] Criar validador de consistência contábil matemática independente do LLM.
- [ ] Implementar testes unitários com dados financeiros reais e sintéticos.

## ✅ Critérios de Aceite
- [ ] Módulo sob arquitetura SOLID em `projects/b_prompt_engineering/src/lab_07_financial_extractor/`.
- [ ] Testes unitários com cobertura >= 90% em `projects/b_prompt_engineering/tests/test_financial_extractor.py`.
- [ ] Demonstração de extração com relatórios corporativos.
