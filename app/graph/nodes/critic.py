from app.graph.state import AgentState
from app.llm.client import call_llm_structured
from app.llm.schemas import CriticOutput
from app.prompts.critic_prompt import build_critic_output



def run_critic(state: AgentState) -> AgentState:
    print("[running] critic")

    prompt = build_critic_prompt(state["query"], state["draft"])
    result: CriticOutput = call_llm_structured(prompt, CriticOutput)

    state["critique"] = result.model_dump()
    return state



if __name__=="__main__":
    state: AgentState = {
        "critique":dict
    }

    print(run_critic(state))