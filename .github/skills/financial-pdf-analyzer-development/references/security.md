# Security Hardening

This document explains the security features built into the Financial PDF Analyzer.

## Server-Side Security

### 1. PDF File Validation

**What**: Validates that uploaded files are legitimate PDFs before processing.

**How**:
- **Extension check**: Only `.pdf` files allowed
- **Magic-byte check**: File must start with `%PDF-` (5-byte signature)
- **Size limit**: Max 15 MB per file
- **File count limit**: Max 40 files per request

**Implementation** (`app.py`):
```python
def looks_like_pdf(file_path: Path) -> bool:
    with file_path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"

if not looks_like_pdf(destination):
    abort(400, description="does not appear to be a valid PDF.")
```

### 2. CSRF Token Protection

**What**: Prevents Cross-Site Request Forgery attacks.

**How**:
- Session generates unique CSRF token per user
- Token embedded in form (hidden input)
- Token validated on every POST request
- Token compared using `secrets.compare_digest()` (constant-time)

**Implementation**:
```python
@app.before_request
def before_request_checks():
    if request.method == "POST":
        csrf_token = session.get("csrf_token")
        submitted_token = request.form.get("csrf_token")
        if not secrets.compare_digest(csrf_token, submitted_token):
            abort(400, description="Invalid CSRF token.")
```

### 3. Rate Limiting

**What**: Throttles requests to prevent brute-force and DoS attacks.

**How**:
- 20 requests per 60-second window per IP address
- Sliding window using deque (oldest requests pruned)
- Per-IP tracking (X-Forwarded-For fallback)

**Configuration**:
```python
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 20
```

**Error Response** (429):
```
"Too many requests. Please wait a minute and try again."
```

### 4. Security Headers

**What**: HTTP headers that instruct browsers to enforce security policies.

**Implemented Headers**:

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Content-Type-Options` | `nosniff` | Prevent MIME type sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `Referrer-Policy` | `same-origin` | Don't leak referrer to external sites |
| `Content-Security-Policy` | `default-src 'self'...` | Restrict resource loading |
| `Permissions-Policy` | `geolocation=()...` | Disable dangerous APIs |

**CSP Details**:
```
default-src 'self'          # Only same-origin resources
style-src 'self'            # Stylesheets from self only
script-src 'self'           # JavaScript from self only
base-uri 'none'             # No <base> tag allowed
form-action 'self'          # Forms submit to same-origin
frame-ancestors 'none'      # Cannot be framed
```

### 5. Secure Filename Handling

**What**: Sanitizes uploaded filenames to prevent path traversal.

**How**:
```python
from werkzeug.utils import secure_filename

cleaned_name = secure_filename(uploaded.filename)
```

**Protection**:
- Removes path components (`../`, `../../`)
- Removes special characters
- Prevents directory traversal attacks

### 6. Temporary File Storage

**What**: PDFs are never permanently stored; cleaned up automatically.

**How**:
```python
with tempfile.TemporaryDirectory(prefix="financial_upload_") as temp_dir:
    # Process files here
    # Files auto-deleted when exiting context
```

**Benefit**: Reduces data breach risk; complies with privacy requirements.

## Environment Security

### 1. Secret Management

**Critical variables** (never commit):
- `FLASK_SECRET_KEY` — Session encryption (30+ chars recommended)
- `GEMINI_API_KEY` — Google API credentials

**Best practices**:
```bash
# ✅ Good: Use .env or secrets manager
export FLASK_SECRET_KEY="$(openssl rand -hex 32)"
export GEMINI_API_KEY="sk-proj-..."

# ❌ Bad: Hardcoded in code
SECRET_KEY = "my-secret"  # DO NOT DO THIS
```

### 2. Production Deployment

**Before going live**:
- [ ] Add authentication (SSO/OAuth) layer
- [ ] Enable HTTPS (TLS 1.2+)
- [ ] Use secret manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] Implement file virus scanning
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode (`debug=False`)
- [ ] Add request timeout enforcement
- [ ] Monitor API quotas and errors

## Common Vulnerabilities

### Prevented

- ✅ **SQL Injection**: No database; no SQL queries
- ✅ **Path Traversal**: `secure_filename()` sanitizes paths
- ✅ **CSRF**: CSRF token validation on all POST
- ✅ **Clickjacking**: `X-Frame-Options: DENY`
- ✅ **MIME Sniffing**: `X-Content-Type-Options: nosniff`

### Requires Additional Measures

- ⚠️ **Malware Upload**: Implement antivirus scanning (ClamAV, VirusTotal API)
- ⚠️ **Unauthed Access**: Add authentication layer before production
- ⚠️ **Data Exfiltration**: Encrypt PDFs in transit (TLS) and at rest

## Testing Security

### Run Tests

```bash
pytest tests/ -v --cov=app
```

**Security test categories**:
- `TestSecurityHeaders` — Verifies all headers present
- `TestCSRFProtection` — Tests CSRF token validation
- `TestAnalyzeRoute` — Tests file and input validation

### Manual Testing

1. **CSRF**: Disable CSRF token in form; expect 400 error
2. **Rate limit**: Hammer `/analyze` endpoint 21+ times; expect 429 on 21st
3. **File size**: Upload 16+ MB file; expect 400 error
4. **Non-PDF**: Upload `.txt` file with `.pdf` extension; expect 400 error

## Compliance Notes

This app is designed with the following in mind:

- **GDPR**: Temporary storage, no data retention
- **CCPA**: User can download their analysis
- **PCI DSS**: No payment card data handling
- **HIPAA**: Not suitable for healthcare data without encryption

---

**For more**: [OWASP Top 10](https://cheatsheetseries.owasp.org/)
