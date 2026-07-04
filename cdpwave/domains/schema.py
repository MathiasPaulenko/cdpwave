"""Schema domain: discover available CDP domains and commands."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SchemaDomain(BaseDomain):
    """Wrapper for the CDP Schema domain.

    Provides discovery of available CDP domains, useful for
    introspection and dynamic command building.
    """

    async def get_domains(self) -> dict[str, Any]:
        """Get all available CDP domains.

        Returns:
            Dict with ``domains`` list, each containing ``name``,
            ``version``, and optional ``types``, ``commands``, and
            ``events``.
        """
        return await self._call("Schema.getDomains")
