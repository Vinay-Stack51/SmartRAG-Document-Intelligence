"""
rag_pipeline.py — Core RAG logic: retrieve relevant chunks → send to Groq → return answer
"""

from typing import List, Tuple
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from backend.llm import get_llm
from backend.vector_store import get_retriever

# RAG system prompt — instructs the LLM to stay grounded in retrieved context
RAG_PROMPT_TEMPLATE = """You are a helpful AI assistant. Answer the user's question based ONLY on the provided context from their uploaded documents.

If the answer is not found in the context, say: "I couldn't find relevant information in the uploaded documents to answer this question."

Do not use your general knowledge — only the provided context.

Context:
{context}

Question: {question}

Answer:"""


def format_docs(docs: List[Document]) -> str:
    """Concatenates retrieved document chunks into a single context string."""
    return "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )


def get_rag_chain():
    """
    Builds and returns the full RAG chain:
    question → retriever → prompt → LLM → answer (string)
    """
    retriever = get_retriever(k=4)
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    parser = StrOutputParser()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )

    return chain


def query_rag(question: str) -> Tuple[str, List[Document]]:
    """
    Run a question through the RAG pipeline.

    Args:
        question: User's natural language question

    Returns:
        Tuple of (answer string, list of source Documents used)
    """
    retriever = get_retriever(k=4)
    chain = get_rag_chain()

    # Get source docs separately for display in the UI
    source_docs = retriever.invoke(question)
    answer = chain.invoke(question)

    return answer, source_docs
