"""Pydantic schemas for Project endpoints."""
from pydantic import BaseModel, ConfigDict, Field


class ProjectRead(BaseModel):
    """Project representation including required technologies."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project scope and description")
    technologies: str = Field(..., description="Comma-separated technology stack summary")
    required_skills: list[str] = Field(default_factory=list, description="List of required project skills")
    role: str | None = Field(default=None, description="Primary role needed on the project")
    duration_months: int = Field(default=6, description="Project timeline duration in months")
