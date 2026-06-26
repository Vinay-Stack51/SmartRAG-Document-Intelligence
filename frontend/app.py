"""
app.py — Main Streamlit application entry point
"""

import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartRAG Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0ff !important;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
    }

    /* Status boxes */
    [data-testid="stStatusWidget"] {
        border-radius: 10px;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.08);
    }

    /* Hide default Streamlit footer */
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("SmartRAG Document Intelligence")
    st.markdown("*RAG-powered document chat*")
    st.divider()

    page = st.radio(
        "Navigate",
        options=["📂 Upload Documents", "💬 Chat"],
        label_visibility="collapsed",
    )

    st.divider()

# ── Route to pages ─────────────────────────────────────────────────────────────
from frontend._pages.upload import render_upload_page
from frontend._pages.chat import render_chat_page

if page == "📂 Upload Documents":
    render_upload_page()
else:
    render_chat_page()
