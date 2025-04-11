from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from api.chatbot import chat_with_bot
from faq_handler import handle_faqs
from translation import translate_to_arabic, translate_to_english
from logs.logger import log_event
from langdetect import detect
import io
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()

uploaded_faq_data = None  

class ChatRequest(BaseModel):
    user_input: str
    faq_source: str


@app.post("/chat/")
def chat_endpoint(request: ChatRequest):

        user_input = request.user_input
        faq_source = request.faq_source

        lang = 1

        log_event("QUERY", f"User input: {user_input}")

        if lang == "ar":
            user_input = translate_to_english(user_input)
        
        response, score = chat_with_bot(prompt=user_input, faq_source=faq_source)

        if lang == "ar":
            response = translate_to_arabic(response)

        log_event("RESPONSE", f"Bot response: {response}")

        return {
            "response": response,
            "score": score
        } 

    

@app.post("/upload_faq/")
async def upload_faq(file: UploadFile = File(...)):
    global uploaded_faq_data

    try:
        # Read file content
        file_content = await file.read()

        # Convert bytes to a Pandas DataFrame
        df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))

        log_event("PREPROCESS", "Uploaded FAQ file is being processed")

        # Process the FAQ data
        uploaded_faq_data = handle_faqs(df)

        return {"message": "FAQ file uploaded and processed successfully"}

    except Exception as e:
        log_event("ERROR", f"An error occurred while processing FAQs: {e}")
        raise HTTPException(status_code=500, detail=str(e))  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
