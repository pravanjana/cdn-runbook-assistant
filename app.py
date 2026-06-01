import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Auto-ingest if chroma_db doesn't exist
if not os.path.exists("chroma_db"):
    st.info("🔄 First time setup — building knowledge base from CloudFront docs. This may take a few minutes...")
    from ingest import read_pdf, chunk_text, embed_and_store
    text = read_pdf("docs/AmazonCloudFront_DevGuide.pdf")
    chunks = chunk_text(text)
    embed_and_store(chunks)
    st.success("✅ Knowledge base ready!")
    st.rerun()

from rag import ask

# Page configuration
st.set_page_config(
    page_title="CDN Runbook Assistant",
    page_icon="🚀",
    layout="centered"
)

# Header
st.title("🚀 CDN Runbook Assistant")
st.caption("Powered by Claude + ChromaDB | Ask me anything about AWS CloudFront!")
st.divider()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about AWS CloudFront..."):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating answer..."):
            answer = ask(prompt)
        st.markdown(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})
