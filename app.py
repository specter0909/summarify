import streamlit as st
from summarizer import Summarizer
import pdfplumber

st.set_page_config(page_title='Summarify - Text & PDF Summarizer', layout='centered')

st.title('Summarify — Text & PDF Summarizer (MVP)')
st.write('Paste text or upload a PDF. Large documents will be chunked and summarized in multiple passes.')

model_name = st.text_input('Model name (transformers)', value='facebook/bart-large-cnn', help='Change this to a smaller model if you get memory issues, e.g. sshleifer/distilbart-cnn-12-6 or t5-small')

summary_type = st.selectbox('Summary length', ['short', 'medium', 'long'], index=1)
show_keypoints = st.checkbox('Also extract key bullet points', value=True)

input_mode = st.radio('Input', ['Paste text', 'Upload PDF'])

input_text = ''
if input_mode == 'Paste text':
    input_text = st.text_area('Paste the text or book excerpt here', height=300)
else:
    uploaded = st.file_uploader('Upload PDF', type=['pdf'])
    if uploaded is not None:
        with pdfplumber.open(uploaded) as pdf:
            pages = [p.extract_text() or '' for p in pdf.pages]
        input_text = '\n'.join(pages)
        st.success(f'Extracted {len(pages)} pages. Approx {len(input_text)} characters.')

if st.button('Summarize') and input_text.strip():
    with st.spinner('Loading model and summarizing — this may take a minute for large documents...'):
        summarizer = Summarizer(model_name=model_name)
        try:
            summary = summarizer.summarize(input_text, summary_type=summary_type)
            st.subheader('Summary')
            st.write(summary)
            if show_keypoints:
                st.subheader('Key points')
                kps = summarizer.extract_keypoints(input_text, max_points=8)
                for i, kp in enumerate(kps, 1):
                    st.write(f"{i}. {kp}")
        except Exception as e:
            st.error(f'Error while summarizing: {e}')
            st.info('Try a smaller model or shorter input if you see memory errors.')\n