"""Business logic layer for Employee profile operations."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dataservice.employee_repository import EmployeeRepository
from app.models.employee import EmployeeRead


class EmployeeService:
    """Provides business logic and queries for Employee profiles."""

    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def list_employees(self) -> list[EmployeeRead]:
        return self._repository.get_all()

    def get_employee(self, employee_id: int) -> EmployeeRead | None:
        return self._repository.get_by_id(employee_id)


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """FastAPI dependency factory for `EmployeeService`."""
    repository = EmployeeRepository(db)
    return EmployeeService(repository)
