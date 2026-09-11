from sentence_transformers import SentenceTransformer
import logging


logger = logging.getLogger(__name__)

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def embed_texts(texts: list[str]) -> list[list[str]]:

    try:
        embeddings = model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    except Exception as e:
        logger.error(f"embedding call failed {e}")
        raise    