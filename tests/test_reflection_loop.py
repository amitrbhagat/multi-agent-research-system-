from unittest.mock import patch

from app.graph.builder import build_graph, route_after_critique
from app.graph.state import AgentState, MAX_RETRIES


def _initial_state(query="hard query") -> AgentState:
    return {
        "query": query,
        "plan": [],
        "retrieved_docs": [{"source": "stub", "content": "some context"}],
        "draft": "",
        "critique": {},
        "retry_count": 0,
        "retrieval_failed": False,
    }


def test_router_ends_on_good_score():
    state = _initial_state()
    state["critique"] = {"score": 0.9, "feedback": "great"}
    state["retry_count"] = 0
    assert route_after_critique(state) == "end"


def test_router_retries_on_low_score_under_cap():
    state = _initial_state()
    state["critique"] = {"score": 0.3, "feedback": "missing detail"}
    state["retry_count"] = 0
    assert route_after_critique(state) == "retry"


def test_router_forces_end_at_cap_even_with_low_score():
    state = _initial_state()
    state["critique"] = {"score": 0.1, "feedback": "still bad"}
    state["retry_count"] = MAX_RETRIES
    assert route_after_critique(state) == "end"


def test_full_graph_terminates_with_persistently_low_score():
    """
    Forces the Critic to always score low, confirming the graph
    still terminates instead of looping forever.
    """
    call_count = {"planner": 0}

    def counting_planner(state):
        call_count["planner"] += 1
        state["plan"] = ["stub-task"]
        return state

    with patch("app.graph.nodes.critic.call_llm_structured") as mock_critic, \
         patch("app.graph.nodes.writer.call_llm_structured") as mock_writer, \
         patch("app.graph.builder.run_planner", side_effect=counting_planner):


        from app.llm.schemas import CriticOutput, WriterOutput

        mock_writer.return_value = WriterOutput(draft="weak draft", key_points=[])
        mock_critic.return_value = CriticOutput(
            score=0.1, is_complete=False, feedback="always bad"
        )

        graph = build_graph()
        final_state = graph.invoke(_initial_state())

        # Planner should run once initially + once per retry, capped at MAX_RETRIES
        assert call_count["planner"] == MAX_RETRIES + 1
        assert final_state["retry_count"] == MAX_RETRIES