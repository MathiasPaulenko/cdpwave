"""FedCm domain: Federated Credential Management."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class FedCmDomain(BaseDomain):
    """Wrapper for the CDP FedCm domain.

    Provides control over the Federated Credential Management API
    for testing federated login flows.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the FedCm domain."""
        return await self._call("FedCm.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the FedCm domain."""
        return await self._call("FedCm.disable")

    async def select_account(
        self,
        dialog_id: str,
        account_index: int,
    ) -> dict[str, Any]:
        """Select an account in a FedCm dialog.

        Args:
            dialog_id: Dialog ID.
            account_index: Index of the account to select.
        """
        return await self._call(
            "FedCm.selectAccount",
            {"dialogId": dialog_id, "accountIndex": account_index},
        )

    async def click_dialog_button(
        self,
        dialog_id: str,
        button: str,
    ) -> dict[str, Any]:
        """Click a button in a FedCm dialog.

        Args:
            dialog_id: Dialog ID.
            button: Button type (``"ConfirmIdpLoginContinue"``,
                ``"ErrorGotIt"``, ``"CloseButton"``).
        """
        return await self._call(
            "FedCm.clickDialogButton",
            {"dialogId": dialog_id, "button": button},
        )

    async def open_url(
        self,
        dialog_id: str,
        frame_id: str,
        url: str,
    ) -> dict[str, Any]:
        """Open a URL from a FedCm dialog.

        Args:
            dialog_id: Dialog ID.
            frame_id: Frame ID.
            url: URL to open.
        """
        return await self._call(
            "FedCm.openUrl",
            {"dialogId": dialog_id, "frameId": frame_id, "url": url},
        )

    async def dismiss_dialog(
        self,
        dialog_id: str,
        trigger_cooldown: bool | None = None,
    ) -> dict[str, Any]:
        """Dismiss a FedCm dialog.

        Args:
            dialog_id: Dialog ID.
            trigger_cooldown: Whether to trigger a cooldown.
        """
        params: dict[str, Any] = {"dialogId": dialog_id}
        if trigger_cooldown is not None:
            params["triggerCooldown"] = trigger_cooldown
        return await self._call("FedCm.dismissDialog", params)

    async def reset_cooldown(self) -> dict[str, Any]:
        """Reset the FedCm cooldown."""
        return await self._call("FedCm.resetCooldown")
