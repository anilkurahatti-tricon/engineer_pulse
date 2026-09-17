"""Demo controller: full CRUD sample API used to validate the layered setup."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.business.demo_service import DemoService, get_demo_service
from app.models.demo import DemoItem, DemoItemCreate, DemoItemUpdate

router = APIRouter(prefix="/api/demo", tags=["Demo"])


@router.get("/", response_model=list[DemoItem], summary="List all demo items")
def list_demo_items(service: DemoService = Depends(get_demo_service)) -> list[DemoItem]:
    return service.list_items()


@router.get("/{item_id}", response_model=DemoItem, summary="Get a demo item by id")
def get_demo_item(item_id: int, service: DemoService = Depends(get_demo_service)) -> DemoItem:
    item = service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo item not found")
    return item


@router.post("/", response_model=DemoItem, status_code=status.HTTP_201_CREATED, summary="Create a demo item")
def create_demo_item(payload: DemoItemCreate, service: DemoService = Depends(get_demo_service)) -> DemoItem:
    return service.create_item(payload)


@router.put("/{item_id}", response_model=DemoItem, summary="Update a demo item")
def update_demo_item(
    item_id: int, payload: DemoItemUpdate, service: DemoService = Depends(get_demo_service)
) -> DemoItem:
    item = service.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a demo item")
def delete_demo_item(item_id: int, service: DemoService = Depends(get_demo_service)) -> None:
    if not service.delete_item(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo item not found")
