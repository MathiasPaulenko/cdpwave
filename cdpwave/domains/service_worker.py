"""ServiceWorker domain: inspection and control of service workers."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class ServiceWorkerDomain(BaseDomain):
    """Wrapper for the CDP ServiceWorker domain.

    Provides inspection and control of service worker registrations,
    including starting/stopping workers, delivering push messages,
    and dispatching sync events.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the ServiceWorker domain.

        Activates ServiceWorker domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("ServiceWorker.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the ServiceWorker domain.

        Deactivates ServiceWorker domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("ServiceWorker.disable")

    async def deliver_push_message(
        self,
        origin: str,
        registration_id: str,
        data: str,
    ) -> dict[str, Any]:
        """Deliver a push message to a service worker.

        Args:
            origin: Security origin of the service worker.
            registration_id: Registration ID of the service worker.
            data: Push message data (base64-encoded).
        """
        if not isinstance(origin, str):
            raise TypeError("origin must be a string")
        if not isinstance(registration_id, str):
            raise TypeError("registration_id must be a string")
        if not isinstance(data, str):
            raise TypeError("data must be a string")
        return await self._call(
            "ServiceWorker.deliverPushMessage",
            {"origin": origin, "registrationId": registration_id, "data": data},
        )

    async def dispatch_sync_event(
        self,
        origin: str,
        registration_id: str,
        tag: str = "",
        last_chance: bool = False,
        data: str | None = None,
    ) -> dict[str, Any]:
        """Dispatch a sync event to a service worker.

        Args:
            origin: Security origin of the service worker.
            registration_id: Registration ID.
            tag: Sync tag.
            last_chance: Whether this is the last retry.
            data: Sync event data (not a CDP parameter, kept for API compatibility).
        """
        if not isinstance(origin, str):
            raise TypeError("origin must be a string")
        if not isinstance(registration_id, str):
            raise TypeError("registration_id must be a string")
        if not isinstance(tag, str):
            raise TypeError("tag must be a string")
        if not isinstance(last_chance, bool):
            raise TypeError("last_chance must be a bool")
        return await self._call(
            "ServiceWorker.dispatchSyncEvent",
            {
                "origin": origin,
                "registrationId": registration_id,
                "tag": tag,
                "lastChance": last_chance,
            },
        )

    async def start_worker(
        self,
        scope: str,
    ) -> dict[str, Any]:
        """Start a service worker for a scope.

        Args:
            scope: URL scope of the service worker to start.
        """
        if not isinstance(scope, str):
            raise TypeError("scope must be a string")
        return await self._call("ServiceWorker.startWorker", {"scopeURL": scope})

    async def skip_waiting(self, scope: str) -> dict[str, Any]:
        """Mark a service worker as waiting to activate.

        Args:
            scope: URL scope of the service worker.
        """
        if not isinstance(scope, str):
            raise TypeError("scope must be a string")
        return await self._call("ServiceWorker.skipWaiting", {"scopeURL": scope})

    async def stop_worker(self, version_id: str) -> dict[str, Any]:
        """Stop a running service worker.

        Args:
            version_id: Version ID of the service worker to stop.
        """
        if not isinstance(version_id, str):
            raise TypeError("version_id must be a string")
        return await self._call(
            "ServiceWorker.stopWorker",
            {"versionId": version_id},
        )

    async def inspect_worker(self, version_id: str) -> dict[str, Any]:
        """Inspect a service worker by opening a devtools session.

        Args:
            version_id: Version ID of the service worker to inspect.
        """
        if not isinstance(version_id, str):
            raise TypeError("version_id must be a string")
        return await self._call(
            "ServiceWorker.inspectWorker",
            {"versionId": version_id},
        )

    async def update(self, scope: str) -> dict[str, Any]:
        """Force an update of a service worker registration.

        Args:
            scope: URL scope of the service worker to update.
        """
        if not isinstance(scope, str):
            raise TypeError("scope must be a string")
        return await self._call("ServiceWorker.updateRegistration", {"scopeURL": scope})

    async def unregister(self, scope: str) -> dict[str, Any]:
        """Unregister a service worker.

        Args:
            scope: URL scope of the service worker to unregister.
        """
        if not isinstance(scope, str):
            raise TypeError("scope must be a string")
        return await self._call("ServiceWorker.unregister", {"scopeURL": scope})

    async def get_messages(self) -> dict[str, Any]:
        """Get service worker messages.

        Returns:
            Dict with ``messages`` list.
        """
        return await self._call("ServiceWorker.getMessages")
