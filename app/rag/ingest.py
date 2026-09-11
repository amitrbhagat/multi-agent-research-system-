import os
import uuid
import logging

from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import get_or_create_collection


logger = logging.getLogger(__name__)

RAW_DOCS_DIR = "./data/raw_docs"


def load_raw_documents(directory: str = RAW_DOCS_DIR) -> list[dict]:
    documents = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents.append({"source":filename, "text":f.read()})
    return documents              


def ingest_documents():
    collection = get_or_create_collection()
    documents = load_raw_documents()

    if not documents:
        logger.warning("No documents found in raw_docs directory.")
        return

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size = 500, overlap = 50)
        if not chunks:
            continue

        embeddings = embed_texts(chunks)
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": doc["source"], "chunk_index":i} for i in range(len(chunks))]

        collection.add(
            ids = ids,
            embeddings = embeddings,
            documents = chunks,
            metadatas = metadatas,
        )    

        logger.info(f"Ingested {len(chunks)} chunks from {doc['source']}")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ingest_documents()        
