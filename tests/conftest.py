from __future__ import annotations

import pytest_asyncio

from cdpwave.types import CommandSender
from tests.unit.fake_sender import FakeSender


def pytest_configure(config: object) -> None:
    config.addinivalue_line("markers", "unit: fast isolated tests with mocks")
    config.addinivalue_line("markers", "integration: tests against a real Chrome browser")
    config.addinivalue_line("markers", "e2e: end-to-end tests with real browser flows")
    config.addinivalue_line("markers", "slow: tests that take more than 5 seconds")
    config.addinivalue_line("markers", "chrome: tests that require Chrome specifically")


@pytest_asyncio.fixture
async def fake_sender() -> FakeSender:
    """A FakeSender with an empty default response.

    Use ``fake_sender.set_response({...})`` to change the response mid-test.
    """
    return FakeSender({})


@pytest_asyncio.fixture
async def fake_sender_factory() -> type[FakeSender]:
    """Factory to create FakeSender instances with custom responses.

    Usage::

        sender = fake_sender_factory({"result": 42})
        domain = MyDomain(sender)
    """
    return FakeSender


@pytest_asyncio.fixture
async def fake_command_sender(fake_sender: FakeSender) -> CommandSender:
    """A bare CommandSender callable backed by FakeSender."""
    return fake_sender.as_sender()
