import yaml
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ConfigManger:
    def __init__(self, confing_path="config/config.yaml"):
        with open(confing_path, "r") as f:
            self.config = yaml.safe_load(f)
    
    
    def get_default_faqs_file(self):
        default_faq_data_path = self.config["data"]["default_faqs"]
        default_faq = r"{}".format(default_faq_data_path)
        return default_faq
    

    def get_uploaded_faqs_file(self):
        uploaded_faqs_path = self.config["data"]["uploaded_faqs"]
        uploaded_faqs = r"{}".format(uploaded_faqs_path)
        return uploaded_faqs
    

    def get_hf_api_key(self):
        hf_api_key = os.getenv("HF_API_KEY")
        return hf_api_key
    

    def get_embeddings_model_name(self):
        embeddings_model_name = self.config["models"]["embeddings_model"]
        return embeddings_model_name


    def get_chatbot_model_name(self):
        chatbot_model_name = self.config["models"]["chatbot_model"]
        return chatbot_model_name
    

    def get_uploaded_faqs_faiss_index(self):
        uploaded_faqs_index = self.config["data"]["uploaded_faqs_embedddings"]
        uploaded_faqs_index = r"{}".format(uploaded_faqs_index)
        return uploaded_faqs_index
    

    def get_default_faqs_faiss_index(self):
        default_faqs_embedddings = self.config["data"]["default_faqs_embedddings"]
        default_faqs_embedddings = r"{}".format(default_faqs_embedddings)
        return default_faqs_embedddings
    


