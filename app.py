from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def generate_coverletter():
    cover_letter = """
    Dear Hiring Manager,

    I am excited to apply for the position. I believe my skills and experience make me a great fit.

    Best regards,
    Darshak Vasoya
    """
    return jsonify({"cover_letter": cover_letter.strip()})

if __name__ == "__main__":
    app.run(debug=True)
