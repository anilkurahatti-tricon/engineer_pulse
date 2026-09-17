"""In-memory data access layer for the Employee Feedback controller."""
from datetime import datetime, timezone
from itertools import count

from app.models.employee_feedback import (
    EmployeeFeedback,
    EmployeeFeedbackCreate,
    EmployeeFeedbackUpdate,
)

_id_generator = count(start=1)

_feedback_store: dict[int, EmployeeFeedback] = {}


def _seed() -> None:
    seed_rows = [
        (101, "Jane Doe", "Great collaboration on the sprint.", 5),
        (102, "John Smith", "Needs to improve code review turnaround.", 3),
        (103, "Alex Lee", "Consistently delivers high quality work.", 4),
    ]
    for employee_id, employee_name, feedback_text, rating in seed_rows:
        item_id = next(_id_generator)
        _feedback_store[item_id] = EmployeeFeedback(
            id=item_id,
            employee_id=employee_id,
            employee_name=employee_name,
            feedback_text=feedback_text,
            rating=rating,
            created_at=datetime.now(timezone.utc),
        )


_seed()


class EmployeeFeedbackRepository:
    """Data-access operations for employee feedback (dummy in-memory store)."""

    def get_all(self) -> list[EmployeeFeedback]:
        return list(_feedback_store.values())

    def get_by_id(self, item_id: int) -> EmployeeFeedback | None:
        return _feedback_store.get(item_id)

    def create(self, payload: EmployeeFeedbackCreate) -> EmployeeFeedback:
        item_id = next(_id_generator)
        item = EmployeeFeedback(id=item_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
        _feedback_store[item_id] = item
        return item

    def update(self, item_id: int, payload: EmployeeFeedbackUpdate) -> EmployeeFeedback | None:
        existing = _feedback_store.get(item_id)
        if existing is None:
            return None
        updated_data = existing.model_dump()
        updated_data.update({k: v for k, v in payload.model_dump().items() if v is not None})
        updated_item = EmployeeFeedback(**updated_data)
        _feedback_store[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        return _feedback_store.pop(item_id, None) is not None


employee_feedback_repository = EmployeeFeedbackRepository()
