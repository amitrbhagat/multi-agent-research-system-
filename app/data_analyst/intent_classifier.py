DATA_KEYWORDS = (
    "average", "mean", "total", "sum", "highest", "lowest",
    "maximum", "minimum", "how many", "count", "median",
)


def classify_intent(query: str) -> str:
    """
    Deterministic, rule-based intent classification.
    No LLM call — given the narrow, fixed set of operations
    answer_data_question() actually supports (avg/sum/max/total),
    keyword matching is more reliable than a small local model's
    judgment call, and costs zero inference time.
    """
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in DATA_KEYWORDS):
        return "data"
    return "research"