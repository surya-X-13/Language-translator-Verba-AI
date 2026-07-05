from langchain_core.prompts import ChatPromptTemplate

translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert translator and language identifier.

Analyze the user's text, identify its source language, and translate it into the target language.

You must respond ONLY with a JSON object in this exact format:
{{
    "detected_language": "<Name of the language detected in the input text, capitalized e.g. English, French, Spanish>",
    "translated_text": "<The translation of the input text>"
}}

Do not include any markdown formatting (like ```json), explanations, or text outside the JSON.
"""
        ),
        (
            "human",
            """
Target Language:
{language}

Text:
{text}
"""
        )
    ]
)