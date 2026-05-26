# CDN Runbook Assistant 

A RAG-powered chatbot that answers questions about AWS CloudFront
grounded in real AWS documentation. Built using Python, 
Anthropic Claude API, and ChromaDB.

## Project Overview

This project demonstrates a production-ready RAG 
(Retrieval-Augmented Generation) pipeline that:
- Ingests AWS CloudFront documentation (PDF)
- Chunks and embeds content into a local vector database
- Retrieves relevant context based on user queries
- Generates accurate, grounded answers using Claude API

## Architecture

User Query → Embed Query → ChromaDB Search → Retrieve Top 5 Chunks
→ Augmented Prompt → Claude API → Grounded Answer

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python 3 |
| LLM | Anthropic Claude (claude-sonnet-4-5) |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| PDF Processing | pypdf |
| Environment | python-dotenv |

## Project Structure

cdn-runbook-assistant/
├── ingest.py        # Phase 2: Chunk, embed and store docs
├── rag.py           # Phase 3: RAG query pipeline
├── chatbot.py       # Phase 4: Interactive CLI chatbot
├── docs/            # AWS CloudFront documentation PDF
└── README.md

## Getting Started

### Prerequisites
- Python 3
- Anthropic API key (console.anthropic.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cdn-runbook-assistant.git
cd cdn-runbook-assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install anthropic chromadb sentence-transformers pypdf python-dotenv
```

### Configuration

```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### Build Knowledge Base

```bash
# Download AWS CloudFront Developer Guide PDF into docs/ folder
# Then run ingestion
python3 ingest.py
```

### Run Chatbot

```bash
python3 chatbot.py
```

## Example Queries

- "What is the default TTL for static objects in CloudFront?"
- "How do I invalidate cache in CloudFront?"
- "What are CloudFront origins?"
- "How do I set up an origin group for high availability?"

## Key Concepts Demonstrated

- **RAG Architecture** — Retrieval-Augmented Generation pipeline
- **Vector Embeddings** — Semantic search using sentence-transformers
- **Prompt Engineering** — Grounded prompts to prevent hallucination
- **Claude API Integration** — Anthropic SDK for LLM inference
- **Vector Database** — ChromaDB for efficient similarity search

## Author

Pravanjana — Solutions Architect | CDN Specialist
AWS SAA-C03 | Azure AZ-104
