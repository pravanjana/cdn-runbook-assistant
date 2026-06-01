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

if collection.count() == 0:
    st.info("🔄 First time setup — building knowledge base. This may take a few minutes...")
    from ingest import read_pdf, chunk_text, embed_and_store
    pdf_files = [
        "docs/AmazonCloudFront_DevGuide.pdf",
        "docs/waf-dg.pdf",
        "docs/AWS-s3-userguide.pdf"
    ]
    for pdf_path in pdf_files:
        text = read_pdf(pdf_path)
        chunks = chunk_text(text)
        embed_and_store(chunks)
    st.success("✅ Knowledge base ready!")
    st.rerun()

from rag import ask

st.set_page_config(
    page_title="AWS Edge Services Assistant",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AWS Edge Services Assistant")
st.caption("Powered by Claude + ChromaDB | Ask me anything about CloudFront, WAF & S3!")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about CloudFront, WAF or S3..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating answer..."):
            answer = ask(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
