import streamlit as st
from transformers import pipeline
import pdfplumber
import docx2txt
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="AI Summarizer", page_icon="🧠", layout="wide")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.title("🧠 AI Text Summarizer")
st.write("Paste text, upload PDF/DOCX, enter a URL or YouTube link to generate summaries.")

summary_length = st.slider("Summary length (words)", 50, 500, 150)

option = st.selectbox(
    "Choose input type",
    ["Text", "Upload PDF/DOCX", "Website URL", "YouTube Link"]
)

def make_summary(text):
    summary = summarizer(text, max_length=summary_length, min_length=40, do_sample=False)[0]["summary_text"]
    return summary

if option == "Text":
    text = st.text_area("Enter text to summarize here")
    if st.button("Summarize"):
        st.write(make_summary(text))

elif option == "Upload PDF/DOCX":
    file = st.file_uploader("Upload your file", type=["pdf","docx"])
    if file is not None:
        if file.type == "application/pdf":
            with pdfplumber.open(file) as pdf:
                text = " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        else:
            text = docx2txt.process(file)

        if st.button("Summarize File"):
            st.write(make_summary(text))

elif option == "Website URL":
    url = st.text_input("Enter article link")
    if st.button("Summarize URL"):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = " ".join(paragraphs)
        st.write(make_summary(text))

elif option == "YouTube Link":
    yt_url = st.text_input("Enter YouTube URL")
    if st.button("Summarize Video"):
        video_id = yt_url.split("=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([x["text"] for x in transcript])
        st.write(make_summary(full_text))
