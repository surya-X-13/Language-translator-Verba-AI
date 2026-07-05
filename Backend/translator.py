import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from prompt import translation_prompt

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

chain = translation_prompt | llm

import json

def translate(text, language):

    response = chain.invoke(
        {
            "text": text,
            "language": language
        }
    )

    content = response.content.strip()
    # Handle optional markdown block formatting that some models include
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        data = json.loads(content)
        return data
    except Exception as e:
        return {
            "detected_language": "Unknown",
            "translated_text": response.content
        }