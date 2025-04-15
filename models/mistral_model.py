import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logs.logger import log_event

API_URL = "https://api.together.xyz/v1/chat/completions"
API_KEY = os.getenv("API_KEY")  # replace with your Together API key

def model_response(prompt: str, instructions: str = None):
    try:
        messages = []

        if instructions:
            messages.append({"role": "system", "content": instructions})
        
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "messages": messages,
            "temperature": 0.1,
            "top_p": 0.95,
            "max_tokens": 256,
            "repetition_penalty": 1.1
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            log_event("ERROR", f"Together AI API Error: {response.status_code} {response.text}")
            raise Exception(f"Together AI API Error: {response.status_code} {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        log_event("ERROR", f"Failed to get response from Together AI: {e}")
        return "Sorry, something went wrong getting a response from the model."
