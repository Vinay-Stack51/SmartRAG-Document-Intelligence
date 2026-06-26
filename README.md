# 🧠 DocMind — Production-Ready RAG Application

A full-stack Retrieval Augmented Generation (RAG) app that lets you upload documents and chat with them using Groq's LLaMA 3.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| LLM | Groq API (`llama3-8b-8192`) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (local, free) |
| Vector DB | ChromaDB (persistent, local) |
| Framework | LangChain |
| File Support | PDF, DOCX, TXT |

---

## Project Structure

```
AI_RAG_APP/
├── backend/
│   ├── llm.py              # Groq LLM integration
│   ├── embeddings.py       # HuggingFace embedding model
│   ├── vector_store.py     # ChromaDB manager
│   ├── document_loader.py  # PDF / DOCX / TXT loader
│   ├── text_splitter.py    # Chunking logic
│   └── rag_pipeline.py     # Core RAG chain
├── frontend/
│   ├── app.py              # Main Streamlit app
│   └── _pages/
│       ├── upload.py       # Upload UI
│       └── chat.py         # Chat UI
├── data/
│   ├── chroma_db/          # Vector DB storage (auto-created)
│   └── uploads/            # (optional file cache)
├── .env                    # Your GROQ_API_KEY
├── requirements.txt
├── run.py                  # Launch script
└── README.md
```

---

## Setup

### 1. Get a Groq API Key
Sign up at [https://console.groq.com](https://console.groq.com) — it's free.

### 2. Clone / download this project
git clone 

### 3. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your API key
Edit `.env`:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 6. Run the app
```bash
python run.py
```
Or directly:
```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How It Works

```
Upload → Extract Text → Chunk (800 chars, 150 overlap)
       → Embed (MiniLM) → Store in ChromaDB

User Query → Retrieve Top-4 Chunks → Build Prompt
           → Send to Groq LLaMA 3 → Stream Answer
```

### Key Features
- **No re-indexing**: Files already in ChromaDB are detected and skipped
- **Source transparency**: Each answer shows which chunks it used
- **Multi-file support**: Index and query multiple documents simultaneously
- **Delete documents**: Remove indexed files from the sidebar
- **Persistent storage**: ChromaDB data survives app restarts

---

## Notes

- Embeddings use `all-MiniLM-L6-v2` which runs **locally** — no extra API key needed
- The model downloads once (~90 MB) and is cached by HuggingFace
- ChromaDB stores data in `data/chroma_db/` — delete this folder to reset the index
- Groq's free tier handles high request volumes with fast inference
