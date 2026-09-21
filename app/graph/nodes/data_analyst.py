from app.graph.state import AgentState
from app.data_analyst.analyst_tool import answer_data_question


def run_data_analyst(state: AgentState) -> AgentState:
    print("[running] data_analyst")
    result = answer_data_question(state["query"])
    state["analyst_result"] = result
    return state
