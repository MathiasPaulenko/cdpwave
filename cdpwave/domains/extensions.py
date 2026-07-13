"""Extensions domain: load unpacked extensions and manage extension storage.

Types:

    ``StorageArea`` — str.  Storage areas.  Values: ``"session"``,
    ``"local"``, ``"sync"``, ``"managed"``.

    ``ExtensionInfo`` — dict.  Detailed information about an extension.
    Fields: ``id`` (str), ``name`` (str), ``version`` (str),
    ``path`` (str), ``enabled`` (bool).

Events:

    None.
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ExtensionsDomain(BaseDomain):
    """Wrapper for the CDP Extensions domain.

    Defines commands and events for browser extensions.
    """

    async def trigger_action(
        self,
        id: str,
        target_id: str,
    ) -> dict[str, Any]:
        """Runs an extension default action.

        Args:
            id: Extension id.
            target_id: A tab target ID to trigger the default extension
                action on.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` or ``target_id`` is not a str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(target_id, str):
            raise TypeError(
                f"target_id must be a str, got {type(target_id).__name__}"
            )
        return await self._call(
            "Extensions.triggerAction",
            {"id": id, "targetId": target_id},
        )

    async def load_unpacked(
        self,
        path: str,
        enable_in_incognito: bool = False,
    ) -> dict[str, Any]:
        """Installs an unpacked extension from the filesystem similar to
        --load-extension CLI flags. Returns extension ID once the extension
        has been installed.

        Args:
            path: Absolute file path.
            enable_in_incognito: Enable the extension in incognito.
                Always sent (no omitempty in Go source — defaults to
                ``False``).

        Returns:
            Dict with ``id`` of the loaded extension.

        Raises:
            TypeError: If ``path`` is not a str, or
                ``enable_in_incognito`` is not a bool.
        """
        if not isinstance(path, str):
            raise TypeError(
                f"path must be a str, got {type(path).__name__}"
            )
        if not isinstance(enable_in_incognito, bool):
            raise TypeError(
                f"enable_in_incognito must be a bool, "
                f"got {type(enable_in_incognito).__name__}"
            )
        params: dict[str, Any] = {
            "path": path,
            "enableInIncognito": enable_in_incognito,
        }
        return await self._call("Extensions.loadUnpacked", params)

    async def get_extensions(self) -> dict[str, Any]:
        """Gets a list of all unpacked extensions.

        Returns:
            Dict with ``extensions`` list.
        """
        return await self._call("Extensions.getExtensions")

    async def uninstall(self, id: str) -> dict[str, Any]:
        """Uninstalls an unpacked extension (others not supported) from the
        profile.

        Args:
            id: Extension id.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` is not a str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        return await self._call("Extensions.uninstall", {"id": id})

    async def get_storage_items(
        self,
        id: str,
        storage_area: str,
        keys: list[str] | None = None,
    ) -> dict[str, Any]:
        """Gets data from extension storage in the given storageArea. If keys
        is specified, these are used to filter the result.

        Args:
            id: ID of extension.
            storage_area: Storage area to retrieve data from
                (``"session"``, ``"local"``, ``"sync"``,
                ``"managed"``).
            keys: Keys to retrieve.  Omitted when None
                (omitempty,omitzero in Go source).

        Returns:
            Dict with ``data``.

        Raises:
            TypeError: If ``id`` or ``storage_area`` is not a str,
                or ``keys`` is not a list of str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(storage_area, str):
            raise TypeError(
                f"storage_area must be a str, "
                f"got {type(storage_area).__name__}"
            )
        if keys is not None:
            if not isinstance(keys, list):
                raise TypeError(
                    f"keys must be a list, got {type(keys).__name__}"
                )
            for i, k in enumerate(keys):
                if not isinstance(k, str):
                    raise TypeError(
                        f"keys[{i}] must be a str, "
                        f"got {type(k).__name__}"
                    )
        params: dict[str, Any] = {"id": id, "storageArea": storage_area}
        if keys is not None:
            params["keys"] = keys
        return await self._call("Extensions.getStorageItems", params)

    async def remove_storage_items(
        self,
        id: str,
        storage_area: str,
        keys: list[str] | None = None,
    ) -> dict[str, Any]:
        """Removes keys from extension storage in the given storageArea.

        Args:
            id: ID of extension.
            storage_area: Storage area to remove data from
                (``"session"``, ``"local"``, ``"sync"``,
                ``"managed"``).
            keys: Keys to remove.  Always sent (no omitempty in Go
                source — defaults to ``[]`` when None).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` or ``storage_area`` is not a str,
                or ``keys`` is not a list of str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(storage_area, str):
            raise TypeError(
                f"storage_area must be a str, "
                f"got {type(storage_area).__name__}"
            )
        if keys is not None:
            if not isinstance(keys, list):
                raise TypeError(
                    f"keys must be a list, got {type(keys).__name__}"
                )
            for i, k in enumerate(keys):
                if not isinstance(k, str):
                    raise TypeError(
                        f"keys[{i}] must be a str, "
                        f"got {type(k).__name__}"
                    )
        params: dict[str, Any] = {
            "id": id,
            "storageArea": storage_area,
            "keys": keys if keys is not None else [],
        }
        return await self._call("Extensions.removeStorageItems", params)

    async def clear_storage_items(
        self,
        id: str,
        storage_area: str,
    ) -> dict[str, Any]:
        """Clears extension storage in the given storageArea.

        Args:
            id: ID of extension.
            storage_area: Storage area to remove data from
                (``"session"``, ``"local"``, ``"sync"``,
                ``"managed"``).

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` or ``storage_area`` is not a str.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(storage_area, str):
            raise TypeError(
                f"storage_area must be a str, "
                f"got {type(storage_area).__name__}"
            )
        return await self._call(
            "Extensions.clearStorageItems",
            {"id": id, "storageArea": storage_area},
        )

    async def set_storage_items(
        self,
        id: str,
        storage_area: str,
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """Sets values in extension storage in the given storageArea. The
        provided values will be merged with existing values in the storage
        area.

        Args:
            id: ID of extension.
            storage_area: Storage area to set data in
                (``"session"``, ``"local"``, ``"sync"``,
                ``"managed"``).
            values: Values to set.

        Returns:
            Empty dict (no return value from CDP).

        Raises:
            TypeError: If ``id`` or ``storage_area`` is not a str,
                or ``values`` is not a dict.
        """
        if not isinstance(id, str):
            raise TypeError(
                f"id must be a str, got {type(id).__name__}"
            )
        if not isinstance(storage_area, str):
            raise TypeError(
                f"storage_area must be a str, "
                f"got {type(storage_area).__name__}"
            )
        if not isinstance(values, dict):
            raise TypeError(
                f"values must be a dict, got {type(values).__name__}"
            )
        return await self._call(
            "Extensions.setStorageItems",
            {"id": id, "storageArea": storage_area, "values": values},
        )
