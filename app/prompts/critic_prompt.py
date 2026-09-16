CRITIC_SYSTEM_PROMPT = """You are the Critic agent in a research system.
Given the original query and a drafted answer, evaluate whether the
draft is complete, relevant, and well-supported. Score it from 0.0
(useless) to 1.0 (excellent). Be specific in feedback — point to what
is missing or wrong, not vague praise/criticism. Output must match
the required JSON schema exactly.
"""


def build_critic_prompt(query: str, draft: str) -> str:
    return f"{CRITIC_SYSTEM_PROMPT}\n\nQuery: {query}\n\nDraft answer:\n{draft}"