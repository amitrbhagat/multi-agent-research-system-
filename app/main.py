import json
import uuid

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph.builder import build_graph
from app.graph.state import AgentState


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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


def _initial_state(query: str) -> AgentState:
    return {
        "run_id": str(uuid.uuid4()),
        "query": query,
        "intent": "",
        "plan": [],
        "retrieved_docs": [],
        "draft": "",
        "claims": [],
        "critique": {},
        "retry_count": 0,
        "retrieval_failed": False,
        "analyst_result": {},
    }


def _stream_graph_events(query: str):
    for step in compiled_graph.stream(_initial_state(query)):
        node_name = list(step.keys())[0]
        node_state = step[node_name]
        event = {"node": node_name, "state":node_state}
        yield f"data: {json.dumps(event)}\n\n"

    yield "data: {\"node\": \"__end__\"}\n\n"    



@app.post("/query/stream")
def run_query_stream(request: QueryRequest):
    return StreamingResponse(
        _stream_graph_events(request.query),
        media_type = "text/event-stream"
    )
