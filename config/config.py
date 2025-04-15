import yaml
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ConfigManger:
    def __init__(self, config_path=None):
        # Always use absolute path for Docker compatibility
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "config.yaml")

        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            raise FileNotFoundError(f"Could not load config file at {config_path}: {e}")

    def get_default_faqs_file(self):
        return self.config["data"]["default_faqs"]

    def get_uploaded_faqs_file(self):
        return self.config["data"]["uploaded_faqs"]

    def get_hf_api_key(self):
        return os.getenv("HF_API_KEY")

    def get_embeddings_model_name(self):
        return self.config["models"]["embeddings_model"]

    def get_chatbot_model_name(self):
        return self.config["models"]["chatbot_model"]

    def get_uploaded_faqs_faiss_index(self):
        return self.config["data"]["uploaded_faqs_embedddings"]

    def get_default_faqs_faiss_index(self):
        return self.config["data"]["default_faqs_embedddings"]
