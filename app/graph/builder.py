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

    if score >= SCORE_THRESHOLD:
        return "end"

    if state["retry_count"] >= MAX_RETRIES:
        return "end"

    return "retry"


def run_retry(state: AgentState) -> AgentState:
    state["retry_count"] += 1

    print(f"[retry] retry_count={state['retry_count']}")

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
