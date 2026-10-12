"""Employee controller: API endpoints for employee profiles and skills."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.business.employee_service import EmployeeService, get_employee_service
from app.models.employee import EmployeeRead

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get(
    "/",
    response_model=list[EmployeeRead],
    summary="List all employees with their current skill profiles",
)
def list_employees(
    service: EmployeeService = Depends(get_employee_service),
) -> list[EmployeeRead]:
    return service.list_employees()


@router.get(
    "/{employee_id}",
    response_model=EmployeeRead,
    summary="Get an employee profile by ID",
)
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    emp = service.get_employee(employee_id)
    if emp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found",
        )
    return emp
