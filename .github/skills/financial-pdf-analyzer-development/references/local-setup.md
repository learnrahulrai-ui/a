# Local Setup & Environment Configuration

## Prerequisites

- Python 3.10 or later
- Git
- Virtual environment tool (`venv`, `virtualenv`, or `conda`)

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/learnrahulrai-ui/a.git
cd a
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Flask==3.1.1` — Web framework
- `requests==2.32.3` — HTTP client for Gemini API
- `pypdf==5.4.0` — PDF text extraction
- `pytest==7.4.4` — Test framework
- `pytest-cov==4.1.0` — Coverage reporting

### 4. Set Environment Variables

```bash
export FLASK_SECRET_KEY="your-very-long-random-secret-at-least-30-chars"
export GEMINI_API_KEY="your-gemini-api-key"  # Optional; analysis skips if missing
```

On Windows (PowerShell):

```powershell
$env:FLASK_SECRET_KEY = "your-secret"
$env:GEMINI_API_KEY = "your-gemini-key"
```

### 5. Run the Server

```bash
python app.py
```

Output:
```
 * Running on http://0.0.0.0:8000/
```

Open `http://localhost:8000` in your browser.

### 6. Verify Installation

Test the app:

```bash
# In another terminal (same venv):
curl http://localhost:8000/
# Should return HTML with the 90s-style UI
```

## Troubleshooting

**"ModuleNotFoundError: No module named 'flask'"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"Address already in use"**
- Port 8000 is busy; check `lsof -i :8000` (macOS/Linux) and kill the process, or change port in `app.py`

**"CSRF token" errors in browser**
- Clear browser cache; reload the page to get a fresh CSRF token

**Gemini API not working**
- Verify `GEMINI_API_KEY` is set: `echo $GEMINI_API_KEY`
- Check the key is valid on [Google AI Studio](https://aistudio.google.com/app/apikey)
