from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import faiss
import numpy as np
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import ConfigManger
from logs.logger import log_event

config = ConfigManger()

# Load HF model + tokenizer once
model_name = config.get_embeddings_model_name()
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

default_faq_path = config.get_default_faqs_file()
uploaded_faq_path = config.get_uploaded_faqs_file()
default_index_path = config.get_default_faqs_faiss_index()
uploaded_index_path = config.get_uploaded_faqs_faiss_index()

def get_embedding(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings.numpy().astype("float32")

def search_faq(query, faq_source):
    try:
        if faq_source == "default":
            if not os.path.exists(default_faq_path):
                raise ValueError("Default FAQ file not found.")
                log_event("ERROR", "Default FAQ file not found.")

            df = pd.read_csv(default_faq_path)
            index_path = default_index_path
        elif faq_source == "uploaded":
            if not os.path.exists(uploaded_faq_path):
                log_event("ERROR", "Uploaded FAQ file not found.")
                return None, 0  
                
            df = pd.read_csv(uploaded_faq_path)
            index_path = uploaded_index_path
        else:
            raise ValueError("Invalid FAQ source. Choose 'default' or 'uploaded'.")
            log_event("ERROR", "Invalid FAQ source. Choose 'default' or 'uploaded'.")
            
        if not os.path.exists(index_path):
            return None, 0  

        index = faiss.read_index(index_path)

        query_embedding = get_embedding([query])
        distances, indices = index.search(query_embedding, k=1)

        faq_answers = df["answer"].tolist()
        retrieved_answer = faq_answers[indices[0][0]] if len(indices[0]) > 0 else None
        score = distances[0][0] if len(distances[0]) > 0 else 0  

        log_event("SEARCH", f"Query: {query}, Answer: {retrieved_answer}, Score: {score}")

        return retrieved_answer, score

    except Exception as e:
        log_event("Error", f"An error occurred while searching FAQs index: {e}")
        return None, 0
