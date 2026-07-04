"""IO domain: reading and resolving stream handles."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class IODomain(BaseDomain):
    """Wrapper for the CDP IO domain.

    Provides read access to stream handles returned by other CDP
    commands (e.g. ``Tracing.end`` with ``ReturnAsStream`` mode,
    ``Page.printToPDF`` with ``returnAsStream``).
    """

    async def read(
        self,
        handle: str,
        offset: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        """Read data from a stream handle.

        Args:
            handle: Stream handle from a prior CDP command.
            offset: Optional byte offset to start reading from.
            size: Optional maximum bytes to read.

        Returns:
            Dict with ``base64Encoded`` flag, ``data`` string, and
            ``eof`` boolean.
        """
        params: dict[str, Any] = {"handle": handle}
        if offset is not None:
            params["offset"] = offset
        if size is not None:
            params["size"] = size
        return await self._call("IO.read", params)

    async def close(self, handle: str) -> dict[str, Any]:
        """Close a stream handle.

        Args:
            handle: Stream handle to close.
        """
        return await self._call("IO.close", {"handle": handle})

    async def resolve_blob(self, object_id: str) -> dict[str, Any]:
        """Resolve a Blob object ID to a UUID for fetching.

        Args:
            object_id: Remote object ID of a Blob.

        Returns:
            Dict with ``uuid`` for the blob.
        """
        return await self._call("IO.resolveBlob", {"objectId": object_id})
