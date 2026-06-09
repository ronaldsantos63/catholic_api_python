---
name: catholic-api-maintenance
description: Use when changing Flask routes, middleware, logging, WSGI deployment, dependencies, or API behavior in this Catholic API Python repository.
---

# Catholic API Maintenance

Follow `AGENTS.md` as the canonical project contract.

## Workflow

1. Read `AGENTS.md`, `docs/API.md`, and the files touched by the task.
2. Preserve the `/liturgy` public contract unless the user explicitly asks for a breaking change.
3. Keep route definitions in `app.py` and deployment entrypoint behavior in `passenger_wsgi.py`.
4. Update docs when setup, routes, response fields, errors, logging, or deployment behavior changes.
5. Run the compileall verification from `AGENTS.md` after Python edits.

## Guardrails

- Do not expand logging of headers, cookies, tokens, or secrets.
- Do not add authentication, caching, OpenAPI, or database layers unless requested.
- Prefer small changes over framework rewrites.

