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
