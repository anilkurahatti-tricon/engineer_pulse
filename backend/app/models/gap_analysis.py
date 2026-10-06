"""Pydantic schemas for the Gap Analysis controller."""
from typing import Any

from pydantic import BaseModel, Field


class GapAnalysisRequest(BaseModel):
    """Employee and target project selectors; omitted fields fall back to sample defaults."""

    employee_id: int | None = Field(default=None, examples=[1])
    project_ids: list[int] | None = Field(default=None, examples=[[1, 2]])


# The agent returns a free-form JSON payload (strengths/gaps/score/etc.), so the
# response is passed through to the client as-is rather than a fixed schema.
GapAnalysisResponse = dict[str, Any]
