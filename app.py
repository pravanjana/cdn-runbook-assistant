import os
import streamlit as st
from dotenv import load_dotenv
import chromadb

load_dotenv()

def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="cloudfront_docs")
    return collection

collection = get_collection()

st.sidebar.write(f"📊 Knowledge base chunks: {collection.count()}")

existing = collection.get(limit=1)
needs_rebuild = (
    len(existing['ids']) == 0 or
    not existing['ids'][0].startswith(('cloudfront_', 'waf_')) or
    collection.count() < 10000
)

if needs_rebuild:
    st.info("🔄 Building knowledge base. This may take a few minutes...")
    client = chromadb.PersistentClient(path="./chroma_db")
    client.delete_collection(name="cloudfront_docs")
    collection = client.get_or_create_collection(name="cloudfront_docs")
    from ingest import read_pdf, chunk_text, embed_and_store
    pdf_files = [
        ("docs/AmazonCloudFront_DevGuide.pdf", "cloudfront"),
        ("docs/waf-dg.pdf", "waf")
    ]
    for pdf_path, prefix in pdf_files:
        st.info(f"📄 Processing {pdf_path}...")
        text = read_pdf(pdf_path)
        chunks = chunk_text(text)
        embed_and_store(chunks, prefix)
    st.success("✅ Knowledge base ready!")
    st.rerun()

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
