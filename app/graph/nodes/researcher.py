from app.graph.state import AgentState
from app.tools.web_search_tool import call_web_search



def run_researcher(state: AgentState) -> AgentState:
    print("[running] agentstate")

    query = state["query"]
    results = call_web_search(query)

    state["retrieved_docs"] = results
    
    return state



if __name__ == "__main__":
    state: AgentState = {
        "retrieved_docs": list[dict]
    }

    print(run_researcher(state))
    