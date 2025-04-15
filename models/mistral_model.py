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
            "temperature": 0.1,
            "top_p": 0.95,
            "max_new_tokens": 200,
            "repetition_penalty": 1.1
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        log_event("ERROR", f"Hugging Face API Error: {response.status_code} {response.text}")
        raise Exception(f"Hugging Face API Error: {response.status_code} {response.text}")

    try:
        output = response.json()
        generated_text = output[0].get("generated_text", "").strip()

        if generated_text.startswith(full_prompt):
            generated_text_processed = generated_text[len(full_prompt):].strip()
        else:
            generated_text_processed = generated_text

    except Exception as e:
        log_event("ERROR", f"An error occurred when processing model output: {e}")
        raise Exception("Failed to process response from model")

    return generated_text_processed
