---
trigger: always_on
---

# Catholic API Python

Use `AGENTS.md` as the canonical repository guidance.

- Preserve `GET /liturgy` and the `period` header format.
- Keep scraping logic in `extractor/`.
- Update `README.md`, `docs/`, and `AGENTS.md` when behavior or commands change.
- Prefer mocked HTTP/HTML fixtures for tests instead of live Canção Nova calls.

