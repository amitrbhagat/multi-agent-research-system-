from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    plan: list[str] = Field(
        description = "Ordered list of concrete sub-tasks needed to answer the query"
    )
    reasoning: str = Field(
        description = "Brief explanation of why this plan addresses the query"
    )


class Claim(BaseModel):
    text: str = Field(description = "a single actual claim made in the draft")
    source_id: str | None = Field(
        default=None,
        description="ID of the retrieved doc that supports this claim, or null if none supports it",
    )


class WriterOutput(BaseModel):
    draft: str = Field(
        description = "The answer to the user's query"
    )    
    claims: list[Claim] = Field(
        description="Every factual claim in the draft, each tagged with its supporting source_id"
    )


class CriticOutput(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Overall quality score")
    is_complete: bool = Field(description="Whether the draft fully answers the query")
    ungrounded_claims: list[str] = Field(
        default_factory = list,
        description="Claims from the draft that have no valid supporting source_id",
    )
    feedback: str = Field(description="Specific, actionable feedback for revision")

