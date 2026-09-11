import chromadb
from chromadb.config import settings as chromaSettings


CHROMA_PERSIST_DIR = "./data/chromadb"
COLLECTION_NAME = "research_docs"


def get_chroma_client():
    return chromadb.PersistentClient(
        path = CHROMA_PERSIST_DIR,
        settings = chromaSettings(anonymized_telemetry=False)
    )


def get_or_create_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name = COLLECTION_NAME)


def query_collection(query_embedding: list[float], top_k: int=5)->dict:
    collection = get_or_create_collection()
    return collection.query(
        query_embedding=[query_embedding],
        n_results=top_k
    )