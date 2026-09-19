from typing import TypedDict

MAX_RETRIES = 2
SCORE_THRESHOLD = 0.7


class AgentState(TypedDict):
    query: str
    plan: list[str]
    retrieved_docs: list[dict]
    draft: str
    critique: dict
    retry_count: int
    retrieval_failed: bool
    claims: list[dict]