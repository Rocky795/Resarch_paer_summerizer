from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def chunk_text(text, max_tokens=400):
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

def summarize_all(input_dir="extracted", out_dir="summaries"):
    os.makedirs(out_dir, exist_ok=True)
    all_summaries = []

    for file in os.listdir(input_dir):
        with open(f"{input_dir}/{file}", "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        section_summaries = []

        for chunk in chunks:
            prompt = f"Summarize this section in simple language:\n{chunk}"
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
            outputs = model.generate(**inputs, max_new_tokens=120)
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            section_summaries.append(summary)

        combined = "\n".join(section_summaries)
        all_summaries.append(f"--- {file.upper()} ---\n{combined}")

        with open(f"{out_dir}/{file}", "w", encoding="utf-8") as f:
            f.write(combined)

    return "\n\n".join(all_summaries)
