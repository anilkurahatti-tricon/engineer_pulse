"""Business logic layer for the Employee Feedback controller."""
from app.dataservice.employee_feedback_repository import (
    EmployeeFeedbackRepository,
    employee_feedback_repository,
)
from app.models.employee_feedback import (
    EmployeeFeedback,
    EmployeeFeedbackCreate,
    EmployeeFeedbackUpdate,
)


class EmployeeFeedbackService:
    """Business rules sit between the controller and the data-access layer."""

    def __init__(self, repository: EmployeeFeedbackRepository) -> None:
        self._repository = repository

    def list_feedback(self) -> list[EmployeeFeedback]:
        return self._repository.get_all()

    def get_feedback(self, item_id: int) -> EmployeeFeedback | None:
        return self._repository.get_by_id(item_id)

    def create_feedback(self, payload: EmployeeFeedbackCreate) -> EmployeeFeedback:
        return self._repository.create(payload)

    def update_feedback(self, item_id: int, payload: EmployeeFeedbackUpdate) -> EmployeeFeedback | None:
        return self._repository.update(item_id, payload)

    def delete_feedback(self, item_id: int) -> bool:
        return self._repository.delete(item_id)


def get_employee_feedback_service() -> EmployeeFeedbackService:
    """FastAPI dependency factory for `EmployeeFeedbackService`."""
    return EmployeeFeedbackService(employee_feedback_repository)
