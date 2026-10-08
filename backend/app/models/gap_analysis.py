"""Pydantic schemas for the Gap Analysis controller."""
from typing import Any

from pydantic import BaseModel, Field


class GapAnalysisRequest(BaseModel):
    """Employee and target project selectors; both fields are required."""

    employee_id: int = Field(examples=[1], description="ID of the employee in the employees table")
    project_ids: list[int] = Field(examples=[[1, 2]], description="List of project IDs from employee_projects table to analyse against")


# The agent returns a free-form JSON payload (strengths/gaps/score/etc.), so the
# response is passed through to the client as-is rather than a fixed schema.
GapAnalysisResponse = dict[str, Any]
