# scripts/reconstruct_run.py
import sys
import json

from app.db.connection import SessionLocal
from app.db.models import RunLog


def reconstruct_run(run_id: str):
    db = SessionLocal()
    try:
        logs = (
            db.query(RunLog)
            .filter(RunLog.run_id == run_id)
            .order_by(RunLog.created_at.asc())
            .all()
        )

        if not logs:
            print(f"No logs found for run_id={run_id}")
            return

        print(f"=== Trace for run_id={run_id} ===\n")
        for entry in logs:
            print(f"[{entry.created_at}] {entry.node_name}")
            output = json.loads(entry.output_data)
            # print only a few relevant fields, not the entire dict
            for key in ("plan", "draft", "critique", "intent", "analyst_result"):
                if output.get(key):
                    print(f"    {key}: {output[key]}")
            print()

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/reconstruct_run.py <run_id>")
        sys.exit(1)
    reconstruct_run(sys.argv[1])