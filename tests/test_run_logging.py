# tests/test_run_logging.py
from app.graph.builder import build_graph
from app.db.connection import SessionLocal
from app.db.models import RunLog


def test_run_logs_are_written_for_full_graph_execution():
    graph = build_graph()

    run_id = "test-run-day11-001"
    initial_state = {
        "run_id": run_id,
        "query": "What was the exact GDP growth rate of Brazil in Q3 2024?",
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

    graph.invoke(initial_state)

    db = SessionLocal()
    try:
        logs = db.query(RunLog).filter(RunLog.run_id == run_id).all()
        node_names = {log.node_name for log in logs}

        assert len(logs) > 0
        assert "run_planner" in node_names
        # confirms logging captured whichever path this run actually took
        assert "run_researcher" in node_names or "run_data_analyst" in node_names
    finally:
        db.close()