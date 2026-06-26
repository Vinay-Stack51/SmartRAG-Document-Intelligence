"""
text_splitter.py — Chunking logic using LangChain RecursiveCharacterTextSplitter
"""

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Chunk config — tuned for RAG with Groq's llama3-8b context window
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Splits a list of Documents into smaller chunks.

    Uses RecursiveCharacterTextSplitter which tries to split on:
    paragraph → sentence → word → character (in that order), preserving
    semantic meaning better than a fixed-size splitter.

    Args:
        documents: List of raw LangChain Document objects

    Returns:
        List of chunked Document objects
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    # Filter out empty or whitespace-only chunks
    chunks = [c for c in chunks if c.page_content.strip()]

    return chunks
