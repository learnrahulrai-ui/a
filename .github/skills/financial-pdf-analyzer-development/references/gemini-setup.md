# Gemini API Integration

## Overview

The `analyze_with_gemini()` function sends uploaded PDF metadata and text snippets to Google's Gemini API for financial analysis.

## Obtaining a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API key"**
3. Copy the key and store it securely

## Configuration

Set the environment variable:

```bash
export GEMINI_API_KEY="sk-proj-..."
```

If not set, analysis gracefully returns:
```
"Analysis skipped: GEMINI_API_KEY is not configured on the server."
```

## How It Works

1. User uploads PDFs → server validates and extracts text snippets
2. `analyze_with_gemini()` builds a prompt with company name and file summaries
3. POST request to: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`
4. Response contains AI-generated financial analysis

## API Call Details

**Endpoint**: `gemini-2.0-flash` model
**Temperature**: 0.2 (low variance, factual)
**Max Output Tokens**: 900 (concise analysis)
**Timeout**: 35 seconds

## Error Handling

If the API call fails, the function returns:
```
"Analysis failed safely. Error: {exception_type}"
```

Examples:
- `ConnectionError` → Network issue
- `Timeout` → Request took >35 seconds
- `JSONDecodeError` → Invalid response from API

## Rate Limits

Google Gemini API has project-level quotas. If hit:
- Response status: 429
- Error: `"Rate limit exceeded"`

Contact Google Cloud support to increase quota.

## Security Notes

- **Never commit API keys** — use environment variables only
- **Rotate quarterly** — regenerate in Google AI Studio
- **Production**: Use service accounts and Secret Manager instead of raw keys

## Testing Without an API Key

The app works fine without Gemini configured. For testing, comment out the `if not api_key:` check or provide a mock response.

## Example Request Payload

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "You are a financial analyst assistant. Review uploaded PDF data for company: Acme Corp. Give a concise report with: 1) file completeness observation, 2) potential risks, 3) revenue/profit trends if present, 4) confidence level and caveats.\n\nData:\n[{\"filename\": \"acme-2024.pdf\", \"size_bytes\": 250000, \"text_snippet\": \"Revenue: $5M...\", \"has_extractable_text\": true}]"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 900
  }
}
```

## Example Response

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "**Analysis Summary**\n\n1. **File Completeness**: One comprehensive financial document for Acme Corp for 2024.\n\n2. **Potential Risks**: Revenue concentration in single market; observe expense growth.\n\n3. **Trends**: Revenue growth of 15% YoY; profit margins stable.\n\n4. **Confidence**: High (80%) — document is clear; limited to one fiscal year."
          }
        ]
      }
    }
  ]
}
```
