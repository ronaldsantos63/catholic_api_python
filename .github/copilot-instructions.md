# GitHub Copilot Instructions

Use `AGENTS.md` as the canonical source for repository instructions.

Project summary: this is a small Flask API that scrapes Catholic daily liturgy data from Canção Nova and returns JSON from `GET /liturgy`.

Follow these rules:

- Preserve the public `/liturgy` contract documented in `docs/API.md`.
- Keep scraper changes scoped to `extractor/` unless route behavior must change.
- Do not add dependencies without a clear reason.
- Prefer mocked HTTP responses or HTML fixtures for tests.
- After Python changes, run:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/catholic-api-pycache python3 -m compileall app.py adapter extractor middleware passenger_wsgi.py
```

- Update `README.md`, `docs/`, and `AGENTS.md` when setup, API behavior, architecture, or agent expectations change.

