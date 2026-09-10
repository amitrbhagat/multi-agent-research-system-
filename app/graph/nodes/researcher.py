from app.graph.state import AgentState
from app.tools.page_fetch_tool import call_page_fetch
from app.tools.web_search_tool import call_web_search



def run_researcher(state: AgentState) -> AgentState:
    print("[running] agentstate")

    query = state["query"]
    search_results = call_web_search(query)

    enriched_docs = []
    for result in search_results[:3]:
        fetched = call_page_fetch(result["url"])
        if fetched:
            enriched_docs.append(fetched)
        else:
            enriched_docs.append(result)


    state["retrieved_docs"] = enriched_docs
    state["retrieval_failed"] = len(enriched_docs) == 0
    
    return state



if __name__ == "__main__":
    state: AgentState = {
        "retrieved_docs": list[dict]
    }

    print(run_researcher(state))
    