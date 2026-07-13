"""Schema domain: discover available CDP domains and commands.

.. deprecated:: This domain is deprecated.

Types:

    ``Domain`` — dict. Description of the protocol domain.
    Fields: ``name`` (str — Domain name), ``version`` (str — Domain
    version).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class SchemaDomain(BaseDomain):
    """Wrapper for the CDP Schema domain.

    Provides discovery of available CDP domains, useful for
    introspection and dynamic command building.

    .. deprecated:: This domain is deprecated.
    """

    async def get_domains(self) -> dict[str, Any]:
        """Returns supported domains.

        Returns:
            Dict with ``domains`` list, each containing ``name``
            (str) and ``version`` (str).
        """
        return await self._call("Schema.getDomains")
