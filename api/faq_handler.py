import nltk
nltk.download('punkt')
nltk.download('stopwords')

import pandas as pd
import string
import unicodedata
import html
from tqdm import tqdm
import contractions
import collections
import collections.abc
collections.Sequence = collections.abc.Sequence
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import os
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch
from config.config import ConfigManger
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = ConfigManger()

# Load HF model + tokenizer once
model_name = config.get_embeddings_model_name()
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

uploaded_faqs = config.get_uploaded_faqs_file()
uploaded_faiss_index_file = config.get_uploaded_faqs_faiss_index()

def get_embedding(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings.numpy().astype("float32")

def preprocess_text(df):
    def _preprocess(text):
        text = text.lower()
        text = contractions.fix(text)
        text = unicodedata.normalize("NFKD", text)
        text = html.unescape(text)
        text = "".join(char for char in text if char.isalnum() or char.isspace() or char in ['.', ',', '?'])
        text = ' '.join(text.split())
        return text

    df['question'] = df['question'].apply(_preprocess)
    df['answer'] = df['answer'].apply(_preprocess)
    return df

def summarize_text(df):
    def _summarize(text):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()

        if len(text.split()) < 100:
            return text
        elif len(text.split()) <= 200:
            summary = summarizer(parser.document, 3)
            return "".join([str(sentence) for sentence in summary])
        elif len(text.split()) <= 300:
            summary = summarizer(parser.document, 5)
            return "".join([str(sentence) for sentence in summary])
        return text

    df['summary'] = df['answer'].apply(_summarize)
    df['answer'] = df["summary"]
    df = df.drop("summary", axis=1)
    return df

def embed_questions(df):
    faq_questions = df["question"].tolist()
    embeddings = get_embedding(faq_questions)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, uploaded_faiss_index_file)

    return None

def save_file(df):
    df.to_csv(uploaded_faqs, index=False)
    return None

def handle_faqs(df):
    try:
        df["word_count"] = df["answer"].apply(lambda text: len(text.split()))
        df = df[df['word_count'] <= 300]
        df = df.drop("word_count", axis=1)

        df = preprocess_text(df)
        df = summarize_text(df)
        embed_questions(df)
        save_file(df)

        return df

    except Exception as e:
        raise ValueError(f"An error occurred while preprocessing FAQs: {e}")
