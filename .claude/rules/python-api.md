---
paths:
  - "*.py"
  - "adapter/**/*.py"
  - "extractor/**/*.py"
  - "middleware/**/*.py"
---

# Python API Rules

- Preserve the Flask route and response contract documented in `AGENTS.md` and `docs/API.md`.
- Keep scraping logic in `extractor/extractor_service.py` and pure helpers in `extractor/utils.py`.
- Prefer mocks or HTML fixtures for tests that touch Canção Nova parsing.
- Run the compileall verification command from `AGENTS.md` after Python changes.

