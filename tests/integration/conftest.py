from __future__ import annotations

import contextlib
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio

from cdpwave import CDPClient, CDPSession
from cdpwave.browser.finder import find_browser


def _browser_available() -> bool:
    try:
        return find_browser() is not None
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _browser_available(),
    reason="No Chromium-based browser found",
)


@pytest_asyncio.fixture
async def client() -> AsyncIterator[CDPClient]:
    c = await CDPClient.launch(headless=True)
    yield c
    with contextlib.suppress(Exception):
        await c.close()


@pytest_asyncio.fixture
async def page(client: CDPClient) -> AsyncIterator[CDPSession]:
    p = await client.new_page("about:blank")
    yield p
    with contextlib.suppress(Exception):
        await p.close()


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
