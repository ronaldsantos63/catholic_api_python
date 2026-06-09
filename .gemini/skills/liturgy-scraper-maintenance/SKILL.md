---
name: liturgy-scraper-maintenance
description: Use when changing liturgy scraping, Canção Nova request construction, BeautifulSoup parsing, Markdown conversion, date mapping, or reading extraction in extractor files.
---

# Liturgy Scraper Maintenance

Follow `AGENTS.md` as the canonical project contract.

## Workflow

1. Read `docs/ARCHITECTURE.md`, `docs/API.md`, `extractor/extractor_service.py`, `extractor/config.py`, and `extractor/utils.py`.
2. Locate whether the issue is URL discovery, date/query mapping, page download, header parsing, or reading parsing.
3. Preserve output keys in `daily_liturgy_markdown`: `date_string`, `date`, `color`, `entry_title`, and `readings`.
4. Prefer mocked `requests` calls or small HTML fixtures for tests.
5. Update `docs/ARCHITECTURE.md` when source assumptions change.
6. Run the compileall verification from `AGENTS.md` after Python edits.

## Guardrails

- Add network timeouts when introducing new request calls.
- Validate date inputs before broadening accepted formats.
- Avoid live integration checks unless the user asks or the task requires current source verification.

