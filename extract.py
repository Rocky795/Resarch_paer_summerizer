import pdfplumber
import os

def extract_pdf(pdf_path, out_dir="extracted"):
    os.makedirs(out_dir, exist_ok=True)

    sections = {
        "abstract": [],
        "introduction": [],
        "method": [],
        "conclusion": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lower = text.lower()
            if "abstract" in lower:
                sections["abstract"].append(text)
            elif "introduction" in lower:
                sections["introduction"].append(text)
            elif "method" in lower or "approach" in lower:
                sections["method"].append(text)
            elif "conclusion" in lower:
                sections["conclusion"].append(text)

    for name, content in sections.items():
        if content:
            with open(f"{out_dir}/{name}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(content))
