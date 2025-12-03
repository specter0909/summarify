import streamlit as st
import PyPDF2
import pandas as pd
from docx import Document

st.set_page_config(page_title="AI Summarizer", layout="wide")

st.title("AI Summarizer Tool")

option = st.selectbox(
    "Select upload type",
    ("PDF File", "Text", "Word File", "Excel File")
)

if option == "PDF File":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.text_area("Extracted Text", text, height=300)

elif option == "Text":
    text_input = st.text_area("Enter text manually", height=300)
    st.write(text_input)

elif option == "Word File":
    doc_file = st.file_uploader("Upload DOCX", type=["docx"])
    if doc_file:
        doc = Document(doc_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.text_area("Extracted text", text, height=300)

elif option == "Excel File":
    excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if excel_file:
        df = pd.read_excel(excel_file)
        st.write(df)
