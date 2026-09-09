from app.graph.state import AgentState


def run_researcher(state: AgentState) -> AgentState:
    print("[running] agentstate")
    state["retrieved_docs"] = [
            {
                "name": "Pratik",
                "age":24
            },
            {
                "name":"Dhanush",
                "age":26
            }
        ]
    return state



if __name__ == "__main__":
    state: AgentState = {
        "retrieved_docs": list[dict]
    }

    print(run_researcher(state))