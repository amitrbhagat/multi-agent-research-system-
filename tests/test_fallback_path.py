from unittest.mock import patch

from app.graph.builder import build_graph
from app.graph.state import AgentState


def test_fallback_triggers_on_total_retrieval_failure():
    with patch(
        "app.graph.nodes.researcher.call_web_search", return_value=[]
    ):
        graph = build_graph()
        initial_state: AgentState = {
            "query": "this will fail",
            "plan": [],
            "retrieved_docs": [],
            "draft": "",
            "critique": {},
            "retry_count": 0,
            "retrieval_failed": False,
        }
        final_state = graph.invoke(initial_state)

        assert final_state["retrieval_failed"] is True
        assert "wasn't able to retrieve" in final_state["draft"]
        assert final_state["critique"]["score"] == 0.0
        return final_state["draft"]


if __name__=="__main__":
    print(test_fallback_triggers_on_total_retrieval_failure())    
    