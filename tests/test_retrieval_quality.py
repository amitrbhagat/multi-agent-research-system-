from app.rag.vector_store import retrieve_local_context

SAMPLE_QUERIES = [
    "What is the main topic of the documents?",
    "Summarize the key findings",
    "What methodology was used?",
    "What are the limitations mentioned?",
    "What conclusions were drawn?",
]


def test_manual_retrieval_relevance():
    for query in SAMPLE_QUERIES:
        results = retrieve_local_context(query, top_k=3)
        print(f"\nQuery: {query}")
        for i, doc in enumerate(results):
            print(f"  [{i}] source={doc['source']} content={doc['content'][:120]}...")

    # Not a strict assertion — this test exists to surface output for manual review
    assert True
