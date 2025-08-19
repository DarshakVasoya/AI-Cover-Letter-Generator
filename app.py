from flask import Flask, jsonify
import os

app = Flask(__name__)

# Load environment variable (OpenAI API Key)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def generate_coverletter():
    cover_letter = f"""
    Dear Hiring Manager,

    I am excited to apply for the position. I believe my skills and experience make me a great fit.
    change messgae
    Best regards,
    Darshak Vasoya
    """ + OPENAI_API_KEY
    return jsonify({"cover_letter": cover_letter.strip(), "api_key_set": bool(OPENAI_API_KEY)})

if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
