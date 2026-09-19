from langgraph.graph import StateGraph, END

from app.graph.state import AgentState, MAX_RETRIES, SCORE_THRESHOLD
from app.graph.nodes.planner import run_planner
from app.graph.nodes.critic import run_critic
from app.graph.nodes.researcher import run_researcher
from app.graph.nodes.writer import run_writer
from app.graph.nodes.fallback import run_fallback


def route_after_research(state: AgentState) -> str:
    return "fallback" if state["retrieval_failed"] else "writer"


def route_after_critique(state: AgentState) -> str:
    score = state["critique"].get("score", 0.0)
    ungrounded = state["critique"].get("ungrounded_claims", [])

    if state["retry_count"] >= MAX_RETRIES:
        return "end"

    if score >= SCORE_THRESHOLD and not ungrounded:
        return "end"

    return "retry"


def run_retry(state: AgentState) -> AgentState:
    state["retry_count"] += 1

    ungrounded = state["critique"].get("ungrounded_claims", [])

    if ungrounded:
        note = (
            f"Groundedness failure: these claims had no valid supporting "
            f"source: {ungrounded}. On retry, either find real support for "
            f"them in the retrieved documents or remove them."
        )

        state["critique"]["feedback"] = (
            state["critique"].get("feedback", "") + "\n" + note
        )

    print(f"[retry] incrementing retry_count to {state['retry_count']}")
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", run_planner)
    graph.add_node("researcher", run_researcher)
    graph.add_node("writer", run_writer)
    graph.add_node("critic", run_critic)
    graph.add_node("retry", run_retry)
    graph.add_node("fallback", run_fallback)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "researcher")

    graph.add_conditional_edges(
        "researcher",
        route_after_research,
        {
            "writer": "writer",
            "fallback": "fallback",
        },
    )

    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critique,
        {
            "retry": "retry",
            "end": END,
        },
    )

    graph.add_edge("retry", "planner")

    graph.add_edge("fallback", END)

    return graph.compile()
