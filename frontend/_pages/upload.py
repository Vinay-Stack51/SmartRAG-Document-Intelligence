"""
upload.py — Document upload page for the RAG app
"""

import streamlit as st
from backend.document_loader import load_document
from backend.text_splitter import split_documents
from backend.vector_store import add_documents, list_indexed_files, delete_file


def render_upload_page():
    st.markdown("## 📂 Upload Documents")
    st.markdown(
        "Upload PDF, DOCX, or TXT files. Each file is chunked and stored in the "
        "vector database. Already-indexed files are skipped automatically."
    )

    # ── File uploader ──────────────────────────────────────────────────────────
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files at once.",
    )

    if uploaded_files:
        if st.button("⚡ Index Documents", type="primary", use_container_width=True):
            for uploaded_file in uploaded_files:
                with st.status(f"Processing **{uploaded_file.name}**...", expanded=True) as status:
                    try:
                        st.write("📄 Extracting text...")
                        docs = load_document(uploaded_file)

                        st.write(f"✂️ Splitting into chunks...")
                        chunks = split_documents(docs)

                        st.write(f"🧠 Generating embeddings & storing in ChromaDB...")
                        added = add_documents(chunks, uploaded_file.name)

                        if added == 0:
                            status.update(
                                label=f"⏭️ **{uploaded_file.name}** — already indexed, skipped.",
                                state="complete",
                            )
                        else:
                            status.update(
                                label=f"✅ **{uploaded_file.name}** — {added} chunks indexed.",
                                state="complete",
                            )
                    except Exception as e:
                        status.update(
                            label=f"❌ Failed to process **{uploaded_file.name}**",
                            state="error",
                        )
                        st.error(str(e))

    # ── Indexed files list ─────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 🗂️ Indexed Documents")

    indexed = list_indexed_files()

    if not indexed:
        st.info("No documents indexed yet. Upload files above to get started.")
        return

    for fname in indexed:
        col1, col2 = st.columns([5, 1])
        col1.markdown(f"📄 `{fname}`")
        if col2.button("🗑️", key=f"del_{fname}", help=f"Remove {fname}"):
            removed = delete_file(fname)
            st.success(f"Removed **{fname}** ({removed} chunks deleted).")
            st.rerun()
