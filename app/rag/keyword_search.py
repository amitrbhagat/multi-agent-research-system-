from rank_bm25 import BM25Okapi

from app.rag.vector_store import get_or_create_collection


def keyword_search(query: str, top_k: int=20) -> list[dict]:

    collection = get_or_create_collection()
    all_data = collection.get(include=["documents", "metadatas"])

    documents = all_data.get("documents", [])
    metadatas = all_data.get("metadatas", [])

    if not documents:
        return []

    tokenized_corpus = [doc.lower() for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    scored = list(zip(documents, metadatas, scores))
    scored.sort(key=lambda x: x[2], reverse=True)

    results = []

    for doc_text, meta, score in scored[:top_k]:
        results.append(
            {
                "source": meta.get("source", "local"),
                "content": doc_text,
                "origin": "keyword_search",
            }
        )

    return results
    