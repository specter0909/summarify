import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def summarize_text(text):
    response = model.generate_content(
        f"Summarize this clearly and concisely:\n\n{text}"
    )
    return response.text

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text

st.set_page_config(page_title="AI Summarizer", layout="centered")
st.title("🧠 AI Summarizer - Text & PDF")
st.write("Upload a PDF or paste text below to generate a summary.")

input_text = st.text_area("Enter text to summarize:")
uploaded_file = st.file_uploader("Or upload a PDF", type=["pdf"])

final_text = ""

if uploaded_file is not None:
    final_text = extract_text_from_pdf(uploaded_file)
elif input_text.strip() != "":
    final_text = input_text

if st.button("Generate Summary"):
    if final_text.strip() == "":
        st.warning("⚠ Please upload a PDF or enter text.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(final_text)
        st.subheader("📌 Summary Result")
        st.write(summary)
