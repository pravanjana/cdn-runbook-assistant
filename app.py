import os
import sys
import subprocess
import streamlit as st
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="cloudfront_docs")

st.sidebar.write(f"📊 Knowledge base chunks: {collection.count()}")

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

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about CloudFront or WAF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating answer..."):
            answer = ask(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
