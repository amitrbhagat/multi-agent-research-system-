CRITIC_SYSTEM_PROMPT = """You are the Critic agent in a research system.
You are given the original query, a drafted answer, and a list of claims
with the source_id each is supposedly grounded in, plus the actual
retrieved documents.

Do TWO separate checks:
1. Completeness/relevance: does the draft fully and relevantly answer the query?
2. Groundedness: for each claim, does the cited source_id actually exist
   AND does that document's content genuinely support the claim? Any claim
   with source_id=null, a source_id that doesn't exist, or a source_id
   whose content does NOT support the claim, must be listed in
   ungrounded_claims verbatim.

These are independent failure modes — a draft can be complete but
ungrounded, or grounded but incomplete. Score reflects both.
Output must match the required JSON schema exactly.
"""


def build_critic_prompt(query: str, draft: str, claims: list[dict], retrieved_docs: list[dict]) -> str:
    claims_text = "\n".join(
        f"-claim: \"{c['text']}\" | cited source_id: {c.get('source_id')}"
        for c in claims
    )

    docs_text = "\n\n".join(
        f"[id: {d.get('id', 'unknown')}]\n{d.get('content', '')[:500]}"
        for d in retrieved_docs
    )

    return (
        f"{CRITIC_SYSTEM_PROMPT}\n\n"
        f"Query: {query}\n\n"
        f"Draft:\n{draft}\n\n"
        f"Claims and their cited sources:\n{claims_text}\n\n"
        f"Retrieved documents (ground truth):\n{docs_text}"
    )
