from app.llm.client import call_llm_structured
from app.llm.schemas import WriterOutput, CriticOutput
from app.prompts.writer_prompt import build_writer_prompt
from app.prompts.critic_prompt import build_critic_prompt

SPARSE_DOCS = [
    {
        "id": "doc_0",
        "source": "unrelated.txt",
        "content": "The history of tea cultivation in China dates back centuries."
    }
]


def test_writer_does_not_fabricate_on_sparse_data():
    query = "What was the exact GDP growth rate of Brazil in Q3 2024?"
    prompt = build_writer_prompt(query, SPARSE_DOCS)
    result: WriterOutput = call_llm_structured(prompt, WriterOutput)

    assert isinstance(result, WriterOutput)
    # every claim should either cite doc_0 honestly or be marked ungrounded (null)
    for claim in result.claims:
        assert claim.source_id in (None, "doc_0")


def test_critic_flags_ungrounded_claim():
    query = "What was the exact GDP growth rate of Brazil in Q3 2024?"
    draft = "Brazil's GDP grew by 4.2% in Q3 2024."
    claims = [{"text": "Brazil's GDP grew by 4.2% in Q3 2024.", "source_id": "doc_0"}]

    prompt = build_critic_prompt(query, draft, claims, SPARSE_DOCS)
    result: CriticOutput = call_llm_structured(prompt, CriticOutput)

    assert isinstance(result, CriticOutput)
    assert len(result.ungrounded_claims) > 0


def test_critic_passes_properly_grounded_claim():
    query = "When does tea cultivation in China date back to?"
    draft = "Tea cultivation in China dates back centuries."
    claims = [{"text": "Tea cultivation in China dates back centuries.", "source_id": "doc_0"}]

    prompt = build_critic_prompt(query, draft, claims, SPARSE_DOCS)
    result: CriticOutput = call_llm_structured(prompt, CriticOutput)

    assert isinstance(result, CriticOutput)
    assert len(result.ungrounded_claims) == 0