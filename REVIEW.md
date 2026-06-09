# Review Guidelines

Use these checks when reviewing pull requests in this repository.

## Critical Areas

- Treat regressions in `GET /liturgy` as high priority.
- Treat leaks of headers, cookies, tokens, or personal data in logs as high priority.
- Treat unvalidated user input in new routes or scraper parameters as high priority.
- Treat new network calls without timeouts as high priority.
- Treat changes that bypass rate limiting, API key checks, or security headers as high priority.

## API Contract

- Preserve the optional `period` header format: `dd/mm/yyyy`.
- Preserve response fields: `date_string`, `date`, `color`, `entry_title`, and `readings`.
- Require documentation updates in `docs/API.md` for any public behavior change.

## Scraper Changes

- Check that source HTML assumptions are documented in `docs/ARCHITECTURE.md`.
- Prefer mocked HTTP responses or HTML fixtures over live Canção Nova calls in automated tests.
- Watch for brittle paragraph-index parsing and missing-section errors.

## Dependencies

- Flag new dependencies that are not necessary for the requested change.
- Check that `requirements.txt` remains installable.
