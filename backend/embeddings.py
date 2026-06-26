"""
embeddings.py — Embedding model setup (HuggingFace, runs locally, no API key needed)
"""

from langchain_huggingface import HuggingFaceEmbeddings

# Singleton — created once and reused across the app
_embedding_model = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Returns a singleton HuggingFace embedding model.
    Uses all-MiniLM-L6-v2: fast, lightweight, and great for RAG.
    Downloads the model on first run (~90 MB), then caches it locally.
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embedding_model
