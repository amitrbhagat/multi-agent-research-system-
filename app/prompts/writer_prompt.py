WRITER_SYSTEM_PROMPT = """You are the Writer agent in a research system.
Given a user query and a set of retrieved documents (each with an id),
write a clear answer using ONLY information present in the documents.

For every factual claim you make, you must list it separately with the
exact source_id of the document that supports it. If a claim is not
directly supported by any document, set source_id to null — do NOT
invent a source_id just to fill the field.

If the documents don't fully cover the query, say so explicitly in the
draft rather than filling gaps from general knowledge.
Output must match the required JSON schema exactly.
"""


def build_writer_prompt(query: str, retrieved_docs: list[dict], feedback: str | None=None) -> str:
    docs_text = "\n\n".join(
        f"[id: {d.get('id', 'unknown')}] [Source: {d.get('source', 'unknown')}]\n{d.get('content', '')[:800]}"
        for d in retrieved_docs
    )
    prompt = f"{WRITER_SYSTEM_PROMPT}\n\nQuery: {query}\n\nRetrieved documents:\n{docs_text}"
    if feedback:
        prompt += (
            f"\n\nA previous draft was scored as incomplete. "
            f"Critic feedback: {feedback}\n"
            f"Revise the draft to address this feedback directly."
        )
    return prompt
