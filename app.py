import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader
import fitz
import requests
from urllib.parse import urlparse, parse_qs

# Load summarizer model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.set_page_config(page_title="AI Text Summarizer", layout="wide")
st.title("📚 AI Text Summarizer")
st.write("Paste text, upload PDFs, or add a YouTube link to generate a summary.")

summary_length = st.slider("Summary Length (Words)", 50, 500, 150)

def summarize_text(text):
    return summarizer(text, max_length=summary_length, min_length=40, do_sample=False)[0]['summary_text']

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_with_fitz(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_youtube_id(url):
    query = urlparse(url)
    if query.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(query.query).get("v", [None])[0]
    if query.hostname == "youtu.be":
        return query.path[1:]
    return None

def get_youtube_transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join(entry["text"] for entry in transcript)
    return full_text

choice = st.radio("Select Input Type:", ["Text", "PDF File", "YouTube URL"])

if choice == "Text":
    text_input = st.text_area("Enter text here", "", height=250)
    if st.button("Summarize"):
        st.success(summarize_text(text_input))

elif choice == "PDF File":
    uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_pdf and st.button("Summarize PDF"):
        try:
            text_pdf = extract_text_with_fitz(uploaded_pdf)
        except:
            text_pdf = extract_text_from_pdf(uploaded_pdf)
        st.success(summarize_text(text_pdf))

elif choice == "YouTube URL":
    url = st.text_input("Enter YouTube link")
    if st.button("Summarize Video"):
        try:
            vid = extract_youtube_id(url)
            transcript = get_youtube_transcript(vid)
            st.success(summarize_text(transcript))
        except Exception as e:
            st.error("Transcript not available or invalid URL.")
