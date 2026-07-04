import asyncio

import pytest

from cdpwave import CDPClient


@pytest.mark.integration
class TestLifecycle:
    async def test_context_manager_closes_browser(self) -> None:
        async with await CDPClient.launch(headless=True) as client:
            assert client._launcher is not None
            assert client._launcher.is_running

        assert not client._launcher.is_running

    async def test_exception_in_context_body_cleans_up(self) -> None:
        client = await CDPClient.launch(headless=True)
        proc = client._launcher._process if client._launcher else None

        with pytest.raises(ValueError, match="body error"):
            async with client:
                raise ValueError("body error")

        assert client.is_closed is True
        if proc is not None:
            assert proc.returncode is not None

    async def test_close_idempotent(self) -> None:
        client = await CDPClient.launch(headless=True)
        await client.close()
        await client.close()
        assert client.is_closed is True

    async def test_close_target_marks_session_closed(
        self, client: CDPClient
    ) -> None:
        session = await client.new_page()
        assert not session.is_closed

        await session.target.close_target(session.target_id)

        for _ in range(10):
            await asyncio.sleep(0.5)
            if session.is_closed:
                break

        assert session.is_closed is True

    async def test_connect_to_existing_browser(self) -> None:
        launcher_client = await CDPClient.launch(headless=True, port=9223)
        assert launcher_client._launcher is not None
        assert launcher_client._launcher._info is not None
        port = launcher_client._launcher._info.port

        try:
            connected = await CDPClient.connect(host="localhost", port=port)
            pages = await connected.get_pages()
            assert isinstance(pages, list)
            await connected.close()
        finally:
            await launcher_client.close()
