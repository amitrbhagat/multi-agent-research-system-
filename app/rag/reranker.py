import logging
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

_cross_encoder = None


def get_cross_encoder() -> CrossEncoder: # type: ignore
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _cross_encoder



def rerank_candidates(query: str, candidates: list[dict], top_n: int=5) -> list[dict]:

    if not candidates:
        return []

    try:
        model = get_cross_encoder()
        pairs = [(query, c["content"]) for c in candidates]
        scores = model.predict(pairs)

        scored_candidates = list(zip(candidates, scores))
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        return [c for c, score in scored_candidates[:top_n]]

    except Exception as e:
        logger.error(f"re-ranking failed, falling back to original order: {e}")
        return candidates[:top_n]    
         