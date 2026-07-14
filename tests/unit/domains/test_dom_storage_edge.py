"""Edge-case tests for the DOMStorage domain — validation branches only.

Targets every TypeError/ValueError raise in DOMStorageDomain to push
coverage from 72% to >=90%.
"""

import pytest

from cdpwave.domains.dom_storage import DOMStorageDomain
from tests.unit.fake_sender import FakeSender


@pytest.mark.unit
class TestDOMStorageEdgeValidation:
    async def test_get_dom_storage_items_storage_id_not_dict(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_id must be a dict"):
            await d.get_dom_storage_items("not-a-dict")  # type: ignore[arg-type]

    async def test_get_dom_storage_items_missing_is_local_storage(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(ValueError, match="storage_id must contain 'isLocalStorage'"):
            await d.get_dom_storage_items({"securityOrigin": "http://x"})

    async def test_set_dom_storage_item_storage_id_not_dict(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_id must be a dict"):
            await d.set_dom_storage_item("not-a-dict", "key", "val")  # type: ignore[arg-type]

    async def test_set_dom_storage_item_missing_is_local_storage(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(ValueError, match="storage_id must contain 'isLocalStorage'"):
            await d.set_dom_storage_item({"securityOrigin": "http://x"}, "key", "val")

    async def test_set_dom_storage_item_key_not_str(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key must be a string"):
            await d.set_dom_storage_item({"isLocalStorage": True}, 123, "val")  # type: ignore[arg-type]

    async def test_set_dom_storage_item_value_not_str(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="value must be a string"):
            await d.set_dom_storage_item({"isLocalStorage": True}, "key", 123)  # type: ignore[arg-type]

    async def test_remove_dom_storage_item_storage_id_not_dict(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_id must be a dict"):
            await d.remove_dom_storage_item("not-a-dict", "key")  # type: ignore[arg-type]

    async def test_remove_dom_storage_item_missing_is_local_storage(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(ValueError, match="storage_id must contain 'isLocalStorage'"):
            await d.remove_dom_storage_item({"securityOrigin": "http://x"}, "key")

    async def test_remove_dom_storage_item_key_not_str(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="key must be a string"):
            await d.remove_dom_storage_item({"isLocalStorage": True}, 123)  # type: ignore[arg-type]

    async def test_clear_storage_id_not_dict(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_id must be a dict"):
            await d.clear("not-a-dict")  # type: ignore[arg-type]

    async def test_clear_missing_is_local_storage(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(ValueError, match="storage_id must contain 'isLocalStorage'"):
            await d.clear({"securityOrigin": "http://x"})

    async def test_clear_dom_storage_items_storage_id_not_dict(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(TypeError, match="storage_id must be a dict"):
            await d.clear_dom_storage_items("not-a-dict")  # type: ignore[arg-type]

    async def test_clear_dom_storage_items_missing_is_local_storage(self) -> None:
        d = DOMStorageDomain(FakeSender({}))
        with pytest.raises(ValueError, match="storage_id must contain 'isLocalStorage'"):
            await d.clear_dom_storage_items({"securityOrigin": "http://x"})
