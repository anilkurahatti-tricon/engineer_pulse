"""Pydantic schemas for the Demo controller (used to validate the CRUD wiring)."""
from datetime import datetime

from pydantic import BaseModel, Field


class DemoItemBase(BaseModel):
    name: str = Field(..., examples=["Sample Demo Item"])
    description: str = Field(..., examples=["A demo item used to validate CRUD APIs."])


class DemoItemCreate(DemoItemBase):
    pass


class DemoItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class DemoItem(DemoItemBase):
    id: int
    created_at: datetime
