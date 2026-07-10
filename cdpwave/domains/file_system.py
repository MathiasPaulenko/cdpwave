"""FileSystem domain: file system access for testing."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class FileSystemDomain(BaseDomain):
    """Wrapper for the CDP FileSystem domain.

    Provides access to the File System Access API for
    testing file system interactions in web apps.
    """

    async def get_directory(self) -> dict[str, Any]:
        """Get the file system directory.

        Returns:
            Dict with ``directory`` and ``token``.
        """
        return await self._call("FileSystem.getDirectory")
