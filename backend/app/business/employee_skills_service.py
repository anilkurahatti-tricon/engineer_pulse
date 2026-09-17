"""Business logic layer for the Employee Skills controller."""
from app.dataservice.employee_skills_repository import (
    EmployeeSkillsRepository,
    employee_skills_repository,
)
from app.models.employee_skills import (
    EmployeeSkill,
    EmployeeSkillCreate,
    EmployeeSkillUpdate,
)


class EmployeeSkillsService:
    """Business rules sit between the controller and the data-access layer."""

    def __init__(self, repository: EmployeeSkillsRepository) -> None:
        self._repository = repository

    def list_skills(self) -> list[EmployeeSkill]:
        return self._repository.get_all()

    def get_skill(self, item_id: int) -> EmployeeSkill | None:
        return self._repository.get_by_id(item_id)

    def create_skill(self, payload: EmployeeSkillCreate) -> EmployeeSkill:
        return self._repository.create(payload)

    def update_skill(self, item_id: int, payload: EmployeeSkillUpdate) -> EmployeeSkill | None:
        return self._repository.update(item_id, payload)

    def delete_skill(self, item_id: int) -> bool:
        return self._repository.delete(item_id)


def get_employee_skills_service() -> EmployeeSkillsService:
    """FastAPI dependency factory for `EmployeeSkillsService`."""
    return EmployeeSkillsService(employee_skills_repository)
