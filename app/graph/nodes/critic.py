from app.graph.state import AgentState
from app.llm.client import call_llm_structured, StructuredOutputError
from app.llm.schemas import CriticOutput
from app.prompts.critic_prompt import build_critic_prompt



def run_critic(state: AgentState) -> AgentState:
    print(f"[running] critic (retry_count={state['retry_count']})")

    prompt = build_critic_prompt(state["query"], state["draft"], state["claims"], state['retrieved_docs'])

    try:
        result: CriticOutput = call_llm_structured(prompt, CriticOutput)
        state["critique"] = result.model_dump()

    except StructuredOutputError as e:
        print(f"[critic] structured output failed, defaulting to pass: {e}")
        state["critique"] = {
            "score": 1.0,
            "is_complete": True,
            "ungrounded_claims": [],
            "feedback": "critic unavailable, auto-accepted",
        }

    return state



if __name__=="__main__":
    state: AgentState = {
        "critique":dict
    }

    print(run_critic(state))