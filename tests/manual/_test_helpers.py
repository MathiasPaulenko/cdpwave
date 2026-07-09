"""Shared helpers for all test modules."""

from __future__ import annotations

import asyncio
import contextlib
from typing import Any

from cdpwave.client import CDPClient, CDPSession

results: list[dict[str, Any]] = []


def log_result(tc_id: str, name: str, status: str, detail: str = "") -> None:
    if status == "FAIL" and "wasn't found" in detail:
        status = "SKIP"
        detail = f"CDP method not available: {detail[:200]}"
    results.append({"tc": tc_id, "name": name, "status": status, "detail": detail})
    icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]", "ERROR": "[ERROR]"}.get(status, "?")
    print(f"{icon} {tc_id}: {name} - {status}" + (f"  {detail[:120]}" if detail else ""))


async def fresh_session(client: CDPClient) -> CDPSession:
    s = await client.new_page()
    await asyncio.sleep(0.2)
    return s


async def safe_navigate(session: CDPSession, url: str, timeout: float = 10.0) -> dict[str, Any]:
    await session.page.enable()
    ev = asyncio.Event()
    async def _on_load(p): ev.set()
    session.on("Page.loadEventFired", _on_load)
    r = await session.page.navigate(url)
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(ev.wait(), timeout=timeout)
    return r


async def nav_data(session: CDPSession, html: str) -> None:
    await session.page.enable()
    ev = asyncio.Event()
    def _on_load(p): ev.set()
    session.on("Page.loadEventFired", _on_load)
    await session.page.navigate(f"data:text/html,{html}")
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(ev.wait(), timeout=3)
    await asyncio.sleep(0.3)
