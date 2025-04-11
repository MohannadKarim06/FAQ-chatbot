from logs.logger import log_event
from deep_translator import GoogleTranslator
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


translator_en_ar = GoogleTranslator(source="en", target="ar")
translator_ar_en = GoogleTranslator(source="ar", target="en")

def translate_to_english(text):
    try:
        text = translator_ar_en(text)

        return text
    
    except Exception as e:
        log_event("Error", f"An error occured while translting to en: {e}")


def translate_to_arabic(text):
    try:
        text = translator_en_ar(text)

        return text
    except Exception as e:
        log_event("Error", f"An error occured while translting to ar: {e}")




