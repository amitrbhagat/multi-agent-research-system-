from app.graph.builder import build_graph
from app.graph.state import AgentState


def test_full_graph_runs():
    graph = build_graph()

    initial_state: AgentState = {
        "query": "What is LangGraph?",
        "plan": [],
        "retrieved_docs": [],
        "draft": "",
        "critique": {},
        "retry_count": 0,
    }

    final_state = graph.invoke(initial_state)

    assert final_state["plan"] == ["stub-task-1", "stub-task-2"]
    assert final_state["retrieved_docs"][0]["name"] == "Pratik"
    assert final_state["draft"] == "This is a draft created by writer"
    assert final_state["critique"]["score"] == 1.0

    return final_state



if __name__=="__main__":
    final_state = test_full_graph_runs()
    print(final_state)
    