import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from prompt import translation_prompt, detection_prompt

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

detection_chain = detection_prompt | llm
translation_chain = translation_prompt | llm

def translate(text, language):
    # Step 1: Detect language using the first 1000 characters of the input text
    sample_text = text[:1000] if text else ""
    try:
        detect_response = detection_chain.invoke({"text": sample_text})
        detected_language = detect_response.content.strip().strip("'\"`.- ")
        # Fallback to a default if language detection output is long or invalid
        if not detected_language or len(detected_language) > 50:
            detected_language = "Detect Language"
    except Exception:
        detected_language = "Detect Language"

    # Step 2: Translate the entire text
    try:
        translation_response = translation_chain.invoke(
            {
                "text": text,
                "language": language
            }
        )
        translated_text = translation_response.content.strip()
        
        # Strip any markdown code fences that the model might wrap the translation in
        if translated_text.startswith("```"):
            lines = translated_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            translated_text = "\n".join(lines).strip()
            
    except Exception as e:
        translated_text = f"Translation failed: {str(e)}"

    return {
        "detected_language": detected_language,
        "translated_text": translated_text
    }