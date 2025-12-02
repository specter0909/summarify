import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pdfplumber
import docx2txt
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="AI Summarizer", page_icon="🧠", layout="wide")

@st.cache_resource
def load_model():
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    return tokenizer, model

tokenizer, model = load_model()

def summarize_text(text, max_len):
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=4000, truncation=True)
    outputs = model.generate(inputs, max_length=max_len, min_length=40, length_penalty=2.0)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

st.title("🧠 AI Text Summarizer")

summary_len = st.slider("Summary length (words)", 50, 300, 120)

choice = st.selectbox("Choose Input Type", ["Text", "Upload PDF/DOCX", "Website URL", "YouTube Link"])

if choice == "Text":
    text = st.text_area("Enter text")
    if st.button("Summarize"):
        st.write(summarize_text(text, summary_len))

elif choice == "Upload PDF/DOCX":
    file = st.file_uploader("Upload a PDF or DOCX", type=["pdf","docx"])
    if file:
        if file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        else:
            text = docx2txt.process(file)
        if st.button("Summarize File"):
            st.write(summarize_text(text, summary_len))

elif choice == "Website URL":
    url = st.text_input("Enter article url")
    if st.button("Summarize URL"):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        text = " ".join([p.text for p in soup.find_all("p")])
        st.write(summarize_text(text, summary_len))

elif choice == "YouTube Link":
    yt = st.text_input("Enter YouTube link")
    if st.button("Summarize Video"):
        video_id = yt.split("=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([x['text'] for x in transcript])
        st.write(summarize_text(text, summary_len))
