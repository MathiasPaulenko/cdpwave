from __future__ import annotations

import pytest

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
