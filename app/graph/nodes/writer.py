from app.graph.state import AgentState
from app.llm.client import call_llm_structured, StructuredOutputError
from app.llm.schemas import WriterOutput
from app.prompts.writer_prompt import build_writer_prompt


def run_writer(state: AgentState)->AgentState:
    print(f"[running] writer (retry_count = {state['retry_count']})")

    feedback = state["critique"].get("feedback") if state["retry_count"] > 0 else None
    prompt = build_writer_prompt(state["query"], state["retrieved_docs"], feedback=feedback)

    try:
        result: WriterOutput = call_llm_structured(prompt, WriterOutput)
        state["draft"] = result.draft

    except StructuredOutputError as e:
        print(f"[writer] structured output failed: {e}")
        state["draft"] = state["draft"] or "Unable to generate a complete answer."

    return state


if __name__ == "__main__":
    state:AgentState = {
        "draft":str
    }

    print(run_writer(state))
