from app.graph.state import AgentState
from app.llm.client import call_llm_structured
from app.llm.schemas import PlannerOutput
from app.prompts.planner_prompt import build_planner_output


def run_planner(state: AgentState) -> AgentState:
    print("[planner] running")

    prompt = build_planner_output(state["query"])
    result: PlannerOutput = call_llm_structured(prompt, PlannerOutput)

    state["plan"] = result.plan
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