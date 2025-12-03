import streamlit as st
import google.generativeai as genai
import PyPDF2

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.set_page_config(page_title="AI Summarizer", layout="centered")
st.title("📄 AI Summarizer – Text & PDF")
st.write("Upload a PDF or paste text below to generate a smart summary.")

# Function to summarize text using Gemini model
def summarize_text(text):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(f"Summarize this clearly and concisely:\n\n{text}")
    return response.text

# PDF upload section
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

text_input = st.text_area("Or paste text here", height=200)

if st.button("Summarize"):
    final_text = ""

    # Extract PDF text if uploaded
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            final_text += page.extract_text()

    # Or use typed text
    elif text_input.strip() != "":
        final_text = text_input

    if final_text.strip() == "":
        st.error("Please upload a PDF or paste some text to summarize.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(final_text)
            st.subheader("✨ Summary")
            st.write(summary)
