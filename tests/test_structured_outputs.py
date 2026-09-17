from app.llm.client import call_llm_structured
from app.llm.schemas import PlannerOutput, WriterOutput, CriticOutput
from app.prompts.planner_prompt import build_planner_prompt
from app.prompts.writer_prompt import build_writer_prompt
from app.prompts.critic_prompt import build_critic_prompt


def test_planner_output_is_valid_schema():
    prompt = build_planner_prompt("What causes inflation?")
    result = call_llm_structured(prompt, PlannerOutput)
    assert isinstance(result, PlannerOutput)
    assert len(result.plan) > 0


def test_planner_handles_ambiguous_query():
    prompt = build_planner_prompt("tell me about it")
    result = call_llm_structured(prompt, PlannerOutput)
    assert isinstance(result, PlannerOutput)
    assert len(result.plan) >= 1


def test_writer_handles_empty_retrieved_docs():
    prompt = build_writer_prompt("What is the capital of Mars?", [])
    result = call_llm_structured(prompt, WriterOutput)
    assert isinstance(result, WriterOutput)
    assert len(result.draft) > 0  # should explain lack of info, not crash


def test_critic_output_score_is_bounded():
    prompt = build_critic_prompt("What is 2+2?", "The answer is 4.")
    result = call_llm_structured(prompt, CriticOutput)
    assert isinstance(result, CriticOutput)
    assert 0.0 <= result.score <= 1.0