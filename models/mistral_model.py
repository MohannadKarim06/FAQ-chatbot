'''
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import InferenceClient
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import ConfigManger
from huggingface_hub import InferenceClient

config = ConfigManger()

model_name = config.get_chatbot_model_name()
HF_API_KEY = config.get_hf_api_key()
client = InferenceClient(model=model_name, token=HF_API_KEY)


def model_response(instructions):
    full_prompt = instructions
    response = client.text_generation(full_prompt, max_new_tokens=200)

    return response    
'''

import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logs.logger import log_event

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def model_response(text: str):
    
    full_prompt = text
    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 200,
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


