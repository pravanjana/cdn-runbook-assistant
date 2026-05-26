from rag import ask

def main():
    print("="*50)
    print("CDN Runbook Assistant")
    print("Powered by Claude + ChromaDB")
    print("="*50)
    print("Ask me anything about AWS CloudFront!")
    print("Type 'exit' to quit.")
    print("="*50)

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print()
        answer = ask(user_input)
        print(f"Assistant: {answer}")
        print()
        print("-"*50)

if __name__ == "__main__":
    main()
