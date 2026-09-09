from app.graph.state import AgentState


def run_critic(state: AgentState) -> AgentState:
    print("[running] critic")
    state["critique"] = {
        "score": 1.0, 
        "feedback": "stub critique"
    }
    return state


if __name__=="__main__":
    state: AgentState = {
        "critique":dict
    }

    print(run_critic(state))