import streamlit as st
from transformers import pipeline

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.title("AI Text Summarizer ✨")
st.write("Paste any long text below and click Summarize to get a shorter version.")

# Input text box
user_input = st.text_area("Enter text to summarize", height=300)

# Button to trigger summarization
if st.button("Summarize"):
    if user_input.strip():
        try:
            summary = summarizer(
                user_input,
                max_length=300,
                min_length=80,
                do_sample=False
            )[0]["summary_text"]

            st.subheader("Summary:")
            st.write(summary)

        except Exception as e:
            st.error(f"Error during summarization: {e}")
    else:
        st.warning("Please enter some text first.")
