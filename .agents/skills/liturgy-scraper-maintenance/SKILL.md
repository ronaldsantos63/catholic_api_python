---
name: liturgy-scraper-maintenance
description: Use when changing liturgy scraping, Canção Nova request construction, BeautifulSoup parsing, Markdown conversion, date mapping, or reading extraction in extractor files.
---

# Liturgy Scraper Maintenance

## Workflow

1. Read `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/API.md`, `extractor/extractor_service.py`, `extractor/config.py`, and `extractor/utils.py`.
2. Locate whether the issue is URL discovery, date/query mapping, page download, header parsing, or reading parsing.
3. Keep external-source assumptions explicit in `docs/ARCHITECTURE.md` when they change.
4. Preserve output keys in `daily_liturgy_markdown`: `date_string`, `date`, `color`, `entry_title`, and `readings`.
5. Prefer mocked `requests` calls or small HTML fixtures for tests.
6. Run the compileall verification from `AGENTS.md` after Python edits.

## Source Assumptions

- Calendar discovery posts to `/wp-admin/admin-ajax.php`.
- Liturgy pages currently expose header fields such as `dia-calendar`, `mes-calendar`, `ano-calendar`, `cor-liturgica`, and `entry-title`.
- Reading sections currently use IDs `liturgia-1` through `liturgia-4`.

## Guardrails

- Add network timeouts when introducing new request calls.
- Validate date inputs before broadening accepted formats.
- Avoid live integration checks unless the user asks or the task requires current source verification.
- Do not silently remove missing readings; keep behavior predictable and document changes.

