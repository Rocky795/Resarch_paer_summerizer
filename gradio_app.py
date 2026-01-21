import gradio as gr
from extract import extract_pdf
from summarize import summarize_all
from explain import explain_all, answer_question

# Global cache (simple, effective)
CACHED_SUMMARY = ""


def explain_paper(pdf_file):
    global CACHED_SUMMARY

    if pdf_file is None:
        return "No PDF uploaded", "", ""

    pdf_path = pdf_file.name

    # Full pipeline
    extract_pdf(pdf_path)
    summaries = summarize_all()
    explanation = explain_all()

    CACHED_SUMMARY = summaries

    return summaries, explanation, ""


def ask_question(question):
    if not CACHED_SUMMARY:
        return "Please explain a paper first."

    if not question.strip():
        return "Ask a valid question."

    answer = answer_question(CACHED_SUMMARY, question)
    return answer


with gr.Blocks(title="AI Research Paper Explainer + Q&A") as demo:
    gr.Markdown("# 📄 AI Research Paper Explainer with Q&A")

    pdf_input = gr.File(label="Upload Research Paper (PDF)", file_types=[".pdf"])

    explain_btn = gr.Button("🧠 Explain Paper")

    with gr.Row():
        summary_box = gr.Textbox(label="📌 Summary", lines=18)
        explanation_box = gr.Textbox(label="🧠 Explanation", lines=18)

    explain_btn.click(
        fn=explain_paper,
        inputs=pdf_input,
        outputs=[summary_box, explanation_box, gr.Textbox(visible=False)]
    )

    gr.Markdown("## ❓ Ask Questions About the Paper")

    question_input = gr.Textbox(
        label="Your Question",
        placeholder="e.g. What problem does this paper solve?"
    )

    answer_output = gr.Textbox(
        label="Answer",
        lines=8
    )

    ask_btn = gr.Button("Ask Question")

    ask_btn.click(
        fn=ask_question,
        inputs=question_input,
        outputs=answer_output
    )

demo.launch()
