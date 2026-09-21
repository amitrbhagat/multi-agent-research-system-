from pydantic import BaseModel
from app.llm.client import call_llm_structured, StructuredOutputError


INTENT_PROMPT = """Classify the following user query into exactly one category:
- "data" — the query asks for a specific number, statistic, average, total, or comparison from a structured dataset
- "research" — the query is open-ended, conceptual, or requires synthesizing information from multiple sources

Query: {query}

Respond with only the category label.
"""


class IntentOutput(BaseModel):
    intent: str


def classify_intent(query: str) -> str:
    prompt = INTENT_PROMPT.format(query=query)
    try:
        result: IntentOutput = call_llm_structured(prompt, IntentOutput)
        label = result.intent.strip().lower()
        return label if label in ("data", "research") else "research"
    except StructuredOutputError:
        return "research"
