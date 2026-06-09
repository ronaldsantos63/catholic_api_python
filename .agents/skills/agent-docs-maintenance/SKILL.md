---
name: agent-docs-maintenance
description: Use when creating or updating AI-agent instructions, AGENTS.md, REVIEW.md, CLAUDE.md, GEMINI.md, Copilot instructions, Cursor rules, Windsurf or Devin rules, Claude skills, Gemini skills, or Codex skills for this repository.
---

# Agent Docs Maintenance

## Workflow

1. Treat `AGENTS.md` as the canonical agent contract.
2. Keep `README.md` human-facing and detailed docs in `docs/`.
3. Keep tool-specific files short and aligned with `AGENTS.md`.
4. Use imports or references when a tool supports them; otherwise include only a concise summary.
5. For Codex and GitHub Copilot project skills, place repo-scoped skills under `.agents/skills/<skill-name>/SKILL.md`.
6. For Claude Code, mirror project skills under `.claude/skills/<skill-name>/SKILL.md`.
7. For Gemini CLI, mirror workspace skills under `.gemini/skills/<skill-name>/SKILL.md`.
8. Validate skills with the skill-creator quick validator when skill files change if `PyYAML` is available; otherwise validate frontmatter with another YAML parser.

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

## Guardrails

- Avoid contradictory instructions across agent files.
- Keep long explanations out of always-loaded files.
- Update docs when commands, architecture, API contract, or verification steps change.
- Do not create extra files inside skill directories beyond `SKILL.md`, `agents/openai.yaml`, and purposeful resources.
