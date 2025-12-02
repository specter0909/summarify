import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import re
import docx2txt
import fitz

# Title
st.title("✨ AI Summarizer - By Om Jethani")

# Load summarizer
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Function to summarize text
def summarize_text(text, max_length=200):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]["summary_text"]

# Extract text from PDF
def read_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

# Extract text from YouTube
def extract_youtube_transcript(url):
    video_id = re.search(r"v=([^&]+)", url).group(1)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

# Sidebar
choice = st.sidebar.selectbox(
    "Choose input type",
    ["Text", "Upload File", "YouTube Link"]
)

text_data = ""

if choice == "Text":
    text_data = st.text_area("Enter your text")

elif choice == "Upload File":
    uploaded = st.file_uploader("Upload Document (PDF/TXT/DOCX)", type=["pdf", "txt", "docx"])
    if uploaded:
        if uploaded.type == "application/pdf":
            text_data = read_pdf(uploaded)
        elif uploaded.type == "text/plain":
            text_data = uploaded.read().decode("utf-8")
        elif uploaded.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_data = docx2txt.process(uploaded)

elif choice == "YouTube Link":
    url = st.text_input("Enter YouTube video link")
    if st.button("Extract Transcript"):
        text_data = extract_youtube_transcript(url)
        st.success("Transcript extracted successfully!")

# Summarize button
if st.button("Summarize"):
    if text_data.strip():
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_data)
            st.subheader("🔍 Summary:")
            st.write(summary)
    else:
        st.warning("Please enter or upload content first")
