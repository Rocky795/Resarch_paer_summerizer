import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from extract import extract_pdf
from summarize import summarize_all
from explain import explain_all


class PaperExplainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Research Paper Explainer")
        self.root.geometry("900x600")

        self.pdf_path = None

        tk.Button(root, text="Select PDF", command=self.select_pdf).pack(pady=5)
        tk.Button(root, text="Summarize (Auto Preprocess)", command=self.run_summarize_pipeline).pack(pady=5)
        tk.Button(root, text="Explain", command=self.run_explain_pipeline).pack(pady=5)

        self.status = tk.StringVar(value="Idle")
        tk.Label(root, textvariable=self.status, fg="blue").pack(pady=5)

        self.output = tk.Text(root, wrap=tk.WORD)
        self.output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.status.set("PDF selected")

    def run_summarize_pipeline(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Select a PDF first")
            return
        threading.Thread(target=self._summarize_pipeline, daemon=True).start()

    def _summarize_pipeline(self):
        self.status.set("Extracting text from PDF...")
        extract_pdf(self.pdf_path)

        self.status.set("Summarizing paper...")
        summaries = summarize_all()

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "[SUMMARY OUTPUT]\n\n" + summaries)

        self.status.set("Summarization completed")

    def run_explain_pipeline(self):
        threading.Thread(target=self._explain_pipeline, daemon=True).start()

    def _explain_pipeline(self):
        self.status.set("Generating explanation...")
        explanation = explain_all()

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "[EXPLANATION OUTPUT]\n\n" + explanation)

        self.status.set("Explanation completed")


root = tk.Tk()
app = PaperExplainerApp(root)
root.mainloop()
