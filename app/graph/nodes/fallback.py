from app.graph.state import AgentState


def run_fallback(state: AgentState) -> AgentState:

    print("[fallback] retrieval failed, returning honest response")
    state["draft"] = (
        "I wasn't able to retrieve reliable information to answer this "
        "query right now. Please try rephrasing or try again shortly."
    )
    state["critique"] = {"score": 0.0, "feedback": "no data retrieved"}
    return state
