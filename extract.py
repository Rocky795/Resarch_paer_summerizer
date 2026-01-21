import pdfplumber
import os

PDF_PATH = "papers/19-301.pdf"
OUT_DIR = "extracted"

os.makedirs(OUT_DIR, exist_ok=True)

sections = {
    "abstract": [],
    "introduction": [],
    "method": [],
    "conclusion": []
}

with pdfplumber.open(PDF_PATH) as pdf:
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
        with open(f"{OUT_DIR}/{name}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

print("Extraction done.")
