# AI Cover Letter Generator (Gemini Only)

Flask microservice that generates a tailored cover letter from:
- A PDF resume (parsed to text in memory via PyPDF2)
- A plain text job description

It uses **Google Gemini** models (default: `gemini-1.5-flash`). All OpenAI code was removed.

## Features
- POST `/generate_coverletter` accepts either multipart (PDF + job description) or JSON (`resume_text` + `job_description`).
- PDF text extraction entirely in-memory (no disk writes).
- `/health` endpoint reports configuration status (no secrets exposed).
- Root `/` provides a simple HTML form for manual testing.
- Environment-driven configuration via `.env` or host platform variables.

## Quick Start

### 1. Clone & create virtual environment
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables
Create a `.env` file (NOT committed):
```
GEMINI_API_KEY=your_google_generative_ai_key_here
GEMINI_MODEL=gemini-1.5-flash
```
Or set in Windows cmd for current session:
```
set GEMINI_API_KEY=your_key_here
set GEMINI_MODEL=gemini-1.5-flash
```
PowerShell:
```
$env:GEMINI_API_KEY="your_key_here"
$env:GEMINI_MODEL="gemini-1.5-flash"
```

### 3. Run
```
venv\Scripts\python.exe app.py
```
Visit: http://127.0.0.1:5000/

## API

### Health
GET `/health`
```
{
  "status": "ok",
  "gemini_configured": true,
  "default_provider": "gemini",
  "version": "1.0.0"
}
```

### Generate Cover Letter (Multipart)
```
curl -X POST http://127.0.0.1:5000/generate_coverletter ^
  -F job_description="Senior Python developer role focusing on APIs" ^
  -F resume=@resume.pdf
```

### Generate Cover Letter (JSON)
Windows cmd (escape quotes):
```
curl -X POST http://127.0.0.1:5000/generate_coverletter -H "Content-Type: application/json" -d "{\"job_description\":\"Senior Python developer role\",\"resume_text\":\"Experienced developer with...\"}"
```
PowerShell (simpler):
```
curl -Method POST http://127.0.0.1:5000/generate_coverletter -ContentType 'application/json' -Body '{"job_description":"Senior Python developer role","resume_text":"Experienced developer with..."}'
```

### Response
```
{
  "cover_letter": "...generated text...",
  "resume_text_chars": 12345,
  "resume_parse_status": "ok",       // or "empty_or_unparsed"
  "provider": "gemini",
  "model_used": "gemini-1.5-flash"
}
```

## PDF Parsing
- Library: PyPDF2
- If a page fails to extract, it's skipped; result may be partial.
- Empty or unparsable PDFs set `resume_parse_status` to `empty_or_unparsed`.

## Customizing Prompt
Edit `_build_prompt` in `app.py` to adjust tone, length, or structure.

## Deployment
A `Procfile` exists for platforms like Heroku:
```
web: python app.py
```
Set environment variables in platform dashboard (never hardcode keys):
- `GEMINI_API_KEY`
- `GEMINI_MODEL` (optional)
- `PORT` (often injected automatically by the host; the app respects it)

### Example (Heroku CLI)
```
heroku config:set GEMINI_API_KEY=your_key GEMINI_MODEL=gemini-1.5-flash
```

## Security Notes
- Treat API keys as secrets. Do not commit `.env`.
- Log output currently prints a simple request line; avoid logging full resume/job text in production if privacy is critical.
- Add rate limiting / auth (e.g., API key header) before exposing publicly.

## Error Handling
The service returns placeholder messages like `[GEMINI_API_KEY not set: ...]` if no key is configured. Gemini API exceptions are wrapped as `[gemini_error: ...]` in the `cover_letter` field. Adjust this for stricter HTTP error codes if desired.

## Extending
Possible enhancements:
- Add streaming output (server-sent events or chunked response).
- Add authentication (Bearer token or API key header).
- Cache resume embeddings for repeated requests.
- Add unit tests (e.g., mock Gemini responses).

## Project Structure
```
app.py              # Flask app & endpoints
requirements.txt    # Python dependencies
Procfile            # Process definition (Heroku style)
.env (ignored)      # Local environment variables
```

## Dependency List (Key)
- Flask
- PyPDF2
- python-dotenv
- google-generativeai

## Testing (Manual)
1. Health check: `curl http://127.0.0.1:5000/health`
2. JSON request: see examples above.
3. PDF request: ensure resume is a readable PDF (not scanned image).

## Contributing
1. Create a feature branch
2. Make changes + add concise commit messages
3. Open a PR describing change & testing steps

## License
Add a license (MIT/Apache-2.0) as needed. Currently unspecified.

---
Questions or want new features (streaming, auth, multiple providers)? Open an issue or implement and submit a PR.
