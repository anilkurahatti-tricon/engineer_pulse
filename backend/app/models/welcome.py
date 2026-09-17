"""Pydantic schemas for the Welcome controller (landing page content)."""
from pydantic import BaseModel, Field


class FeatureHighlight(BaseModel):
    title: str = Field(..., examples=["Employee Feedback"])
    description: str = Field(..., examples=["Capture and review feedback for every engineer."])
    path: str = Field(..., examples=["/employee-feedback"])


class WelcomeInfo(BaseModel):
    app_name: str
    version: str
    tagline: str
    description: str
    features: list[FeatureHighlight]
