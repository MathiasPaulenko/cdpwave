"""FileSystem domain: file system access for testing.

Experimental domain.

Types:

    ``BucketFileSystemLocator`` — dict with fields:
        - ``storageKey`` (str, required) — Storage key
        - ``bucketName`` (str, optional) — Bucket name; omitted if empty
        - ``pathComponents`` (list[str], required) — Path components

    ``Directory`` — dict with fields:
        - ``name`` (str)
        - ``nestedDirectories`` (list[str])
        - ``nestedFiles`` (list[File])

    ``File`` — dict with fields:
        - ``name`` (str)
        - ``lastModified`` (float — timestamp)
        - ``size`` (float — bytes)
        - ``type`` (str)
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class FileSystemDomain(BaseDomain):
    """Wrapper for the CDP FileSystem domain.

    **Experimental.**

    Provides access to the File System Access API for
    testing file system interactions in web apps.
    """

    async def get_directory(
        self,
        storage_key: str,
        path_components: list[str],
        bucket_name: str = "",
    ) -> dict[str, Any]:
        """Get a file system directory via a bucket file system locator.

        Args:
            storage_key: Storage key identifying the origin/storage partition.
            path_components: Path to the directory, each element being a
                single path component.
            bucket_name: Optional bucket name. If omitted (empty string),
                the default bucket is used.

        Returns:
            Dict with a ``directory`` key containing a ``Directory`` object
            (``name``, ``nestedDirectories``, ``nestedFiles``).

        Raises:
            TypeError: If ``storage_key`` is not a str, ``path_components``
                is not a list of str, or ``bucket_name`` is not a str.
        """
        if not isinstance(storage_key, str):
            raise TypeError(
                f"storage_key must be a str, got {type(storage_key).__name__}"
            )
        if not isinstance(path_components, list):
            raise TypeError(
                f"path_components must be a list[str], got {type(path_components).__name__}"
            )
        for i, pc in enumerate(path_components):
            if not isinstance(pc, str):
                raise TypeError(
                    f"path_components[{i}] must be a str, got {type(pc).__name__}"
                )
        if not isinstance(bucket_name, str):
            raise TypeError(
                f"bucket_name must be a str, got {type(bucket_name).__name__}"
            )

        locator: dict[str, Any] = {
            "storageKey": storage_key,
            "pathComponents": path_components,
        }
        if bucket_name:
            locator["bucketName"] = bucket_name

        return await self._call(
            "FileSystem.getDirectory",
            {"bucketFileSystemLocator": locator},
        )
