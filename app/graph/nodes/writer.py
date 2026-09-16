from app.graph.state import AgentState
from app.llm.client import call_llm_structured
from app.llm.schemas import WriterOutput
from app.prompts.writer_prompt import build_writer_output


def run_writer(state: AgentState)->AgentState:
    print("[running] writer")

    prompt = build_writer_prompt(state["query"], state["retrieved_docs"])
    result: WriterOutput = call_llm_structured(prompt, WriterOutput)

    state["draft"] = result.draft
    return state


if __name__ == "__main__":
    state:AgentState = {
        "draft":str
    }

    print(run_writer(state))
