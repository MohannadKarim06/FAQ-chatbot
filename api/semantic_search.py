from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss
import numpy as np
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ConfigManger
from logs.logger import log_event
import os

config = ConfigManger()

model_name = config.get_embeddings_model_name()
model = SentenceTransformer(model_name)


default_faq_path = config.get_default_faqs_file()
uploaded_faq_path = config.get_uploaded_faqs_file()
default_index_path = config.get_default_faqs_faiss_index()
uploaded_index_path = config.get_uploaded_faqs_faiss_index()

def search_faq(query, faq_source):
    try:
        if faq_source == "default":
            if not os.path.exists(default_faq_path):
                raise ValueError("Default FAQ file not found.")
            df = pd.read_csv(default_faq_path)
            index_path = default_index_path
        elif faq_source == "uploaded":
            if not os.path.exists(uploaded_faq_path):
                return None, 0  
            df = pd.read_csv(uploaded_faq_path)
            index_path = uploaded_index_path
        else:
            raise ValueError("Invalid FAQ source. Choose 'default' or 'uploaded'.")

        
        if not os.path.exists(index_path):
            return None, 0  

        # Load FAISS index
        index = faiss.read_index(index_path)

        # Encode the query
        query_embedding = model.encode([query])
        query_embedding = np.array(query_embedding, dtype="float32")

        # Search the index
        distances, indices = index.search(query_embedding, k=1)  

        # Retrieve answer
        faq_answers = df["answer"].tolist()
        retrieved_answer = faq_answers[indices[0][0]] if len(indices[0]) > 0 else None
        score = distances[0][0] if len(distances[0]) > 0 else 0  

        log_event("SEARCH", f"Query: {query}, Answer: {retrieved_answer}, Score: {score}")

        return retrieved_answer, score

    except Exception as e:
        log_event("Error", f"An error occurred while searching FAQs index: {e}")
        return None, 0  
