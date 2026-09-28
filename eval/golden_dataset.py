
GOLDEN_QUERIES = [
    # --- Simple factual (research path) ---
    {
        "id": "factual_01",
        "query": "What is photosynthesis?",
        "expected": {"route": "research", "min_citations": 1},
    },
    {
        "id": "factual_02",
        "query": "What causes inflation?",
        "expected": {"route": "research", "min_citations": 1},
    },
    # --- Multi-hop / comparison (research path, likely harder) ---
    {
        "id": "multihop_01",
        "query": "Compare the economic effects of remote work versus office work",
        "expected": {"route": "research", "min_citations": 2},
    },
    {
        "id": "multihop_02",
        "query": "How do interest rates affect both inflation and unemployment?",
        "expected": {"route": "research", "min_citations": 2},
    },
    # --- Sparse-data / groundedness stress test ---
    {
        "id": "sparse_01",
        "query": "What was the exact GDP growth rate of Brazil in Q3 2024?",
        "expected": {"route": "research", "allow_ungrounded_admission": True},
    },
    {
        "id": "sparse_02",
        "query": "What is the population of a fictional city called Zorblatt?",
        "expected": {"route": "research", "allow_ungrounded_admission": True},
    },
    # --- Data-analyst routing ---
    {
        "id": "data_01",
        "query": "What is the average revenue in the dataset?",
        "expected": {"route": "data_analyst"},
    },
    {
        "id": "data_02",
        "query": "What is the total sum of sales?",
        "expected": {"route": "data_analyst"},
    },
    {
        "id": "data_03",
        "query": "What is the highest value recorded?",
        "expected": {"route": "data_analyst"},
    },
    # --- Ambiguous / edge cases ---
    {
        "id": "edge_01",
        "query": "tell me about it",
        "expected": {"route": "research", "should_not_crash": True},
    },
    {
        "id": "edge_02",
        "query": "",
        "expected": {"should_not_crash": True},
    },
    # --- Retry-loop stress test (deliberately vague, likely low-scoring) ---
    {
        "id": "retry_stress_01",
        "query": "Explain the thing about the stuff that happened",
        "expected": {"route": "research", "should_not_crash": True},
    },
]