import os
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# Load environment variables
load_dotenv()

# Step 1: READ - Extract text from PDF
def read_pdf(file_path):
    print(f"Reading PDF: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(f"Total characters extracted: {len(text)}")
    return text

# Step 2: CHUNK - Split text into smaller pieces
def chunk_text(text, chunk_size=500, overlap=50):
    print("Chunking text...")
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    print(f"Total chunks created: {len(chunks)}")
    return chunks

# Step 3 & 4: EMBED and STORE into ChromaDB
def embed_and_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="cloudfront_docs")

    print("Embedding and storing chunks...")
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
        if i % 100 == 0:
            print(f"Stored {i}/{len(chunks)} chunks...")

    print(f"Done! Total chunks stored: {len(chunks)}")

# Main execution
if __name__ == "__main__":
    pdf_path = "docs/AmazonCloudFront_DevGuide.pdf"
    text = read_pdf(pdf_path)
    chunks = chunk_text(text)
    embed_and_store(chunks)
    print("Ingestion complete! Knowledge base is ready.")
