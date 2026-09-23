"""Database access layer for the Employee Skills controller."""
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.db_models import EmployeeSkillModel
from app.models.employee_skills import (
    EmployeeSkill,
    EmployeeSkillCreate,
    EmployeeSkillUpdate,
)


class EmployeeSkillsRepository:
    """Data-access operations for employee skills (PostgreSQL)."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[EmployeeSkill]:
        stmt = select(EmployeeSkillModel).order_by(EmployeeSkillModel.created_at.desc())
        models = self.db.scalars(stmt).all()
        return [EmployeeSkill.model_validate(m) for m in models]

    def get_by_id(self, item_id: int) -> EmployeeSkill | None:
        model = self.db.get(EmployeeSkillModel, item_id)
        if not model:
            return None
        return EmployeeSkill.model_validate(model)

    def create(self, payload: EmployeeSkillCreate) -> EmployeeSkill:
        model = EmployeeSkillModel(**payload.model_dump())
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return EmployeeSkill.model_validate(model)

    def update(self, item_id: int, payload: EmployeeSkillUpdate) -> EmployeeSkill | None:
        model = self.db.get(EmployeeSkillModel, item_id)
        if not model:
            return None
        
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(model, k, v)
            
        self.db.commit()
        self.db.refresh(model)
        return EmployeeSkill.model_validate(model)

    def delete(self, item_id: int) -> bool:
        model = self.db.get(EmployeeSkillModel, item_id)
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
