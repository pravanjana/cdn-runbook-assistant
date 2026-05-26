import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
import anthropic

# Load environment variables
load_dotenv()

# Initialize clients
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="cloudfront_docs")
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Step 1: EMBED the user query
def embed_query(query):
    print(f"Embedding query: {query}")
    return embedding_model.encode(query).tolist()

# Step 2: RETRIEVE relevant chunks from ChromaDB
def retrieve_chunks(query_embedding, top_k=5):
    print(f"Retrieving top {top_k} relevant chunks...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    chunks = results['documents'][0]
    return chunks

# Step 3: GENERATE answer using Claude
def generate_answer(query, chunks):
    print("Generating answer with Claude...")
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful AWS CloudFront expert assistant.
Use the following documentation excerpts to answer the question.
If the answer is not in the provided context, say "I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""

    response = claude_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

# Main RAG pipeline
def ask(query):
    query_embedding = embed_query(query)
    chunks = retrieve_chunks(query_embedding)
    answer = generate_answer(query, chunks)
    return answer

# Test it
if __name__ == "__main__":
    question = "What is CloudFront and how does it work?"
    print(f"\nQuestion: {question}")
    print("\nAnswer:")
    print(ask(question))
