"""Project controller: API endpoints for project profiles and requirements."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.business.project_service import ProjectService, get_project_service
from app.models.project import ProjectRead

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get(
    "/",
    response_model=list[ProjectRead],
    summary="List all projects with required technologies and skills",
)
def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    return service.list_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get a project profile by ID",
)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    proj = service.get_project(project_id)
    if proj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    return proj
