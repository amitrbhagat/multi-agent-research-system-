from app.graph.state import AgentState
from app.tools.page_fetch_tool import call_page_fetch
from app.tools.web_search_tool import call_web_search
from app.rag.vector_store import retrieve_local_context
from app.rag.hybrid_retrieval import hybrid_retrieve



def run_researcher(state: AgentState) -> AgentState:
    print("[running] agentstate")

    query = state["query"]

    local_docs = hybrid_retrieve(query, top_n=5)

    search_results = call_web_search(query)

    web_docs = []
    for result in search_results[:3]:
        fetched = call_page_fetch(result["url"])
        web_docs.append(fetched if fetched else result)

    combined_docs = local_docs + web_docs  

    state["retrieved_docs"] = combined_docs
    state["retrieval_failed"] = len(combined_docs) == 0
    
    return state



if __name__ == "__main__":
    state: AgentState = {
        "retrieved_docs": list[dict]
    }

    print(run_researcher(state))
    