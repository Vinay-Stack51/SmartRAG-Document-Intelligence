
"""
llm.py — Groq LLM integration via LangChain
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm(
    model: str = "openai/gpt-oss-20b",
    temperature: float = 0.2
) -> ChatGroq:
    """
    Returns a configured Groq LLM instance.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please add it to your .env file."
        )

    return ChatGroq(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=2048,
    )
