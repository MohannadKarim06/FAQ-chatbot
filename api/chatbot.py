import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.semantic_search import search_faq
from models.mistral_model import model_response
from logs.logger import log_event

conversation_history = [] 


def chat_with_bot(prompt, faq_source):
    
   try:
      retrieved_answer, score = search_faq(query=prompt, faq_source=faq_source)
   except Exception as e:
      log_event("ERROR", f"an error happend while searching faqs: {e}")
   

   formatted_history = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in conversation_history])

   if score < 1:
      relevance_score = "High Relevance"
   elif score < 1.5:
      relevance_score= "Medium Relevance"
   else:
      relevance_score = "Low Relevance"

   instructions = f"""
You are a helpful assistant that answers user questions using a FAQ.

Only use the provided FAQ answer. If it’s not relevant, say: "Sorry, I couldn’t find an answer in the FAQs."

---

History: {formatted_history}
Question: {prompt}
FAQ: {retrieved_answer}

Answer:
""".strip()
   
   try:
      response = model_response(instructions)
   except Exception as e:
      log_event("ERROR", f"an error occured while getting model response: {e}")
    
   conversation_history.append({"user": prompt, "bot": response})
   
   log_event("HISTORY", conversation_history)


   return response, score













