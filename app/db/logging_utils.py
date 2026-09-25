import json
import functools
import logging

from sqlalchemy.orm import Session

from app.db.connection import SessionLocal, engine
from app.db.models import RunLog, Base

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


def _safe_json(data) -> str:
    try:
        return json.dumps(data, default=data)
    except Exception as e:
        logger.warning(f"failed to serialize state for logging: {e}")
        return json.dumps({"_serialization_error": str(e)})


def run_save_log(run_id: str, node_name: str, input_data: dict, output_data: dict):
    db: Session = SessionLocal()
    try:
        log_entry = RunLog(
            run_id= run_id,
            node_name= node_name,
            input_data= _safe_json(input_data),
            output_data= _safe_json(output_data),
        )
        db.add(log_entry)    
        db.commit()
    except Exception as e:
        logger.error(f"failed to write run log for node={node_name}: {e}")
        db.rollback()
    finally:
        db.close() 


def with_logging(node_fn):

    @functools.wraps(node_fn)
    def wrapped(state):
        run_id = state.get("run_id", "unknown")
        input_snapshot = dict(state)

        output_state = node_fn(state)

        run_save_log(
            run_id=run_id,
            node_name=node_fn.__name__,
            input_data = input_snapshot,
            output_data=dict(output_state),
        )

        return output_state
    return wrapped
    