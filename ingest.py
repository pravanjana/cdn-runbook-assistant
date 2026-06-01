import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb

load_dotenv()

def read_pdf(file_path):
    print(f"Reading PDF: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(f"Total characters extracted: {len(text)}")
    return text

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

def embed_and_store(chunks, doc_prefix):
    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="cloudfront_docs")

    print("Storing chunks...")
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{doc_prefix}_chunk_{i}"]
        )
        if i % 100 == 0:
            print(f"Stored {i}/{len(chunks)} chunks...")

    print(f"Done! Total chunks stored: {len(chunks)}")

if __name__ == "__main__":
    pdf_files = [
        ("docs/AmazonCloudFront_DevGuide.pdf", "cloudfront"),
        ("docs/waf-dg.pdf", "waf"),
        ("docs/AWS-s3-userguide.pdf", "s3")
    ]

    for pdf_path, prefix in pdf_files:
        print(f"\nProcessing: {pdf_path}")
        text = read_pdf(pdf_path)
        chunks = chunk_text(text)
        embed_and_store(chunks, prefix)

    print("\nAll documents ingested! Knowledge base is ready.")
