"""Pydantic schemas for the Employee Skills controller."""
from datetime import datetime

from pydantic import BaseModel, Field


class EmployeeSkillBase(BaseModel):
    employee_id: int = Field(..., examples=[101])
    employee_name: str = Field(..., examples=["Jane Doe"])
    skill_name: str = Field(..., examples=["Python"])
    proficiency_level: str = Field(..., examples=["Advanced"])


class EmployeeSkillCreate(EmployeeSkillBase):
    pass


class EmployeeSkillUpdate(BaseModel):
    employee_name: str | None = None
    skill_name: str | None = None
    proficiency_level: str | None = None


class EmployeeSkill(EmployeeSkillBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
