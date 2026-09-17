"""Employee Skills controller: sample CRUD API backed by dummy data."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.business.employee_skills_service import (
    EmployeeSkillsService,
    get_employee_skills_service,
)
from app.models.employee_skills import (
    EmployeeSkill,
    EmployeeSkillCreate,
    EmployeeSkillUpdate,
)

router = APIRouter(prefix="/api/employee-skills", tags=["Employee Skills"])


@router.get("/", response_model=list[EmployeeSkill], summary="List all employee skill entries")
def list_skills(
    service: EmployeeSkillsService = Depends(get_employee_skills_service),
) -> list[EmployeeSkill]:
    return service.list_skills()


@router.get("/{item_id}", response_model=EmployeeSkill, summary="Get an employee skill entry by id")
def get_skill(
    item_id: int, service: EmployeeSkillsService = Depends(get_employee_skills_service)
) -> EmployeeSkill:
    item = service.get_skill(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return item


@router.post(
    "/",
    response_model=EmployeeSkill,
    status_code=status.HTTP_201_CREATED,
    summary="Create an employee skill entry",
)
def create_skill(
    payload: EmployeeSkillCreate,
    service: EmployeeSkillsService = Depends(get_employee_skills_service),
) -> EmployeeSkill:
    return service.create_skill(payload)


@router.put("/{item_id}", response_model=EmployeeSkill, summary="Update an employee skill entry")
def update_skill(
    item_id: int,
    payload: EmployeeSkillUpdate,
    service: EmployeeSkillsService = Depends(get_employee_skills_service),
) -> EmployeeSkill:
    item = service.update_skill(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an employee skill entry")
def delete_skill(
    item_id: int, service: EmployeeSkillsService = Depends(get_employee_skills_service)
) -> None:
    if not service.delete_skill(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
