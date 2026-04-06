# Financial PDF Analyzer (90s-style web app)

A retro-style website that lets a user upload **many company financial PDFs** and receive an **AI-generated analysis** using **Gemini API keys** that you provide.

## Features

- 90s desktop UI style (single-page web experience)
- Multi-file PDF upload for company financial documents
- Server-side validation:
  - PDF extension check
  - PDF magic-byte signature check
  - per-file size limit
  - max file count
- Security hardening:
  - CSRF token for POST requests
  - strict response security headers (CSP, X-Frame-Options, etc.)
  - request rate limiting
  - safe filename handling
  - temporary storage only (no persistent PDF retention)
- Gemini analysis via `GEMINI_API_KEY`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY="replace-with-long-random-secret"
export GEMINI_API_KEY="your-gemini-key"
python app.py
```

Open: `http://localhost:8000`

## Important security notes

- Keep `FLASK_SECRET_KEY` and `GEMINI_API_KEY` in environment variables only.
- Put this app behind HTTPS in production.
- Add an auth layer (SSO/OAuth) before public deployment.
- Consider malware scanning for uploaded files in production.


## Deploy so you can see it on the web

### Option A (full app): GitHub Codespaces ✅

GitHub Codespaces can run this Flask backend and show the real upload + AI analysis flow.

1. Push this repo to GitHub.
2. Click **Code → Codespaces → Create codespace on branch**.
3. Codespace auto-installs dependencies via `.devcontainer/devcontainer.json`.
4. In Codespaces terminal:
   ```bash
   export FLASK_SECRET_KEY="replace-with-long-random-secret"
   export GEMINI_API_KEY="your-gemini-key"
   python app.py
   ```
5. Open forwarded port `8000` in browser.

### Option B (static preview): GitHub Pages ⚠️

GitHub Pages is static-only, so it cannot run Flask or process PDF uploads server-side.

- This repo includes a Pages workflow that publishes `preview/` as a public preview page.
- Use it for a quick visual preview, then use Codespaces for real functionality.

After pushing:
1. Go to **Settings → Pages** and ensure **GitHub Actions** is selected as source.
2. Push to `main`/`master` (or run workflow manually).
3. Open your published Pages URL.
