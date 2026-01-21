from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "google/flan-t5-small"
INPUT_DIR = "summaries"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

for file in os.listdir(INPUT_DIR):
    with open(f"{INPUT_DIR}/{file}", "r", encoding="utf-8") as f:
        text = f.read()

    prompt = (
        "Explain the following research content to a beginner. "
        "Use simple words, short sentences, and analogies if helpful:\n\n"
        + text
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=300
    )

    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("\n" + "="*50)
    print(f"EXPLANATION FOR {file.upper()}")
    print("="*50)
    print(explanation)
