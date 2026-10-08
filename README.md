# NEXUS ATS

NEXUS ATS is a Python + Flask resume ATS analyzer.

## Version 1.0

The user uploads only a PDF resume.

NEXUS ATS analyzes:
- Basic ATS-friendly structure
- Contact information
- Standard resume sections
- Detected professional/technical skills
- Basic text readability
- Improvement suggestions
- Estimated ATS score

## Run in VS Code

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## Important

This is a rule-based v1.0 analyzer. Real companies can use different ATS systems and criteria, so the score is an estimate, not a guaranteed employer ATS score.
