import os
import PyPDF2
import docx
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(path)
    elif ext == '.docx':
        text = extract_text_from_docx(path)
    else:
        return {"skills": [], "summary": "Unsupported file type"}

    doc = nlp(text)

    # Load skills
    with open(os.path.join(os.path.dirname(__file__), "skills.txt")) as f:
        skills_list = [line.strip().lower() for line in f.readlines()]

    # Extract skills
    found_skills = set()
    for token in doc:
        if token.text.lower() in skills_list:
            found_skills.add(token.text)

    # Create summary from first 2 sentences
    sentences = list(doc.sents)
    summary = " ".join([str(s) for s in sentences[:2]])

    return {
        "skills": list(found_skills),
        "summary": summary
    }
