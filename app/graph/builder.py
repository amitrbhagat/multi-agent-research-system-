from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes.planner import run_planner
from app.graph.nodes.critic import run_critic
from app.graph.nodes.researcher import run_researcher
from app.graph.nodes.writer import run_writer
from app.graph.nodes.fallback import run_fallback


def route_after_research(state: AgentState) -> str:
    return "fallback" if state["retrieval_failed"] else "write"



def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", run_planner)
    graph.add_node("researcher", run_researcher)
    graph.add_node("writer", run_writer)
    graph.add_node("critic", run_critic)
    graph.add_node("fallback", run_fallback)


    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")

    graph.add_conditional_edges(
        "researcher",
        route_after_research,
        {"writer":"writer", "fallback":"fallback"},
    )

    graph.add_edge("writer", "critic")
    graph.add_edge("critic", END)
    graph.add_edge("fallback", END)

    return graph.compile()
