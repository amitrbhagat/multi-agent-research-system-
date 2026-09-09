from app.graph.state import AgentState



def run_writer(state: AgentState)->AgentState:
    print("[running] writer")
    state["draft"] = "This is a draft created by writer"
    return state


if __name__ == "__main__":
    state:AgentState = {
        "draft":str
    }

    print(run_writer(state))
