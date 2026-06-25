---
name: documentation_sync
description: Syncs and updates project progress across README.md, docs/PROGRESS.md, mkdocs config, and project-specific notes.
---

# Documentation Sync & Progress Manager

You are responsible for keeping all project documentation, status tracking, and notes perfectly synchronized.

Whenever a lab or project task is started, updated, or completed, you must:

## 1. Update Project TODOs
Update the task checklist in the project's `TODO.md` file (e.g., `projects/01_llm_basics/TODO.md`).

## 2. Sync Repository Progress
Update the main `docs/PROGRESS.md` to reflect completed phases (`[x]`), active phases (`[/]`), or pending phases (`[ ]`).
Also update the `README.md` progress status indicators if necessary.

## 3. Keep MKDocs Updated
If new note pages or lab documentation files are created under `docs/` or `projects/`, verify that they are linked correctly in `mkdocs.yml` navigation so they compile properly when mkdocs is built.

## 4. Technical Reflection and Notes
Ensure that the notes file for the current module (e.g., `docs/notes/01_foundations.md`) is filled with:
- Academic references/papers used for the solution.
- Rationale behind implementation choices.
- Brief benchmark/experiment results.
- Code blocks showing standard usage.
