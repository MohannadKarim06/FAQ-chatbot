import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logs.logger import log_event

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def model_response(text: str):
    
    full_prompt = text
    payload = {
        "inputs": full_prompt,
        "parameters": {
            "temperature": 0.0,             # Fully deterministic, important for strictness
            "top_p": 0.95,
            "max_new_tokens": 200,
            "repetition_penalty": 1.1
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        log_event(f"Hugging Face API Error: {response.status_code} {response.text}")
        raise Exception(f"Hugging Face API Error: {response.status_code} {response.text}")

    output = response.json()
    generated_text = output[0]["generated_text"]  
    
    try:
        generated_text_processed = generated_text.replace(text, "").strip() 
    except Exception as e:
        log_event("ERROR", f"an error occured when processing model output: {e}")    

    return generated_text_processed


