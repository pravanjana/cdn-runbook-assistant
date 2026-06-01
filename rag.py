import os
from dotenv import load_dotenv
import chromadb
import anthropic

load_dotenv()

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="cloudfront_docs")
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def retrieve_chunks(query, top_k=5):
    print(f"Retrieving top {top_k} relevant chunks...")
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    chunks = results['documents'][0]
    return chunks

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

def ask(query):
    chunks = retrieve_chunks(query)
    answer = generate_answer(query, chunks)
    return answer

if __name__ == "__main__":
    question = "What is CloudFront and how does it work?"
    print(f"\nQuestion: {question}")
    print("\nAnswer:")
    print(ask(question))
