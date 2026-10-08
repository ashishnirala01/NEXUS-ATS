from flask import Flask, render_template, request
from pathlib import Path
from utils.pdf_parser import extract_text_from_pdf
from utils.ats_checker import analyze_resume

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")

    if not resume or resume.filename == "":
        return render_template("index.html", error="Please upload a PDF resume.")

    if not resume.filename.lower().endswith(".pdf"):
        return render_template("index.html", error="Only PDF files are supported.")

    file_path = UPLOAD_FOLDER / "resume.pdf"
    resume.save(file_path)

    try:
        resume_text = extract_text_from_pdf(file_path)

        if not resume_text.strip():
            return render_template(
                "index.html",
                error="No readable text found. Please upload a text-based PDF."
            )

        result = analyze_resume(resume_text)

    except Exception as e:
        return render_template("index.html", error=f"Analysis failed: {e}")

    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
