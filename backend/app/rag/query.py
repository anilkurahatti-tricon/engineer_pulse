from app.rag.rag_service import RAGService


def main():
    rag = RAGService()

    print("=" * 60)
    print("Engineer Pulse - RAG Query")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:
        query = input("\nQuestion: ").strip()

        if query.lower() == "exit":
            print("Exiting...")
            break

        if not query:
            continue

        result = rag.retrieve(
            query=query,
            top_k=3,
        )

        print("\nRetrieved Results")
        print("-" * 60)

        for index, item in enumerate(
            result["results"],
            start=1,
        ):
            print(f"\nResult {index}")
            print(f"ID       : {item['id']}")
            print(f"Distance : {item['distance']}")
            print(f"Source   : {item['metadata'].get('source')}")
            print(f"\nContent:\n{item['content']}")


if __name__ == "__main__":
    main()