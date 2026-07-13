"""DigitalCredentials domain: digital wallet behavior simulation.

This domain is **experimental**.

Types:
    VirtualWalletAction

Commands:
    setVirtualWalletBehavior

Events:
    (none)
"""

from typing import Any

from cdpwave.domains.base import BaseDomain

_VALID_ACTIONS = frozenset({"respond", "decline", "wait", "clear"})


class DigitalCredentialsDomain(BaseDomain):
    """Wrapper for the CDP DigitalCredentials domain.

    This domain is **experimental**.

    Allows interacting with the Digital Credentials API for
    automation by setting the behavior of the virtual wallet
    for digital credential requests.
    """

    async def set_virtual_wallet_behavior(
        self,
        action: str,
        protocol: str | None = None,
        response: dict[str, Any] | None = None,
        frame_id: str | None = None,
    ) -> dict[str, Any]:
        """Set the behavior of the virtual wallet for digital credential requests.

        Args:
            action: The action of the virtual wallet. One of
                ``"respond"``, ``"decline"``, ``"wait"``, ``"clear"``.
            protocol: The protocol identifier (e.g. ``"openid4vp"``).
            response: The response data object returned by the wallet.
            frame_id: The frame to scope the virtual wallet behavior
                to.

        Returns:
            The CDP response result dict.

        Raises:
            TypeError: If ``action`` is not a str, ``protocol`` is not
                a str, ``response`` is not a dict, or ``frame_id`` is
                not a str.
            ValueError: If ``action`` is not one of ``"respond"``,
                ``"decline"``, ``"wait"``, ``"clear"``.
        """
        if not isinstance(action, str):
            raise TypeError(
                f"action must be a str, got {type(action).__name__}"
            )
        if action not in _VALID_ACTIONS:
            raise ValueError(
                f"action must be 'respond', 'decline', 'wait', or "
                f"'clear', got {action!r}"
            )
        if protocol is not None and not isinstance(protocol, str):
            raise TypeError(
                f"protocol must be a str, got {type(protocol).__name__}"
            )
        if response is not None and not isinstance(response, dict):
            raise TypeError(
                f"response must be a dict, got {type(response).__name__}"
            )
        if frame_id is not None and not isinstance(frame_id, str):
            raise TypeError(
                f"frame_id must be a str, got {type(frame_id).__name__}"
            )
        params: dict[str, Any] = {"action": action}
        if protocol is not None:
            params["protocol"] = protocol
        if response is not None:
            params["response"] = response
        if frame_id is not None:
            params["frameId"] = frame_id
        return await self._call(
            "DigitalCredentials.setVirtualWalletBehavior",
            params,
        )
