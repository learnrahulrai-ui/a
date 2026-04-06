# Testing & Coverage Guide

## Running Tests

### Basic Test Run

```bash
pytest tests/ -v
```

Output shows each test with `PASSED` or `FAILED`.

### With Coverage Report

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Shows:
- Lines of app.py with no test coverage
- Overall coverage percentage
- Missing line numbers

### Example Output

```
tests/test_app.py::TestIndexRoute::test_index_returns_200 PASSED
tests/test_app.py::TestAnalyzeRoute::test_analyze_missing_company_name PASSED
...

---------- coverage: platform linux, python 3.12.13-final-0 ----------
Name     Stmts   Miss  Cover   Missing
--------------------------------------
app.py     116     17    85%    55, 87, 95, 106-137, 152, 169, 206, 211, 216
--------------------------------------
TOTAL      116     17    85%
```

## Test Structure

```
tests/
├── conftest.py           # Fixtures (test app, client, temp files)
├── test_app.py           # Route & security tests
└── test_functions.py     # Unit tests for helper functions
```

### Test Categories

| File | Count | Coverage |
|------|-------|----------|
| Route tests (GET `/`, POST `/analyze`) | 7 | Index, form submission, validation |
| Security tests (headers, CSRF, rate limit) | 7 | CSP, X-Frame-Options, rate throttling |
| PDF validation tests | 3 | Magic bytes, file extension, size |
| Error handling tests | 2 | 400, 404 responses |
| Utility function tests | 2 | PDF text extraction |

## Key Test Fixtures

### `@pytest.fixture: client`
Flask test client for making requests.

```python
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
```

### `@pytest.fixture: temp_pdf_file`
Creates a valid PDF file (with `%PDF-` header) for testing.

```python
def test_pdf_validation(client, temp_pdf_file):
    with open(temp_pdf_file, "rb") as f:
        # test code
```

### `@pytest.fixture: invalid_pdf_file`
Creates a fake PDF (non-PDF content) for negative testing.

## Understanding Coverage Gaps

Current **missing coverage** (line numbers like `55, 87, 95`):

- Error handling in `analyze_with_gemini()` — requires mocking external API
- Some exception branches in PDF extraction
- Edge cases in rate limiting cleanup

## Improving Coverage

To reach 95%+ coverage:

1. **Mock Gemini API responses**:
   ```python
   from unittest.mock import patch
   
   @patch("requests.post")
   def test_gemini_api(mock_post, client):
       mock_post.return_value.json.return_value = {"candidates": [...]}
       # test code
   ```

2. **Test file size limits**:
   ```python
   def test_file_exceeds_max_size(client):
       # Create a file > 15 MB
       # Upload and verify 400 error
   ```

3. **Test missing Gemini API key**:
   ```python
   @patch.dict(os.environ, {"GEMINI_API_KEY": ""})
   def test_no_gemini_key(client):
       # Verify graceful fallback
   ```

## Running Specific Tests

```bash
# Run single test class
pytest tests/test_app.py::TestSecurityHeaders -v

# Run single test
pytest tests/test_app.py::TestSecurityHeaders::test_csp_header_content -v

# Run tests matching a pattern
pytest tests/ -k "csrf" -v
```

## Continuous Integration

GitHub Actions runs tests on every push to `main`. See `.github/workflows/` (if added).

To manually trigger CI:
```bash
git push origin main
```

Then check the **Actions** tab on GitHub.
