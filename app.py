import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("AI Summarizer App")
import streamlit as st
import PyPDF2
import pandas as pd
from docx import Document
import google.generativeai as genai

st.set_page_config(page_title="AI Summarizer", layout="wide")
st.title("AI Summarizer Tool")

# API Key input
api_key = st.text_input("Enter Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

option = st.selectbox(
    "Select upload type",
    ("PDF File", "Text", "Word File", "Excel File")
)

text_data = ""

if option == "PDF File":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text_data += page.extract_text()
        st.text_area("Extracted Text", text_data, height=300)

elif option == "Text":
    text_data = st.text_area("Enter text manually", height=300)

elif option == "Word File":
    doc_file = st.file_uploader("Upload DOCX", type=["docx"])
    if doc_file:
        doc = Document(doc_file)
        text_data = "\n".join([p.text for p in doc.paragraphs])
        st.text_area("Extracted text", text_data, height=300)

elif option == "Excel File":
    excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if excel_file:
        df = pd.read_excel(excel_file)
        st.write(df)
        text_data = df.to_string()

# summarizing
if api_key and text_data:
    if st.button("Generate Summary"):
        with st.spinner("Summarizing..."):
            response = model.generate_content(
                f"Summarize the following text in bullet points:\n{text_data}"
            )
            st.subheader("Summary")
            st.write(response.text)
