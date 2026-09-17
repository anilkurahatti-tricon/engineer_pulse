"""In-memory data access layer for the Employee Skills controller."""
from datetime import datetime, timezone
from itertools import count

from app.models.employee_skills import (
    EmployeeSkill,
    EmployeeSkillCreate,
    EmployeeSkillUpdate,
)

_id_generator = count(start=1)

_skills_store: dict[int, EmployeeSkill] = {}


def _seed() -> None:
    seed_rows = [
        (101, "Jane Doe", "Python", "Advanced"),
        (102, "John Smith", "React", "Intermediate"),
        (103, "Alex Lee", "FastAPI", "Advanced"),
    ]
    for employee_id, employee_name, skill_name, proficiency_level in seed_rows:
        item_id = next(_id_generator)
        _skills_store[item_id] = EmployeeSkill(
            id=item_id,
            employee_id=employee_id,
            employee_name=employee_name,
            skill_name=skill_name,
            proficiency_level=proficiency_level,
            created_at=datetime.now(timezone.utc),
        )


_seed()


class EmployeeSkillsRepository:
    """Data-access operations for employee skills (dummy in-memory store)."""

    def get_all(self) -> list[EmployeeSkill]:
        return list(_skills_store.values())

    def get_by_id(self, item_id: int) -> EmployeeSkill | None:
        return _skills_store.get(item_id)

    def create(self, payload: EmployeeSkillCreate) -> EmployeeSkill:
        item_id = next(_id_generator)
        item = EmployeeSkill(id=item_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
        _skills_store[item_id] = item
        return item

    def update(self, item_id: int, payload: EmployeeSkillUpdate) -> EmployeeSkill | None:
        existing = _skills_store.get(item_id)
        if existing is None:
            return None
        updated_data = existing.model_dump()
        updated_data.update({k: v for k, v in payload.model_dump().items() if v is not None})
        updated_item = EmployeeSkill(**updated_data)
        _skills_store[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        return _skills_store.pop(item_id, None) is not None


employee_skills_repository = EmployeeSkillsRepository()
