from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    plan: list[str] = Field(
        description = "Ordered list of concrete sub-tasks needed to answer the query"
    )
    reasoning: str = Field(
        description = "Brief explanation of why this plan addresses the query"
    )



class WriterOutput(BaseModel):
    draft: str = Field(
        description = "The answer to the user's query"
    )    
    key_points: list[str] = Field(
        descrition = "The main claims made in the draft, for the Critic to check"
    )


class CriticOutput(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Overall quality score")
    is_complete: bool = Field(description="Whether the draft fully answers the query")
    feedback: str = Field(description="Specific, actionable feedback for revision")
