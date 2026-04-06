import os
import secrets
import tempfile
import time
from collections import defaultdict, deque
from pathlib import Path

import requests
from flask import Flask, abort, jsonify, render_template, request, session
from werkzeug.utils import secure_filename

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - fallback if dependency missing
    PdfReader = None


MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB per file
MAX_FILES = 40
ALLOWED_EXTENSION = {".pdf"}
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 20


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE * MAX_FILES

request_tracker = defaultdict(deque)


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "script-src 'self'; "
        "img-src 'self'; "
        "base-uri 'none'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


def enforce_rate_limit(client_ip: str) -> None:
    now = time.time()
    bucket = request_tracker[client_ip]

    while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
        bucket.popleft()

    if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
        abort(429, description="Too many requests. Please wait a minute and try again.")

    bucket.append(now)


@app.before_request
def before_request_checks():
    enforce_rate_limit(request.headers.get("X-Forwarded-For", request.remote_addr or "unknown"))

    if request.method == "POST":
        csrf_token = session.get("csrf_token")
        submitted_token = request.form.get("csrf_token")
        if not csrf_token or not submitted_token or not secrets.compare_digest(csrf_token, submitted_token):
            abort(400, description="Invalid CSRF token.")


@app.get("/")
def index():
    session["csrf_token"] = secrets.token_urlsafe(32)
    return render_template("index.html", csrf_token=session["csrf_token"])


def looks_like_pdf(file_path: Path) -> bool:
    with file_path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def extract_pdf_text(file_path: Path, max_chars: int = 12_000) -> str:
    if PdfReader is None:
        return ""

    try:
        reader = PdfReader(str(file_path))
        chunks = []
        for page in reader.pages:
            chunks.append(page.extract_text() or "")
            if sum(len(c) for c in chunks) > max_chars:
                break
        return "\n".join(chunks)[:max_chars]
    except Exception:
        return ""


def analyze_with_gemini(company_name: str, files_summary: list[dict]) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Analysis skipped: GEMINI_API_KEY is not configured on the server."

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    prompt = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a financial analyst assistant. "
                            f"Review uploaded PDF data for company: {company_name}. "
                            "Give a concise report with: 1) file completeness observation, "
                            "2) potential risks, 3) revenue/profit trends if present, "
                            "4) confidence level and caveats.\n\n"
                            f"Data:\n{files_summary}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 900},
    }

    try:
        response = requests.post(endpoint, json=prompt, timeout=35)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as exc:
        return f"Analysis failed safely. Error: {type(exc).__name__}"


@app.post("/analyze")
def analyze():
    company_name = request.form.get("company_name", "").strip()
    uploads = request.files.getlist("financial_pdfs")

    if not company_name:
        abort(400, description="Company name is required.")

    if not uploads or not uploads[0].filename:
        abort(400, description="At least one PDF is required.")

    if len(uploads) > MAX_FILES:
        abort(400, description=f"Too many files. Max allowed is {MAX_FILES}.")

    files_summary = []

    with tempfile.TemporaryDirectory(prefix="financial_upload_") as temp_dir:
        temp_path = Path(temp_dir)

        for uploaded in uploads:
            cleaned_name = secure_filename(uploaded.filename or "")
            suffix = Path(cleaned_name).suffix.lower()
            if not cleaned_name or suffix not in ALLOWED_EXTENSION:
                abort(400, description="Only PDF files are allowed.")

            destination = temp_path / cleaned_name
            uploaded.save(destination)

            if destination.stat().st_size > MAX_FILE_SIZE:
                abort(400, description=f"{cleaned_name} exceeds 15 MB limit.")

            if not looks_like_pdf(destination):
                abort(400, description=f"{cleaned_name} does not appear to be a valid PDF.")

            snippet = extract_pdf_text(destination)
            files_summary.append(
                {
                    "filename": cleaned_name,
                    "size_bytes": destination.stat().st_size,
                    "text_snippet": snippet[:1200],
                    "has_extractable_text": bool(snippet.strip()),
                }
            )

    analysis = analyze_with_gemini(company_name=company_name, files_summary=files_summary)

    return jsonify(
        {
            "company": company_name,
            "uploaded_count": len(files_summary),
            "message": (
                f"Received {len(files_summary)} financial PDFs for {company_name}. "
                "AI analysis completed."
            ),
            "analysis": analysis,
        }
    )


@app.errorhandler(400)
def handle_bad_request(err):
    return jsonify({"description": getattr(err, "description", "Bad request")}), 400


@app.errorhandler(413)
def handle_too_large(_err):
    return jsonify({"description": "Upload too large. Reduce number/size of PDF files."}), 413


@app.errorhandler(429)
def handle_rate_limit(err):
    return jsonify({"description": getattr(err, "description", "Rate limit exceeded")}), 429



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
