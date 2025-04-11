from semantic_search import search_faq
from models.mistral_model import model_response
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def chat_with_bot(prompt, faq_source):
    
    conversation_history = [] 

    # Retrieve FAQ answer
    retrieved_answer, score = search_faq(query=prompt, faq_source=faq_source)

    # Format history for the model
    formatted_history = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in conversation_history])

    # Select instructions based on confidence score
    if score < 2:
      instructions = f"""
You are an AI assistant that answers user questions conversationally.
You also have access to a knowledge base of FAQs. Your job is to:

1️⃣ **Handle small talk properly**:
   - If the user is engaging in small talk (e.g., greetings, casual conversation), respond naturally like a human assistant.
   - **Do not use the FAQ knowledge base** in small talk responses.

2️⃣ **Use the FAQ knowledge base appropriately**:
   - If the user asks an informational or support-related question, check the retrieved FAQ answer.
   - If the FAQ answer is relevant, rephrase it in a conversational way.
   - If the FAQ answer is **partially relevant**, provide the answer while adding additional useful context.
   - If the FAQ answer is **not relevant**, ignore it and answer using general knowledge.

3️⃣ **Keep track of the conversation**:
   - Consider previous interactions to make responses more natural.
   - Do not repeat information unnecessarily.

### 📜 Conversation History:
{formatted_history}

### 📌 User Question:
"{prompt}"

### 📝 Retrieved FAQ Answer:
"{retrieved_answer}" (Relevance Score: {score})

Now, generate your response following these rules.
"""

    else:
        instructions = f"""
        You are an AI assistant engaged in an ongoing conversation with The user.
        Below is the conversation history:
        {formatted_history}

        The user asked: "{prompt}"

        Your task
        - Provide a helpful response using general knowledge.
        - Maintain conversational flow and ask clarifying questions if needed.
        """

    
    response = model_response(instructions=instructions)

    
    conversation_history.append({"user": prompt, "bot": response})

    return response, score














