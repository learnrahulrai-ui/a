---
name: financial-pdf-analyzer-development
description: "Develop and test the Financial PDF Analyzer Flask app. Use when: running tests, fixing bugs, deploying to GitHub Pages, configuring Gemini API, setting up devcontainer, adding security features."
argument-hint: "Type your development task (e.g., 'run tests', 'deploy to pages', 'set up Gemini API')"
user-invocable: true
---

# Financial PDF Analyzer Development

A secure Flask application for uploading multiple company financial PDFs and receiving AI-generated analysis via Gemini.

## Project Overview

- **Backend**: Flask server (`app.py`) with PDF validation, CSRF protection, rate limiting, security headers
- **Frontend**: 90s-style retro UI (`templates/index.html`, `static/`)
- **Tests**: 21 passing pytest tests with 85% code coverage (`tests/`)
- **Deployment**: GitHub Pages static preview + Codespaces for full app
- **Security**: Server-side PDF validation, request throttling, secure headers, temporary file storage

## Architecture

```
- app.py                 # Flask backend (PDF upload, Gemini analysis)
- templates/index.html   # Retro 90s UI template
- static/                # CSS & JavaScript assets
- preview/               # GitHub Pages static content
- tests/                 # Complete pytest test suite
- .devcontainer/         # Codespace configuration
- .github/workflows/     # GitHub Actions (Pages deployment)
```

## Getting Started

### Local Development

[Setup Guide](./references/local-setup.md) — Install dependencies, configure environment variables, run the Flask server.

### Running Tests

```bash
pytest tests/ -v --cov=app
```

All 21 tests passing; 85% code coverage.

## Common Tasks

### 1. Run the Flask App Locally

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
export FLASK_SECRET_KEY="your-long-random-secret"
export GEMINI_API_KEY="your-gemini-api-key"
python app.py
```

Open: `http://localhost:8000`

### 2. Run Test Suite

```bash
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```

- 21 tests: routes, security headers, CSRF, rate limiting, PDF validation
- Coverage: 85% of app logic

### 3. Deploy to GitHub Pages

```bash
git add .
git commit -m "Ready for Pages deployment"
git push origin HEAD:main
```

Site publishes to: `https://<username>.github.io/<repo-name>/`

The `preview/index.html` static page explains that full functionality requires running in Codespaces.

### 4. Set Up Gemini API

[Gemini Integration Guide](./references/gemini-setup.md) — Obtain API key, configure environment variable, handle errors gracefully.

### 5. Use GitHub Codespaces

1. Click **Code → Codespaces → Create codespace on branch**
2. Codespace auto-installs dependencies via `.devcontainer/devcontainer.json`
3. Set environment variables and run `python app.py`
4. Open forwarded port 8000

## Security Features

✅ **PDF Validation**
- File extension check (`.pdf` only)
- Magic-byte signature check (`%PDF-` header)
- Per-file size limit (15 MB)
- Max file count (40 files)

✅ **Request Security**
- CSRF token per session
- Rate limiting (20 requests/60 sec per IP)
- Strict Content-Security-Policy header
- X-Frame-Options: DENY

✅ **File Handling**
- Safe filename sanitization via `secure_filename()`
- Temporary directory storage (auto-deleted)
- No persistent file retention

## Key Functions

| Function | Purpose |
|----------|---------|
| `looks_like_pdf()` | Validates PDF magic bytes |
| `extract_pdf_text()` | Extracts text using pypdf for AI analysis |
| `enforce_rate_limit()` | Throttles requests per IP |
| `analyze_with_gemini()` | Calls Gemini API for financial analysis |

## Configuration

| Variable | Required | Purpose |
|----------|----------|---------|
| `FLASK_SECRET_KEY` | Yes | Session encryption key (30+ chars recommended) |
| `GEMINI_API_KEY` | No | Google Gemini API key for analysis (optional) |
| `FLASK_ENV` | No | Set to `production` for deployment |

## Testing

[Testing Guide](./references/testing.md) — Unit tests, integration tests, mocking Gemini calls, interpreting coverage reports.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pages site not deploying | Push to `main` branch; check `.github/workflows/pages.yml` |
| Tests failing | Run `pytest tests/ -v --tb=long` for detailed output |
| CSRF token errors | Ensure session is enabled; reload page to get fresh token |
| Rate limit errors | Adjust `RATE_LIMIT_MAX_REQUESTS` in `app.py` |

## References

- [Local Setup & Environment](./references/local-setup.md)
- [Gemini API Integration](./references/gemini-setup.md)
- [Testing & Coverage](./references/testing.md)
- [Deployment to GitHub Pages](./references/pages-deployment.md)
- [Security Hardening](./references/security.md)
