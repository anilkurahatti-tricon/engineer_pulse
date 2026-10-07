"""Pydantic schemas for the Roadmap controller."""
from typing import Any

from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    """The gap-analysis agent's own JSON output, posted directly as the request body.

    Matches the exact shape returned by POST /api/gap-analysis/analyze (employee_name,
    experience_years, overall_readiness_score, strengths, gaps, areas_of_improvement,
    summary). `employee_id` is an optional extra field used only to link the persisted
    roadmap record to an employee.
    """

    employee_name: str
    experience_years: float
    overall_readiness_score: float
    strengths: list[dict[str, Any]] = Field(default_factory=list)
    gaps: list[dict[str, Any]] = Field(default_factory=list)
    areas_of_improvement: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
    employee_id: int | None = Field(default=None, examples=[1])

    def to_gap_analysis(self) -> dict[str, Any]:
        """Rebuilds the plain gap-analysis dict (excluding the extra `employee_id`) for the agent."""
        return self.model_dump(exclude={"employee_id"})


# The agent returns a free-form JSON payload (monthly_plan/resources/etc.), so the
# response is passed through to the client as-is rather than a fixed schema.
RoadmapResponse = dict[str, Any]

