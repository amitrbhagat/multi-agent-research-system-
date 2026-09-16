from app.rag.vector_store import retrieve_candidates
from app.rag.hybrid_retrieval import hybrid_retrieve

TEST_QUERIES = [
    "What is the main topic of the documents?",
    "What specific numbers or statistics are mentioned?",
    "What methodology was used?",
]


def test_compare_before_after_reranking():
    for query in TEST_QUERIES:
        raw_results = retrieve_candidates(query, candidates_k=5)
        reranked_results = hybrid_retrieve(query, top_n=5)

        print(f"\n=== Query: {query} ===")
        print("-- BEFORE (raw vector top-5) --")
        for r in raw_results:
            print(f"  {r['content'][:100]}...")

        print("-- AFTER (hybrid + re-ranked top-5) --")
        for r in reranked_results:
            print(f"  {r['content'][:100]}...")

    assert True  # manual review test