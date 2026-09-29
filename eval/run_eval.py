import json
import uuid
import logging

from app.graph.builder import build_graph
from app.db.connection import SessionLocal, engine
from app.db.models import Base, EvalResult
from eval.golden_dataset import GOLDEN_QUERIES
from eval.evaluators import EVALUATOR_MAP

logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)


def _initial_state(query: str, run_id: str) -> dict:
    return {
        "run_id": run_id,
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


def evaluate_single_query(graph, item: dict) -> dict:
    run_id = str(uuid.uuid4())
    initial_state = _initial_state(item["query"], run_id)

    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        logger.error(f"graph crashed on query_id={item['id']}: {e}")
        return {"query_id": item["id"], "run_id": run_id, "properties": {}, "crashed": True}

    results = {}
    # FIX: changed .item() to .items()
    for prop_name, expected_value in item['expected'].items():
        evaluator = EVALUATOR_MAP.get(prop_name)
        if evaluator is None:
            continue
        results[prop_name] = evaluator(final_state, expected_value)

    return {"query_id": item["id"], "run_id": run_id, "properties": results, "crashed": False}


def run_eval_suite():
    graph = build_graph()
    eval_run_id = str(uuid.uuid4())
    db = SessionLocal()

    total, passed = 0, 0

    try:
        for item in GOLDEN_QUERIES:
            outcome = evaluate_single_query(graph, item)
            all_passed = not outcome["crashed"] and all(outcome["properties"].values())

            total += 1
            passed += int(all_passed)

            print(f"[{item['id']}] {'PASS' if all_passed else 'FAIL'} — {outcome['properties']}")

            db.add(EvalResult(
                eval_run_id=eval_run_id,
                query_id=item["id"],
                query=item["query"],
                run_id=outcome["run_id"],
                passed="pass" if all_passed else "fail",
                details=json.dumps(outcome["properties"]),
            ))
        db.commit()
    finally:
        db.close()

    print(f"\n=== Eval suite complete: {passed}/{total} passed (eval_run_id={eval_run_id}) ===")
    return passed, total


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_eval_suite()