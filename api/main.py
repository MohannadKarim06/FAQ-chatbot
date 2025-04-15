from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from langdetect import detect
import sys, os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.chatbot import chat_with_bot
from api.faq_handler import handle_faqs
from api.translation import translate_to_arabic, translate_to_english
from logs.logger import log_event

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploaded_faq_data = None

class ChatRequest(BaseModel):
    user_input: str
    faq_source: str

@app.post("/chat/")
def chat_endpoint(request: ChatRequest):
    user_input = request.user_input
    faq_source = request.faq_source

    try:
        lang = detect(user_input)
    except Exception as e:
        log_event("ERROR", f"Error detecting language: {e}")
        lang = "en"

    log_event("QUERY", f"User input: {user_input}")

    try:
        if lang == "ar":
            user_input = translate_to_english(user_input)
    except Exception as e:
        log_event("ERROR", f"Error translating to English: {e}")

    try:
        response, score = chat_with_bot(prompt=user_input, faq_source=faq_source)
    except Exception as e:
        log_event("ERROR", f"Error chatting with bot: {e}")
        response = "An error occurred while processing your request."
        score = None

    try:
        if lang == "ar":
            response = translate_to_arabic(response)
    except Exception as e:
        log_event("ERROR", f"Error translating to Arabic: {e}")

    log_event("RESPONSE", f"Bot response: {response}")

    return {
        "response": response,
        "score": f"{score}"
    }

@app.post("/upload_faq/")
async def upload_faq(file: UploadFile = File(...)):
    global uploaded_faq_data

    try:
        file_content = await file.read()
        df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))
        log_event("PREPROCESS", "Uploaded FAQ file is being processed")
        uploaded_faq_data = handle_faqs(df)

        return {"message": "FAQ file uploaded and processed successfully"}

    except Exception as e:
        log_event("ERROR", f"Error processing uploaded FAQ: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
