from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def answer_question(context, question):
    prompt = (
        "You are answering questions based only on the following research paper content.\n\n"
        "Paper content:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Answer in simple, clear language:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def explain_all(input_dir="summaries"):
    explanations = []

    for file in os.listdir(input_dir):
        with open(f"{input_dir}/{file}", "r", encoding="utf-8") as f:
            text = f.read()

        prompt = (
            "Explain this research content to a beginner using simple words "
            "and short sentences:\n\n" + text
        )

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = model.generate(**inputs, max_new_tokens=300)
        explanations.append(tokenizer.decode(outputs[0], skip_special_tokens=True))

    return "\n\n".join(explanations)
