---
name: catholic-api-maintenance
description: Use when changing Flask routes, middleware, logging, WSGI deployment, dependencies, or API behavior in this Catholic API Python repository. Do not use for pure scraper-only changes unless route behavior changes.
---

# Catholic API Maintenance

## Workflow

1. Read `AGENTS.md`, `docs/API.md`, and the files touched by the task.
2. Identify whether the change affects public HTTP behavior, internal wiring, logging, or deployment.
3. Keep route definitions in `app.py` and WSGI entrypoint behavior in `passenger_wsgi.py`.
4. Preserve the `/liturgy` contract unless the user explicitly asks for a breaking change.
5. Update docs when setup, routes, response fields, errors, logging, or deployment behavior changes.
6. Run the compileall verification from `AGENTS.md` after Python edits.

## Guardrails

- Do not expand logging of request headers, cookies, tokens, or user-provided secrets.
- Do not add authentication, caching, OpenAPI, or database layers unless requested.
- Prefer small changes over framework rewrites.
- If adding dependencies, update `requirements.txt` and document why.

## Expected Outputs

- Code changes scoped to Flask/API concerns.
- Documentation updates for public behavior.
- Verification result or a clear note if verification could not run.

