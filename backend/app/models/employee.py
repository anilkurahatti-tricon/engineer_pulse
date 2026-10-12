"""Pydantic schemas for Employee profile endpoints."""
from pydantic import BaseModel, ConfigDict, Field


class EmployeeRead(BaseModel):
    """Employee representation with aggregated current skills."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique employee identifier")
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Corporate email address")
    title: str = Field(..., description="Job title / engineering role")
    department: str = Field(..., description="Department or business unit")
    total_experience_years: float = Field(default=0.0, description="Total years of software experience")
    bio: str | None = Field(default=None, description="Short professional bio")
    skills: list[str] = Field(default_factory=list, description="List of recognized employee skills")
