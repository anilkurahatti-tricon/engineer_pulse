"""Pydantic schemas for the Employee Feedback controller."""
from datetime import datetime

from pydantic import BaseModel, Field


class EmployeeFeedbackBase(BaseModel):
    employee_id: int = Field(..., examples=[101])
    employee_name: str = Field(..., examples=["Jane Doe"])
    feedback_text: str = Field(..., examples=["Great collaboration on the sprint."])
    rating: int = Field(..., ge=1, le=5, examples=[4])


class EmployeeFeedbackCreate(EmployeeFeedbackBase):
    pass


class EmployeeFeedbackUpdate(BaseModel):
    employee_name: str | None = None
    feedback_text: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)


class EmployeeFeedback(EmployeeFeedbackBase):
    id: int
    created_at: datetime
