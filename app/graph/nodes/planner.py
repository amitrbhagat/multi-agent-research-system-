from app.graph.state import AgentState
from app.llm.client import call_llm_structured, StructuredOutputError
from app.llm.schemas import PlannerOutput
from app.prompts.planner_prompt import build_planner_prompt


def run_planner(state: AgentState) -> AgentState:
    if state["retry_count"] > 0:
        print(f"[planner] retrying (retry_count={state['retry_count']})")
    else:
        print("[planner] initial run")

    feedback = state["critique"].get("feedback") if state["retry_count"] > 0 else None
    prompt = build_planner_prompt(state["query"], feedback=feedback)

    try:
        result: PlannerOutput = call_llm_structured(prompt, PlannerOutput)
        state["plan"] = result.plan

    except StructuredOutputError as e:
        print(f"[planner] structured output failed: {e}")
        state["plan"] = state["plan"] or ["fallback: answer using best available context"]

    return state



if __name__ == "__main__":
    state: AgentState = {
        "query": str,
        "plan": list[str],
        "retrieved_docs": list[dict],
        "draft": str,
        "critique": dict,
        "retry_count": int,
    }

    print(run_planner(state))