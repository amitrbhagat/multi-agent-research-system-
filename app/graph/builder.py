from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes.planner import run_planner
from app.graph.nodes.critic import run_critic
from app.graph.nodes.researcher import run_researcher
from app.graph.nodes.writer import run_writer



def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", run_planner)
    graph.add_node("researcher", run_researcher)
    graph.add_node("writer", run_writer)
    graph.add_node("critic", run_critic)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")
    graph.add_edge("critic", END)

    return graph.compile()
