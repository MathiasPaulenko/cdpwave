"""IO domain: input/output operations for streams produced by DevTools.

Types:

    ``StreamHandle`` — str. Either obtained from another method or
    specified as ``blob:<uuid>`` where ``<uuid>`` is a UUID of a Blob.

Events:

    None.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class IODomain(BaseDomain):
    """Wrapper for the CDP IO domain.

    Provides read access to stream handles returned by other CDP
    commands (e.g. ``Tracing.end`` with ``ReturnAsStream`` mode,
    ``Page.printToPDF`` with ``returnAsStream``).
    """

    async def close(self, handle: str) -> dict[str, Any]:
        """Close the stream, discard any temporary backing storage.

        Args:
            handle: Handle of the stream to close.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``handle`` is not a str.
        """
        if not isinstance(handle, str):
            raise TypeError(
                f"handle must be a str, "
                f"got {type(handle).__name__}"
            )
        return await self._call("IO.close", {"handle": handle})

    async def read(
        self,
        handle: str,
        offset: int | None = None,
        size: int | None = None,
    ) -> dict[str, Any]:
        """Read a chunk of the stream.

        Args:
            handle: Handle of the stream to read.
            offset: Seek to the specified offset before reading (if
                not specified, proceed with offset following the last
                read).  Omitted when None or 0 (omitempty,omitzero in
                Go source).
            size: Maximum number of bytes to read (left upon the
                agent discretion if not specified).  Omitted when
                None or 0 (omitempty,omitzero in Go source).

        Returns:
            Dict with ``base64Encoded`` (bool — set if the data is
            base64-encoded), ``data`` (str — data that were read),
            and ``eof`` (bool — set if end-of-file condition
            occurred).

        Raises:
            TypeError: If ``handle`` is not a str, or ``offset`` or
                ``size`` are not int (bool rejected).
        """
        if not isinstance(handle, str):
            raise TypeError(
                f"handle must be a str, "
                f"got {type(handle).__name__}"
            )
        if offset is not None and (
            isinstance(offset, bool)
            or not isinstance(offset, int)
        ):
            raise TypeError(
                f"offset must be an int, "
                f"got {type(offset).__name__}"
            )
        if size is not None and (
            isinstance(size, bool)
            or not isinstance(size, int)
        ):
            raise TypeError(
                f"size must be an int, "
                f"got {type(size).__name__}"
            )
        params: dict[str, Any] = {"handle": handle}
        if offset:
            params["offset"] = offset
        if size:
            params["size"] = size
        return await self._call("IO.read", params)

    async def resolve_blob(self, object_id: str) -> dict[str, Any]:
        """Return UUID of Blob object specified by a remote object id.

        Args:
            object_id: Object id of a Blob object wrapper.

        Returns:
            Dict with ``uuid`` (str — UUID of the specified Blob).

        Raises:
            TypeError: If ``object_id`` is not a str.
        """
        if not isinstance(object_id, str):
            raise TypeError(
                f"object_id must be a str, "
                f"got {type(object_id).__name__}"
            )
        return await self._call(
            "IO.resolveBlob",
            {"objectId": object_id},
        )
