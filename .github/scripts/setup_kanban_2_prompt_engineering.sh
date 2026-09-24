#!/bin/bash
# Setup Milestone, Labels, and GitHub Issues for Phase 2: Prompt Engineering
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "RogerioLS/production-ai-systems")

echo "🎯 Criando Milestone: 02. Prompt Engineering & Structured Outputs no repo $REPO..."
gh api repos/$REPO/milestones -f title="02. Prompt Engineering & Structured Outputs" -f description="Raciocínio avançado (CoT, ReAct), Schemas Pydantic v2, extração e Spec-Driven Development." 2>/dev/null || echo "ℹ️ Milestone já existe ou gh api indisponível"

echo "🏷️ Criando Labels..."
gh label create "area: prompt-engineering" --color "8e44ad" --description "Engenharia de Prompt e Saídas Estruturadas" --force 2>/dev/null || true
gh label create "type: structured-outputs" --color "16a085" --description "Schemas Pydantic, Instructor e Guardrails" --force 2>/dev/null || true
gh label create "type: reasoning" --color "f39c12" --description "Padrões de Raciocínio (Few-Shot, CoT, ReAct)" --force 2>/dev/null || true

echo "🚀 Populando o Kanban com as tasks do Módulo 02..."

gh issue create \
  --title "[LAB-05] Prompt Reasoning Patterns: Few-Shot, CoT, Self-Consistency & ReAct" \
  --milestone "02. Prompt Engineering & Structured Outputs" \
  --label "area: prompt-engineering,type: implementation,type: reasoning" \
  --body-file ".github/issues/lab-05-reasoning-patterns.md" 2>/dev/null || echo "ℹ️ Use gh auth login para sincronizar online com o GitHub"

gh issue create \
  --title "[LAB-06] Structured Outputs: Pydantic v2, Instructor & Schema Enforcement" \
  --milestone "02. Prompt Engineering & Structured Outputs" \
  --label "area: prompt-engineering,type: implementation,type: structured-outputs" \
  --body-file ".github/issues/lab-06-structured-outputs.md" 2>/dev/null || true

gh issue create \
  --title "[LAB-07] Production Application: Financial Asset & Proposal Extractor" \
  --milestone "02. Prompt Engineering & Structured Outputs" \
  --label "area: prompt-engineering,type: implementation" \
  --body-file ".github/issues/lab-07-financial-asset-extraction.md" 2>/dev/null || true

gh issue create \
  --title "[LAB-08] Spec-Driven Development: OpenSpec & Contract Compliance" \
  --milestone "02. Prompt Engineering & Structured Outputs" \
  --label "area: prompt-engineering,type: implementation,type: research" \
  --body-file ".github/issues/lab-08-spec-driven-development.md" 2>/dev/null || true

echo "✅ Script de setup do Kanban para o Módulo 02 concluído!"
