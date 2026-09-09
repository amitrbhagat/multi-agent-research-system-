from fastapi import FastAPI
from pydantic import BaseModel

from app.graph.builder import build_graph
from app.graph.state import AgentState

app = FastAPI()
compiled_graph = build_graph()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def run_query(request: QueryRequest):
    initial_state: AgentState = {
        "query": request.query,
        "plan": [],
        "retrieved_docs": [],
        "draft": "",
        "critique": {},
        "retry_count": 0,
    }
    final_result = compiled_graph.invoke(initial_state)
    return final_result
