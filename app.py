from flask import Flask, jsonify, request
import os
import openai

app = Flask(__name__)

# Load OpenAI API Key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

@app.route("/generate_coverletter", methods=["GET", "POST"])
def generate_coverletter():
    # Get job requirements and CV data
    job_req = request.args.get("job_requirements") or request.form.get("job_requirements", "")
    cv_data = request.args.get("cv_data") or request.form.get("cv_data", "")

    if not OPENAI_API_KEY:
        return jsonify({"error": "OpenAI API key not set in environment variables."})

    # Generate cover letter using OpenAI
    prompt = f"Write a professional cover letter for a job with the following requirements:\n{job_req}\n\nMy CV data:\n{cv_data}\n\nCover letter:"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        cover_letter = response.choices[0].text.strip()
        return jsonify({"cover_letter": cover_letter})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/test_coverletter")
def test_coverletter():
    return jsonify({
        "cover_letter": "This is a dummy cover letter. Use POST for real generation."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
