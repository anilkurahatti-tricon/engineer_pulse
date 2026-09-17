"""Business logic layer for the Demo controller."""
from app.dataservice.demo_repository import DemoRepository, demo_repository
from app.models.demo import DemoItem, DemoItemCreate, DemoItemUpdate


class DemoService:
    """Business rules sit between the controller and the data-access layer."""

    def __init__(self, repository: DemoRepository) -> None:
        self._repository = repository

    def list_items(self) -> list[DemoItem]:
        return self._repository.get_all()

    def get_item(self, item_id: int) -> DemoItem | None:
        return self._repository.get_by_id(item_id)

    def create_item(self, payload: DemoItemCreate) -> DemoItem:
        return self._repository.create(payload)

    def update_item(self, item_id: int, payload: DemoItemUpdate) -> DemoItem | None:
        return self._repository.update(item_id, payload)

    def delete_item(self, item_id: int) -> bool:
        return self._repository.delete(item_id)


def get_demo_service() -> DemoService:
    """FastAPI dependency factory for `DemoService`."""
    return DemoService(demo_repository)
