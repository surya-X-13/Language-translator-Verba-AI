import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from prompt import translation_prompt, detection_prompt

load_dotenv()

detect_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=50
)

translation_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=4096
)

detection_chain = detection_prompt | detect_llm
translation_chain = translation_prompt | translation_llm

def chunk_text(text, max_chunk_size=1500):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_size = 0
    for p in paragraphs:
        p_len = len(p)
        if p_len + current_size > max_chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_size = p_len
        else:
            current_chunk.append(p)
            current_size += p_len + 2  # account for \n\n
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks

def translate(text, language):
    if not text:
        return {
            "detected_language": "Detect Language",
            "translated_text": ""
        }

    # Step 1: Detect language using the first 1000 characters of the input text
    sample_text = text[:1000]
    try:
        detect_response = detection_chain.invoke({"text": sample_text})
        detected_language = detect_response.content.strip().strip("'\"`.- ")
        # Fallback to a default if language detection output is long or invalid
        if not detected_language or len(detected_language) > 50:
            detected_language = "Detect Language"
    except Exception:
        detected_language = "Detect Language"

    # Step 2: Chunk the input text and translate each chunk
    chunks = chunk_text(text, max_chunk_size=1500)
    translated_chunks = []
    
    for chunk in chunks:
        try:
            translation_response = translation_chain.invoke(
                {
                    "text": chunk,
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
                
            translated_chunks.append(translated_text)
        except Exception as e:
            translated_chunks.append(f"[Translation of chunk failed: {str(e)}]")

    return {
        "detected_language": detected_language,
        "translated_text": "\n\n".join(translated_chunks)
    }