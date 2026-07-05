from fastapi import FastAPI
from pydantic import BaseModel

from translator import translate

app = FastAPI(title="Language Translator")

from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    target_language: Optional[str] = None
    language: Optional[str] = None

@app.post("/translate")
def translate_api(req: TranslationRequest):
    target = req.target_language or req.language or "English"
    result = translate(
        req.text,
        target
    )

    return {
        "detected_language": result.get("detected_language", "Detect Language"),
        "translated_text": result.get("translated_text", "")
    }