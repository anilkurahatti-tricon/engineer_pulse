"""In-memory data access layer for the Demo controller.

Simulates a database using a dict so CRUD wiring can be exercised end-to-end
without provisioning real infrastructure.
"""
from datetime import datetime, timezone
from itertools import count

from app.models.demo import DemoItem, DemoItemCreate, DemoItemUpdate

_id_generator = count(start=1)

_demo_store: dict[int, DemoItem] = {}


def _seed() -> None:
    for name, description in [
        ("Sample Item One", "Seeded demo item for testing GET/PUT/DELETE."),
        ("Sample Item Two", "Second seeded demo item."),
    ]:
        item_id = next(_id_generator)
        _demo_store[item_id] = DemoItem(
            id=item_id,
            name=name,
            description=description,
            created_at=datetime.now(timezone.utc),
        )


_seed()


class DemoRepository:
    """Data-access operations for demo items (dummy in-memory store)."""

    def get_all(self) -> list[DemoItem]:
        return list(_demo_store.values())

    def get_by_id(self, item_id: int) -> DemoItem | None:
        return _demo_store.get(item_id)

    def create(self, payload: DemoItemCreate) -> DemoItem:
        item_id = next(_id_generator)
        item = DemoItem(id=item_id, created_at=datetime.now(timezone.utc), **payload.model_dump())
        _demo_store[item_id] = item
        return item

    def update(self, item_id: int, payload: DemoItemUpdate) -> DemoItem | None:
        existing = _demo_store.get(item_id)
        if existing is None:
            return None
        updated_data = existing.model_dump()
        updated_data.update({k: v for k, v in payload.model_dump().items() if v is not None})
        updated_item = DemoItem(**updated_data)
        _demo_store[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        return _demo_store.pop(item_id, None) is not None


demo_repository = DemoRepository()
