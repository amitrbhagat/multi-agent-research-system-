WRITER_SYSTEM_PROMPT = """You are the Writer agent in a research system.
Given a user query and a set of retrieved documents, write a clear,
well-organized answer using ONLY information present in the documents.
If the documents don't fully cover the query, say so explicitly rather
than filling gaps from general knowledge. Output must match the
required JSON schema exactly.
"""


def build_writer_prompt(query: str, retrieved_docs: list[dict]) -> str:
    docs_text = "\n\n".join(
        f"[Source: {d.get('source', 'unknown')}]\n{d.get('content', '')[:800]}"
        for d in retrieved_docs
    )
    return f"{WRITER_SYSTEM_PROMPT}\n\nQuery: {query}\n\nRetrieved documents:\n{docs_text}"