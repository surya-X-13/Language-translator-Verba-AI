from langchain_core.prompts import ChatPromptTemplate

detection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert language identifier.
Analyze the user's input text and identify its primary language.
Respond with ONLY the name of the language (e.g., 'English', 'Spanish', 'French', etc.). 
Do not include any introductory text, markdown, explanation, or punctuation.
"""
        ),
        (
            "human",
            "{text}"
        )
    ]
)

translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert translator.
Translate the user's text into the target language.
Preserve all formatting, paragraphs, whitespace, and layout from the original text.
Respond with ONLY the translated text. Do not add any introductory text, explanations, notes, or markdown code blocks (such as ```).
"""
        ),
        (
            "human",
            """
Target Language: {language}

Text:
{text}
"""
        )
    ]
)