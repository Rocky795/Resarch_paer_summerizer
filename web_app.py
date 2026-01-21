import streamlit as st
import tempfile
import os

from extract import extract_pdf
from summarize import summarize_all
from explain import explain_all

st.set_page_config(
    page_title="AI Research Paper Explainer",
    layout="wide"
)

st.title("📄 AI Research Paper Explainer")
st.write(
    "Upload a research paper PDF. "
    "Click **Explain Paper** to automatically extract, summarize, and explain it."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    if st.button("🧠 Explain Paper (Auto Preprocess)"):
        with st.status("Running full pipeline...", expanded=True) as status:

            # 1. Extraction
            status.update(label="Step 1/3: Extracting text from PDF...")
            extract_pdf(pdf_path)

            # 2. Summarization
            status.update(label="Step 2/3: Summarizing paper...")
            summaries = summarize_all()

            # 3. Explanation
            status.update(label="Step 3/3: Generating explanation...")
            explanation = explain_all()

            status.update(label="Completed successfully", state="complete")

        # -------- DISPLAY RESULTS --------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Summary")
            st.text_area(
                label="Summary Output",
                value=summaries,
                height=450
            )

        with col2:
            st.subheader("🧠 Explanation (Beginner Friendly)")
            st.text_area(
                label="Explanation Output",
                value=explanation,
                height=450
            )
