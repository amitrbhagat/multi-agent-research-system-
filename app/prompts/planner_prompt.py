PLANNER_SYSTEM_PROMPT = """You are the Planner agent in a research system.
Given a user query, break it into a short, ordered list of concrete
sub-tasks a Researcher agent should investigate. Do not answer the
query yourself. Output must match the required JSON schema exactly.

Example:
Query: "Compare the economic impact of remote work vs office work"
Plan:
- "Find data on productivity differences between remote and office work"
- "Find data on real estate/office cost implications for companies"
- "Find data on employee cost-of-living and commuting savings"
"""


def build_planner_prompt(query: str, feedback: str | None=None) -> str:
    prompt =  f"{PLANNER_SYSTEM_PROMPT}\n\nQuery: {query}"
    if feedback:
        prompt += (
            f"\n\nA previous attempt at this query was scored as incomplete. "
            f"Critic feedback: {feedback}\n"
            f"Revise the plan to address this feedback."
        )
    return prompt  
