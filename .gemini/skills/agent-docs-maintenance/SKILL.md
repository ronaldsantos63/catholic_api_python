---
name: agent-docs-maintenance
description: Use when creating or updating AI-agent instructions, AGENTS.md, REVIEW.md, CLAUDE.md, GEMINI.md, Copilot instructions, Cursor rules, Windsurf or Devin rules, Claude skills, Gemini skills, or Codex skills for this repository.
---

# Agent Docs Maintenance

## Workflow

1. Treat `AGENTS.md` as the canonical agent contract.
2. Keep `README.md` human-facing and detailed docs in `docs/`.
3. Keep tool-specific files short and aligned with `AGENTS.md`.
4. Keep `.agents/skills`, `.claude/skills`, and `.gemini/skills` aligned when skill behavior changes.
5. Use `.agents/skills` as the shared Codex and GitHub Copilot project skill root; avoid duplicate `.github/skills` copies unless Copilot needs isolated behavior.
6. Avoid contradictory instructions across agent files.

## Files to Check

- `AGENTS.md`
- `REVIEW.md`
- `CLAUDE.md`
- `.claude/rules/`
- `.claude/skills/`
- `GEMINI.md`
- `.gemini/settings.json`
- `.gemini/skills/`
- `.github/copilot-instructions.md`
- `.github/instructions/`
- `.github/skills/` only if Copilot needs isolated skills not shared through `.agents/skills/`
- `.cursor/rules/`
- `.devin/rules/`
- `.windsurf/rules/`
- `.agents/skills/`
- `docs/AI_AGENTS.md`
