from app.graph.state import AgentState


def run_planner(state: AgentState) -> AgentState:
    print("[planner] running")
    state["plan"] = ["stub-task-1", "stub-task-2"]
    return state



if __name__ == "__main__":
    state: AgentState = {
        "query": str,
        "plan": list[str],
        "retrieved_docs": list[dict],
        "draft": str,
        "critique": dict,
        "retry_count": int,
    }

    print(run_planner(state))