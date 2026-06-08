import os
import sys
import subprocess
import streamlit as st
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="cloudfront_docs")

if collection.count() < 10000:
    st.info("🔄 Building knowledge base. This may take a few minutes...")
    result = subprocess.run(
        [sys.executable, "ingest.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        st.success("✅ Knowledge base ready!")
        st.rerun()
    else:
        st.error(f"Ingestion failed: {result.stderr}")

from rag import ask

st.set_page_config(
    page_title="CDN Runbook Assistant",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 CDN Runbook Assistant")
st.caption("Powered by Claude + ChromaDB | Ask me anything about AWS CloudFront & WAF!")
st.divider()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show remaining questions
remaining = 10 - st.session_state.question_count
if remaining > 0:
    st.caption(f"💬 {remaining} questions remaining in this session")
else:
    st.warning("⚠️ Session limit of 10 questions reached. Please refresh to start a new session.")
    st.stop()

# Chat input
if prompt := st.chat_input("Ask a question about CloudFront or WAF..."):
    st.session_state.question_count += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating answer..."):
            answer = ask(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
