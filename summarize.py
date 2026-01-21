from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "google/flan-t5-small"
INPUT_DIR = "extracted"
OUT_DIR = "summaries"

os.makedirs(OUT_DIR, exist_ok=True)

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

for file in os.listdir(INPUT_DIR):
    with open(f"{INPUT_DIR}/{file}", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        prompt = f"Summarize this section in simple language:\n{chunk}"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

        outputs = model.generate(
            **inputs,
            max_new_tokens=120
        )

        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        summaries.append(summary)

    with open(f"{OUT_DIR}/{file}", "w", encoding="utf-8") as f:
        f.write("\n".join(summaries))

print("Summarization done.")
