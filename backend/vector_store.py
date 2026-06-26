"""
Clean ChromaDB vector store (WORKING FIXED VERSION)
"""

from pathlib import Path
from typing import List

import chromadb
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from backend.embeddings import get_embeddings

CHROMA_DB_PATH = str(Path(__file__).parent.parent / "data" / "chroma_db")
COLLECTION_NAME = "rag_documents"


def get_vector_store():
    """
    Safe ChromaDB init (avoids tenant error)
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    return Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
    )


def add_documents(documents: List[Document], file_name: str) -> int:
    vs = get_vector_store()

    # tag metadata
    for doc in documents:
        doc.metadata["source"] = file_name

    vs.add_documents(documents)
    return len(documents)


def get_retriever(k: int = 4):
    vs = get_vector_store()
    return vs.as_retriever(search_kwargs={"k": k})


def list_indexed_files():
    vs = get_vector_store()
    data = vs.get(include=["metadatas"])

    if not data or not data.get("metadatas"):
        return []

    return sorted({
        m.get("source", "")
        for m in data["metadatas"]
        if m and m.get("source")
    })


def delete_file(file_name: str) -> int:
    vs = get_vector_store()

    # get all chunks for this file
    result = vs.get(where={"source": file_name})

    ids = result.get("ids") or []

    if not ids:
        return 0

    # delete from chroma
    vs.delete(ids=ids)

    return len(ids)