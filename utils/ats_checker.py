import re

SKILLS = [
    "python", "c++", "java", "javascript", "c#", "sql",
    "html", "css", "flask", "django", "fastapi",
    "git", "github", "docker", "azure", "aws",
    "machine learning", "deep learning", "artificial intelligence",
    "generative ai", "prompt engineering", "nlp", "computer vision",
    "pandas", "numpy", "matplotlib", "tensorflow", "pytorch",
    "scikit-learn", "data structures", "algorithms", "dsa",
    "oop", "dbms", "operating systems", "computer networks",
    "rest api", "mongodb", "mysql", "postgresql",
    "problem solving", "communication", "teamwork"
]

SECTIONS = {
    "Contact": ["@", "linkedin", "github"],
    "Education": ["education", "b.tech", "bachelor"],
    "Skills": ["skills", "technical skills"],
    "Projects": ["projects", "project"],
    "Certifications": ["certifications", "certificate"],
    "Experience": ["experience", "internship"]
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def analyze_resume(text):
    data = normalize(text)

    # Detect known skills in the resume.
    matched_skills = [
        skill for skill in SKILLS
        if skill in data
    ]

    # Basic ATS section checks.
    section_results = {}
    for section, terms in SECTIONS.items():
        section_results[section] = any(term in data for term in terms)

    section_score = round(
        sum(section_results.values()) / len(section_results) * 100
    )

    # Contact check.
    contact_ok = (
        bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
        or "linkedin" in data
        or "github" in data
    )

    # Text quality / readability checks.
    word_count = len(text.split())
    readable = word_count >= 80

    checks = {
        "Readable text": readable,
        "Contact information": contact_ok,
        "Standard sections": section_score >= 60,
        "Skills detected": len(matched_skills) >= 3,
        "Projects detected": section_results["Projects"],
    }

    basic_score = round(
        sum(checks.values()) / len(checks) * 100
    )

    # v1 score: combines resume structure and detected professional skills.
    skill_score = min(100, len(matched_skills) * 5)
    final_score = round(
        section_score * 0.35 +
        basic_score * 0.35 +
        skill_score * 0.30
    )

    suggestions = []

    if not contact_ok:
        suggestions.append("Add clear contact information such as email, LinkedIn, or GitHub.")

    if not section_results["Education"]:
        suggestions.append("Add a clear Education section.")

    if not section_results["Skills"]:
        suggestions.append("Add a clear Skills section.")

    if not section_results["Projects"]:
        suggestions.append("Add a clear Projects section.")

    if not section_results["Certifications"]:
        suggestions.append("Add Certifications if you have relevant certificates.")

    if len(matched_skills) < 5:
        suggestions.append("Add relevant technical skills that you genuinely know.")

    if word_count < 150:
        suggestions.append("Your resume may be too short; add relevant project or achievement details.")

    if not suggestions:
        suggestions.append("Your resume passes the basic NEXUS ATS v1 checks. Keep improving measurable project details.")

    return {
        "score": final_score,
        "skill_score": skill_score,
        "section_score": section_score,
        "basic_score": basic_score,
        "skills": matched_skills,
        "sections": section_results,
        "checks": checks,
        "suggestions": suggestions
    }
