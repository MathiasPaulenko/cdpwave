import pytest

from cdpwave import CDPSession
from cdpwave.exceptions import CommandError


@pytest.mark.integration
class TestEscapeHatch:
    async def test_page_stop_loading(self, page: CDPSession) -> None:
        result = await page.send("Page.stopLoading", None)
        assert result == {}

    async def test_emulation_set_device_metrics(self, page: CDPSession) -> None:
        result = await page.send(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": 375,
                "height": 812,
                "deviceScaleFactor": 3,
                "mobile": True,
            },
        )
        assert result == {}

        await page.send("Emulation.clearDeviceMetricsOverride")

    async def test_nonexistent_method_raises_command_error(
        self, page: CDPSession
    ) -> None:
        with pytest.raises(CommandError):
            await page.send("NonExistent.method")
