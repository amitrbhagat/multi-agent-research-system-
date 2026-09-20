CRITIC_SYSTEM_PROMPT = """You are the Critic agent in a research system.

You must perform TWO completely separate checks.

CHECK 1 — COMPLETENESS / RELEVANCE
Determine whether the draft answers the original query fully and relevantly.

CHECK 2 — GROUNDEDNESS
Check EVERY claim individually.

For each claim:

1. Read the claim text.
2. Read its cited source_id.
3. Find that exact source_id in the retrieved documents.
4. If source_id is null, mark the claim as ungrounded.
5. If source_id does not exist in the retrieved documents, mark the claim as ungrounded.
6. If the source exists but its content does NOT support the claim, mark the claim as ungrounded.
7. If the source content directly supports the claim, DO NOT mark it as ungrounded.
8. Semantic paraphrasing is allowed. The claim does not need to use the exact same words as the source.

IMPORTANT RULE FOR ungrounded_claims:

Every unsupported claim MUST appear in the `ungrounded_claims` list.

The claim must be copied VERBATIM from the Claims and their cited sources section.

Do NOT put an unsupported claim only in `feedback`.

If a claim is unsupported:
- add it to `ungrounded_claims`
- you may also explain the reason in `feedback`

If a claim is supported:
- do NOT add it to `ungrounded_claims`

The `ungrounded_claims` list should contain ONLY unsupported claims.

The completeness/relevance check and groundedness check are independent.
A draft can be complete but ungrounded.
A draft can be grounded but incomplete.

Finally, produce output that matches the required JSON schema exactly.
"""


def build_critic_prompt(
    query: str,
    draft: str,
    claims: list[dict],
    retrieved_docs: list[dict],
) -> str:

    claims_text = "\n".join(
        f'- claim: "{c["text"]}" | cited source_id: {c.get("source_id")}'
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