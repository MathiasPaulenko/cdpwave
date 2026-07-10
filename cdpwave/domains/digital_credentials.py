"""DigitalCredentials domain: digital wallet behavior simulation."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class DigitalCredentialsDomain(BaseDomain):
    """Wrapper for the CDP DigitalCredentials domain.

    Provides control over digital credential wallet behavior
    for testing digital credential API interactions.
    """

    async def set_virtual_wallet_behavior(
        self,
        behavior: str,
    ) -> dict[str, Any]:
        """Set the virtual wallet behavior.

        Args:
            behavior: Wallet behavior type.
        """
        return await self._call(
            "DigitalCredentials.setVirtualWalletBehavior",
            {"behavior": behavior},
        )
