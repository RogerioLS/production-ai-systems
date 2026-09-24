---
title: "[LAB-06] Structured Outputs: Pydantic v2, Instructor & Schema Enforcement"
labels: ["area: prompt-engineering", "type: implementation"]
assignee: "RogerioLS"
---

## 🎯 Objetivo
Construir um pipeline industrial de extração de dados estruturados com garantia estrita de esquema (schema enforcement), validação em runtime via Pydantic v2, integração com Instructor/OpenAI JSON mode e resiliência a alucinações de formato.

## 🛠️ Especificação Técnica
1. **Engenharia de Schemas Estruturados:**
   - Modelos Pydantic v2 avançados com `Field(..., description=...)`, validadores customizados (`@field_validator`) e tipos aninhados.
   - Suporte a saídas em JSON Schema estrito e XML tags delimitadas.
2. **Estratégias de Encalhamento e Reparo:**
   - Loop de auto-correção (*Self-Healing / Reflection*): re-injeção do erro de validação do Pydantic no prompt para regeneração corretiva.
   - Parsing tolerante a Markdown blocks (````json ... ````) e trailing commas.

## 📝 Tarefas
- [ ] Criar esquemas Pydantic v2 para extração de entidades financeiras e contratos.
- [ ] Implementar extrator com OpenAI Function/Tool Calling e Instructor.
- [ ] Desenvolver mecanismo de *Self-Healing* que detecta falhas de validação e re-alimenta o LLM com o traceback de validação.
- [ ] Comparar confiabilidade e taxa de erro sintático (JSON puro vs XML Prompting vs Structured Outputs nativos).
- [ ] Escrever suíte de testes com cenários adversos (campos ausentes, tipos incorretos, JSON truncado).

## ✅ Critérios de Aceite
- [ ] Módulo sob arquitetura SOLID em `projects/b_prompt_engineering/src/lab_06_structured_outputs/`.
- [ ] Testes unitários com cobertura >= 90% em `projects/b_prompt_engineering/tests/test_structured_outputs.py`.
- [ ] Playground interativo demonstrando auto-reparo e validação de contratos.
