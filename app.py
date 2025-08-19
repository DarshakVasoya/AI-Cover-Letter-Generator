from flask import Flask, jsonify, request
import os
import openai

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

@app.route("/generate_coverletter", methods=["POST"])
def generate_coverletter():
    job_req = request.form.get("job_requirements", "")
    cv_data = request.form.get("cv_data", "")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Write a cover letter for the following job requirements:\n{job_req}\n\nCandidate CV data:\n{cv_data}",
        max_tokens=300
    )

    cover_letter = response.choices[0].text.strip()
    return jsonify({"cover_letter": cover_letter})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
