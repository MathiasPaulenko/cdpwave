import os

import pytest

from cdpwave.browser.finder import find_brave, find_browser, find_chrome, find_chromium, find_edge
from cdpwave.exceptions import BrowserNotFoundError


class TestFindBrowser:
    def test_find_browser_raises_when_none_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        with pytest.raises(BrowserNotFoundError):
            find_browser()

    def test_env_override(self, monkeypatch: pytest.MonkeyPatch, tmp_path: object) -> None:
        fake_browser = os.path.join(str(tmp_path), "fakechrome.exe")
        with open(fake_browser, "w") as f:
            f.write("fake")
        monkeypatch.setenv("CDPWAVE_BROWSER_PATH", fake_browser)
        result = find_browser()
        assert result == fake_browser

    def test_env_override_nonexistent_falls_through(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("CDPWAVE_BROWSER_PATH", "/nonexistent/path/chrome")
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: "/fake/chrome")
        result = find_browser()
        assert result == "/fake/chrome"

    def test_preferred_browser_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: "/usr/bin/microsoft-edge")
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        result = find_browser(preferred="edge")
        assert result == "/usr/bin/microsoft-edge"

    def test_preferred_not_found_falls_through(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: "/usr/bin/chrome")
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        result = find_browser(preferred="edge")
        assert result == "/usr/bin/chrome"

    def test_search_order_chrome_first(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("cdpwave.browser.finder.find_chrome", lambda: "/usr/bin/chrome")
        monkeypatch.setattr("cdpwave.browser.finder.find_edge", lambda: "/usr/bin/edge")
        monkeypatch.setattr("cdpwave.browser.finder.find_brave", lambda: None)
        monkeypatch.setattr("cdpwave.browser.finder.find_chromium", lambda: None)
        monkeypatch.delenv("CDPWAVE_BROWSER_PATH", raising=False)
        result = find_browser()
        assert result == "/usr/bin/chrome"


class TestIndividualFinders:
    def test_find_chrome_returns_none_if_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CDPWAVE_CHROME_PATH", raising=False)
        monkeypatch.setattr("os.path.isfile", lambda _: False)
        monkeypatch.setattr("shutil.which", lambda _: None)
        assert find_chrome() is None

    def test_find_edge_returns_none_if_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CDPWAVE_EDGE_PATH", raising=False)
        monkeypatch.setattr("os.path.isfile", lambda _: False)
        monkeypatch.setattr("shutil.which", lambda _: None)
        assert find_edge() is None

    def test_find_brave_returns_none_if_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CDPWAVE_BRAVE_PATH", raising=False)
        monkeypatch.setattr("os.path.isfile", lambda _: False)
        monkeypatch.setattr("shutil.which", lambda _: None)
        assert find_brave() is None

    def test_find_chromium_returns_none_if_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CDPWAVE_CHROMIUM_PATH", raising=False)
        monkeypatch.setattr("os.path.isfile", lambda _: False)
        monkeypatch.setattr("shutil.which", lambda _: None)
        assert find_chromium() is None
