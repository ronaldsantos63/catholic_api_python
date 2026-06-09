# Gemini CLI Instructions

Follow `AGENTS.md` as the canonical project guidance. This file exists so Gemini CLI has an explicit context entry.

## Key Rules

- Preserve the `GET /liturgy` API contract and `period` header format `dd/mm/yyyy`.
- Keep route logic, scraper logic, config, middleware and utilities in their existing modules.
- Run the compileall verification from `AGENTS.md` after Python changes.
- Update `README.md` and `docs/` when behavior changes.
- Avoid live-network tests against Canção Nova unless the user explicitly asks for an integration check.

