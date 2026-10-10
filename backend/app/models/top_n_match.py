"""Pydantic schemas for the Top-N Employee Match controller."""
from typing import Any

from pydantic import BaseModel, Field

DEFAULT_TOP_N = 5
MAX_TOP_N = 50


class TopNMatchRequest(BaseModel):
    """Project selector and the max number of employees to return, both required."""

    project_id: int = Field(examples=[1], description="ID of the project (employee_projects table) to match against")
    top_n: int = Field(
        default=DEFAULT_TOP_N,
        ge=1,
        le=MAX_TOP_N,
        examples=[5],
        description="Max number of top-matching employees to return",
    )


# The agent returns a free-form JSON payload (candidates/scores/etc.), so the
# response is passed through to the client as-is rather than a fixed schema.
TopNMatchResponse = dict[str, Any]
