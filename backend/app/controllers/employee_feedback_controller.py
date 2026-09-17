"""Employee Feedback controller: sample CRUD API backed by dummy data."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.business.employee_feedback_service import (
    EmployeeFeedbackService,
    get_employee_feedback_service,
)
from app.models.employee_feedback import (
    EmployeeFeedback,
    EmployeeFeedbackCreate,
    EmployeeFeedbackUpdate,
)

router = APIRouter(prefix="/api/employee-feedback", tags=["Employee Feedback"])


@router.get("/", response_model=list[EmployeeFeedback], summary="List all employee feedback entries")
def list_feedback(
    service: EmployeeFeedbackService = Depends(get_employee_feedback_service),
) -> list[EmployeeFeedback]:
    return service.list_feedback()


@router.get("/{item_id}", response_model=EmployeeFeedback, summary="Get an employee feedback entry by id")
def get_feedback(
    item_id: int, service: EmployeeFeedbackService = Depends(get_employee_feedback_service)
) -> EmployeeFeedback:
    item = service.get_feedback(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return item


@router.post(
    "/",
    response_model=EmployeeFeedback,
    status_code=status.HTTP_201_CREATED,
    summary="Create an employee feedback entry",
)
def create_feedback(
    payload: EmployeeFeedbackCreate,
    service: EmployeeFeedbackService = Depends(get_employee_feedback_service),
) -> EmployeeFeedback:
    return service.create_feedback(payload)


@router.put("/{item_id}", response_model=EmployeeFeedback, summary="Update an employee feedback entry")
def update_feedback(
    item_id: int,
    payload: EmployeeFeedbackUpdate,
    service: EmployeeFeedbackService = Depends(get_employee_feedback_service),
) -> EmployeeFeedback:
    item = service.update_feedback(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an employee feedback entry")
def delete_feedback(
    item_id: int, service: EmployeeFeedbackService = Depends(get_employee_feedback_service)
) -> None:
    if not service.delete_feedback(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
