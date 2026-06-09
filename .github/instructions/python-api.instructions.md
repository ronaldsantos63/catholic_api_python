---
applyTo: "**/*.py"
---

# Python API Instructions

- Keep Flask route definitions in `app.py`.
- Keep extraction and parsing in `extractor/extractor_service.py`.
- Keep generic date/HTML/Markdown helpers in `extractor/utils.py`.
- Do not make automated tests depend on the live Canção Nova website by default.
- Preserve the `GET /liturgy` JSON fields unless the API docs are updated.

