from flask import Flask, jsonify, request
import os
import openai
from io import BytesIO
from typing import Optional

try:
    # Lightweight PDF text extraction
    from PyPDF2 import PdfReader  # type: ignore
except Exception:  # pragma: no cover - if dependency missing runtime error handled later
    PdfReader = None  # type: ignore

app = Flask(__name__)

# Load OpenAI API Key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def _extract_pdf_text(file_obj) -> str:
    """Extract text from an uploaded PDF file object.

    Falls back to empty string if parsing fails. Does not write to disk.
    """
    if not PdfReader:
        return ""
    try:
        reader = PdfReader(file_obj)
        chunks = []
        for page in reader.pages:
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            if txt:
                chunks.append(txt.strip())
        return "\n\n".join(chunks)
    except Exception:
        return ""


def _build_prompt(job_description: str, resume_text: str) -> str:
    return (
        "You are an assistant that writes concise, tailored, professional cover letters. "
        "Use the candidate's resume content to highlight the most relevant achievements for the given job description. "
        "Avoid repeating bullet lists; write in paragraph form, one page max.\n\n"
        f"Job Description:\n{job_description.strip()}\n\nResume:\n{resume_text.strip()[:12000]}\n\nCover Letter (start with a professional greeting):\n"
    )


def _call_openai(prompt: str, model: Optional[str] = None, temperature: float = 0.65, max_tokens: int = 600) -> str:
    """Call OpenAI API using either ChatCompletion (if available) or Completion as fallback."""
    if not OPENAI_API_KEY:
        # Allow graceful degradation in environments without key
        return "[OPENAI_API_KEY not set: returning placeholder cover letter based on prompt truncation.]\n" + prompt[-400:]

    model = model or os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    try:
        if model.startswith("gpt-"):
            # Chat-based
            chat_response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You write professional, tailored cover letters."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return chat_response.choices[0].message["content"].strip()
        else:
            comp = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return comp.choices[0].text.strip()
    except Exception as e:
        return f"[OpenAI API error: {e}]"


@app.route("/generate_coverletter", methods=["POST"])
def generate_coverletter():
    """Generate a cover letter from an uploaded PDF resume + plain-text job description.

    Expected multipart/form-data fields:
      - resume: PDF file (required)
      - job_description: text (required)
    Optional JSON alternative: {"job_description": "...", "resume_text": "..."}
    """
    # Support JSON body without file for flexibility (e.g., pre-extracted text)
    if request.content_type and "application/json" in request.content_type:
        data = request.get_json(silent=True) or {}
        job_description = data.get("job_description", "").strip()
        resume_text = data.get("resume_text", "").strip()
    else:
        job_description = (request.form.get("job_description") or "").strip()
        resume_file = request.files.get("resume")
        resume_text = ""
        if resume_file:
            # Read file bytes into memory buffer for PyPDF2
            resume_bytes = resume_file.read()
            resume_text = _extract_pdf_text(BytesIO(resume_bytes))
    if not job_description:
        return jsonify({"error": "job_description is required"}), 400
    if not resume_text:
        # Provide hint if PDF extraction failed
        resume_status = "empty_or_unparsed"
    else:
        resume_status = "ok"

    prompt = _build_prompt(job_description, resume_text or "(No resume text extracted)")
    cover_letter = _call_openai(prompt)

    return jsonify({
        "cover_letter": cover_letter,
        "resume_text_chars": len(resume_text),
        "resume_parse_status": resume_status,
        "model_used": os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo" if OPENAI_API_KEY else "placeholder"),
    })
    
@app.route("/test_coverletter")
def test_coverletter():
    return jsonify({
        "cover_letter": "This is a dummy cover letter. Use POST for real generation."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
