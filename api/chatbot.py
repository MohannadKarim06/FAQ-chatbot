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
        log_event("ERROR", f"An error occurred while searching FAQs: {e}")
        retrieved_answer, score = "No relevant FAQ found.", 0.0

    formatted_history = "\n".join([
        f"User: {msg['user']}\nBot: {msg['bot']}" for msg in conversation_history
    ])

    instructions = f"""
You are an AI assistant that helps users by engaging in conversation and answering support-related questions using a provided FAQ knowledge base.

🔸 Your behavior is as follows:

1️⃣ **Small Talk & Casual Conversation**:
- If the user greets you or engages in casual conversation, respond naturally and warmly.
- You can chat like a friendly assistant — jokes, comments, etc. — as long as it's not giving factual answers.
- ✅ Do **not** use the FAQ in these responses.

2️⃣ **FAQ-based Answering**:
- If the user asks a support, product, or policy-related question, use the **retrieved FAQ answer** only.
- Rephrase the FAQ answer in a natural way, but **do not add any new information**.
- ❌ Do **not** use external or general knowledge.
- If the FAQ answer doesn’t clearly answer the question, say:
  > "I’m sorry, I couldn’t find an answer to that in the FAQs."

3️⃣ **Conversation Context**:
- Use previous messages (below) to understand what the user is asking.
- Keep your tone friendly and concise.

---

### 💬 Conversation History:
{formatted_history}

### ❓ User Question:
"{prompt}"

### 📄 Retrieved FAQ Answer:
"{retrieved_answer}"

---

### 🗨️ Your Response:
"""

    try:
        response = model_response(prompt=prompt, instructions=instructions)
    except Exception as e:
        log_event("ERROR", f"An error occurred while getting model response: {e}")
        response = "Sorry, there was an error generating a response."

    conversation_history.append({"user": prompt, "bot": response})
    log_event("HISTORY", conversation_history)

    return response, score
