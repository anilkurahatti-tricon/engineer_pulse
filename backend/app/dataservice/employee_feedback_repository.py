"""Database access layer for the Employee Feedback controller."""
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.db_models import EmployeeFeedbackModel
from app.models.employee_feedback import (
    EmployeeFeedback,
    EmployeeFeedbackCreate,
    EmployeeFeedbackUpdate,
)


class EmployeeFeedbackRepository:
    """Data-access operations for employee feedback (PostgreSQL)."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[EmployeeFeedback]:
        stmt = select(EmployeeFeedbackModel).order_by(EmployeeFeedbackModel.created_at.desc())
        models = self.db.scalars(stmt).all()
        return [EmployeeFeedback.model_validate(m) for m in models]

    def get_by_id(self, item_id: int) -> EmployeeFeedback | None:
        model = self.db.get(EmployeeFeedbackModel, item_id)
        if not model:
            return None
        return EmployeeFeedback.model_validate(model)

    def create(self, payload: EmployeeFeedbackCreate) -> EmployeeFeedback:
        model = EmployeeFeedbackModel(**payload.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return EmployeeFeedback.model_validate(model)

    def update(self, item_id: int, payload: EmployeeFeedbackUpdate) -> EmployeeFeedback | None:
        model = self.db.get(EmployeeFeedbackModel, item_id)
        if not model:
            return None
        
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(model, k, v)
            
        self.db.commit()
        self.db.refresh(model)
        return EmployeeFeedback.model_validate(model)

    def delete(self, item_id: int) -> bool:
        model = self.db.get(EmployeeFeedbackModel, item_id)
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
