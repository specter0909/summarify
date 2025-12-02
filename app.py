import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Summarizer", layout="wide")

st.title("📚 AI Text Summarizer")
st.write("Paste any text, article, blog, report, or book chapter below and get a clean summary.")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text = st.text_area("Enter text to summarize:", height=300)

summary_length = st.slider("Summary length:", 50, 300, 120)

if st.button("Summarize"):
    if len(text) < 50:
        st.warning("Enter more text to summarize…")
    else:
        with st.spinner("Summarizing..."):
            result = summarizer(text, max_length=summary_length, min_length=50, do_sample=False)
            st.subheader("🔍 Summary")
            st.write(result[0]['summary_text'])
