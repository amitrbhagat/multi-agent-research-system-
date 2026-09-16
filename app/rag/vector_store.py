import chromadb

from app.rag.embeddings import embed_texts



CHROMA_PERSIST_DIR = "./data/chromadb"
COLLECTION_NAME = "research_docs"


def get_chroma_client():
    return chromadb.PersistentClient(
        path = CHROMA_PERSIST_DIR,
    )


def get_or_create_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name = COLLECTION_NAME)


def query_collection(query_embedding: list[float], top_k: int=5)->dict:
    collection = get_or_create_collection()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )


def retrieve_local_context(query: str, top_k :int = 5) -> list[dict]:
    query_embedding = embed_texts([query], input_type="query")[0]
    results = query_collection(query_embedding, top_k=top_k)

    local_docs = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc_text, meta in zip(documents, metadatas):
        local_docs.append({
            "source": meta.get("source", "local"),
            "content": doc_text,
            "origin": "local_vector_store"
        }
    )

    return local_docs    



def retrieve_candidates(query: str, candidates_k :int = 5) -> list[dict]:
    query_embedding = embed_texts([query])[0]
    results = query_collection(query_embedding, top_k=candidates_k)

    candidates = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc_text, meta in zip(documents, metadatas):
        candidates.append({
            "source": meta.get("source", "local"),
            "content": doc_text,
            "origin": "local_vector_store"
        }
    )

    return candidates  
