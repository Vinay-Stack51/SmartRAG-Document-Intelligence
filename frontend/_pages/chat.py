"""
chat.py — ChatGPT-style chat interface for the RAG app
"""

import streamlit as st
from backend.rag_pipeline import query_rag
from backend.vector_store import list_indexed_files


def render_chat_page():
    st.markdown("## 💬 Chat with Your Documents")

    # Warn if no documents are indexed
    indexed = list_indexed_files()
    if not indexed:
        st.warning(
            "⚠️ No documents indexed yet. Go to the **Upload** page to add files first."
        )
        return

    st.markdown(
        f"**{len(indexed)} document(s) loaded:** "
        + ", ".join(f"`{f}`" for f in indexed)
    )
    st.divider()

    # ── Session state init ─────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── Render message history ─────────────────────────────────────────────────
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📎 Source chunks used", expanded=False):
                    for i, src in enumerate(msg["sources"], 1):
                        st.markdown(
                            f"**Chunk {i}** — `{src.metadata.get('source', 'unknown')}`"
                            + (f", page {src.metadata['page']}" if "page" in src.metadata else "")
                        )
                        st.caption(src.page_content[:400] + ("..." if len(src.page_content) > 400 else ""))

    # ── Chat input ─────────────────────────────────────────────────────────────
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, sources = query_rag(prompt)
                    st.markdown(answer)

                    if sources:
                        with st.expander("📎 Source chunks used", expanded=False):
                            for i, src in enumerate(sources, 1):
                                st.markdown(
                                    f"**Chunk {i}** — `{src.metadata.get('source', 'unknown')}`"
                                    + (f", page {src.metadata['page']}" if "page" in src.metadata else "")
                                )
                                st.caption(src.page_content[:400] + ("..." if len(src.page_content) > 400 else ""))

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    })
                except Exception as e:
                    err_msg = f"❌ Error: {str(e)}"
                    st.error(err_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": err_msg,
                    })

    # ── Clear chat button ──────────────────────────────────────────────────────
    if st.session_state.messages:
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
