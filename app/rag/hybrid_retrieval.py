from app.rag.vector_store import retrieve_candidates
from app.rag.keyword_search import keyword_search
from app.rag.reranker import rerank_candidates


def _deduplicates(candidates: list[dict]) -> list[dict]:

    seen = set()
    unique = []

    for c in candidates:
        key = c["content"][:200]
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique



def hybrid_retrieve(query: str, top_n: int=5) -> list[dict]:

    semantic_candidates = retrieve_candidates(query, candidates_k=15)
    keyword_candidates = keyword_search(query, top_k=15)

    merged = _deduplicates(semantic_candidates + keyword_candidates)
    return rerank_candidates(query, merged, top_n=top_n)
