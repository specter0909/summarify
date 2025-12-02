from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import math
import re

# --- Helpers ---
def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", ' ', text).strip()

def chunk_text(text: str, max_chunk_chars: int=4000):
    """Split text into chunks not exceeding max_chunk_chars (approximate) by sentence boundaries."""
    text = clean_whitespace(text)
    # split into sentences (simple heuristic)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = []
    current_len = 0
    for s in sentences:
        if current_len + len(s) + 1 <= max_chunk_chars:
            current.append(s)
            current_len += len(s) + 1
        else:
            if current:
                chunks.append(' '.join(current))
            # if single sentence longer than max_chunk_chars, force-split
            if len(s) > max_chunk_chars:
                for i in range(0, len(s), max_chunk_chars):
                    chunks.append(s[i:i+max_chunk_chars])
                current = []
                current_len = 0
            else:
                current = [s]
                current_len = len(s) + 1
    if current:
        chunks.append(' '.join(current))
    return chunks

class Summarizer:
    def __init__(self, model_name: str = 'facebook/bart-large-cnn', device: int = -1):
        """device=-1 uses CPU. On machines with GPU, set device=0."""
        self.model_name = model_name
        # lazy load pipeline
        self._pipe = None

    def _ensure_pipe(self):
        if self._pipe is None:
            try:
                self._pipe = pipeline('summarization', model=self.model_name, truncation=True)
            except Exception as e:
                raise RuntimeError(f"Failed to load model {self.model_name}: {e}") from e

    def summarize(self, text: str, summary_type: str = 'short'):
        """summary_type: 'short', 'medium', 'long'"""
        self._ensure_pipe()
        text = clean_whitespace(text)
        # decide lengths
        if summary_type == 'short':
            min_len, max_len = 20, 80
        elif summary_type == 'medium':
            min_len, max_len = 60, 160
        else:
            min_len, max_len = 140, 400

        # chunk if needed
        chunks = chunk_text(text, max_chunk_chars=3000)
        summaries = []
        for c in chunks:
            try:
                out = self._pipe(c, max_length=max_len, min_length=min_len, do_sample=False)
                summaries.append(out[0]['summary_text'])
            except Exception as e:
                # fallback: truncate and summarize
                truncated = c[:4000]
                out = self._pipe(truncated, max_length=max_len, min_length=min_len, do_sample=False)
                summaries.append(out[0]['summary_text'])

        if len(summaries) == 1:
            combined = summaries[0]
        else:
            # combine chunk summaries and summarize again for cohesion
            combined_text = ' '.join(summaries)
            combined = self._pipe(combined_text, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']

        return combined

    def extract_keypoints(self, text: str, max_points: int = 8):
        """Simple heuristic: split the long summary into sentences and choose top N sentences by length/position."""
        summary = self.summarize(text, summary_type='medium')
        sents = re.split(r'(?<=[.!?])\s+', summary)
        # choose longest sentences up to max_points
        sents_sorted = sorted(sents, key=lambda s: len(s), reverse=True)
        chosen = sents_sorted[:max_points]
        # preserve original order
        chosen_sorted = sorted(chosen, key=lambda s: summary.index(s))
        return [c.strip() for c in chosen_sorted if c.strip()]

if __name__ == '__main__':
    # quick local test
    s = Summarizer()
    sample = """Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. AI can be categorized into narrow AI, which is designed for a specific task, and general AI, which can perform any intellectual task that a human can. Applications of AI include natural language processing, computer vision, robotics, and expert systems."""
    print('Short summary: ', s.summarize(sample, 'short'))
    print('Key points: ', s.extract_keypoints(sample, 3))\n