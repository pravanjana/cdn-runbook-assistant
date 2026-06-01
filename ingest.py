import os
from dotenv import load_dotenv
from pypdf import PdfReader
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
    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="cloudfront_docs")

    print("Storing chunks...")
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )
        if i % 100 == 0:
            print(f"Stored {i}/{len(chunks)} chunks...")

    print(f"Done! Total chunks stored: {len(chunks)}")

# Main execution
if __name__ == "__main__":
    pdf_files = [
    "docs/AmazonCloudFront_DevGuide.pdf",
    "docs/waf-dg.pdf",
    "docs/AWS-s3-userguide.pdf"
    ]
    
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path}")
        text = read_pdf(pdf_path)
        chunks = chunk_text(text)
        embed_and_store(chunks)

    print("Ingestion complete! Knowledge base is ready.")
