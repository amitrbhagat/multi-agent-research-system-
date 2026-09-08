from typing import TypedDict


class AgentState(TypedDict):

    query: str
    plan: list[str]
    retrieved_docs: list[dict]
    draft: str
    critique: dict
    retry_count: int
    