#!/bin/bash
# Setup Milestone, Labels, and GitHub Issues for Phase 2: Prompt Engineering
set -e

REPO="${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "RogerioLS/production-ai-systems")}"

echo "🎯 Sincronizando Milestone no repositório: $REPO..."
MILESTONE_TITLE="02. Prompt Engineering & Structured Outputs"
EXISTING_MILESTONE=$(gh api "repos/$REPO/milestones" --jq ".[] | select(.title==\"$MILESTONE_TITLE\") | .number" 2>/dev/null || true)

if [ -z "$EXISTING_MILESTONE" ]; then
  gh api "repos/$REPO/milestones" \
    -f title="$MILESTONE_TITLE" \
    -f description="Raciocínio avançado (CoT, ReAct), Schemas Pydantic v2, extração e Spec-Driven Development." >/dev/null || true
  echo "✔ Milestone criada com sucesso!"
else
  echo "✔ Milestone já existente (#$EXISTING_MILESTONE)."
fi

echo "🏷️ Sincronizando Labels..."
gh label create "area: prompt-engineering" --color "8e44ad" --description "Engenharia de Prompt e Saídas Estruturadas" --force 2>/dev/null || true
gh label create "type: structured-outputs" --color "16a085" --description "Schemas Pydantic, Instructor e Guardrails" --force 2>/dev/null || true
gh label create "type: reasoning" --color "f39c12" --description "Padrões de Raciocínio (Few-Shot, CoT, ReAct)" --force 2>/dev/null || true

create_task_if_not_exists() {
  local title="$1"
  local labels="$2"
  local body_file="$3"
  local task_id="$4"

  # Verifica se já existe uma issue aberta ou fechada com este task_id no título
  local exists=$(gh issue list --repo "$REPO" --state all --search "$task_id in:title" --json number --jq '.[0].number' 2>/dev/null || true)
  if [ -n "$exists" ]; then
    echo "✔ Task $task_id já existe como Issue #$exists. Pulando criação."
  else
    echo "➕ Criando Issue: $title..."
    gh issue create \
      --repo "$REPO" \
      --title "$title" \
      --milestone "$MILESTONE_TITLE" \
      --label "$labels" \
      --body-file "$body_file"
  fi
}

echo "🚀 Populando o Kanban com as tasks do Módulo 02..."

create_task_if_not_exists \
  "[LAB-05] Prompt Reasoning Patterns: Few-Shot, CoT, Self-Consistency & ReAct" \
  "area: prompt-engineering,type: implementation,type: reasoning" \
  ".github/issues/lab-05-reasoning-patterns.md" \
  "LAB-05"

create_task_if_not_exists \
  "[LAB-06] Structured Outputs: Pydantic v2, Instructor & Schema Enforcement" \
  "area: prompt-engineering,type: implementation,type: structured-outputs" \
  ".github/issues/lab-06-structured-outputs.md" \
  "LAB-06"

create_task_if_not_exists \
  "[LAB-07] Production Application: Financial Asset & Proposal Extractor" \
  "area: prompt-engineering,type: implementation" \
  ".github/issues/lab-07-financial-asset-extraction.md" \
  "LAB-07"

create_task_if_not_exists \
  "[LAB-08] Spec-Driven Development: OpenSpec & Contract Compliance" \
  "area: prompt-engineering,type: implementation,type: research" \
  ".github/issues/lab-08-spec-driven-development.md" \
  "LAB-08"

echo "✅ Sincronização do Kanban para o Módulo 02 concluída com sucesso!"
