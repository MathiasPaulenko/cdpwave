"""BackgroundService domain: observe background service events."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class BackgroundServiceDomain(BaseDomain):
    """Wrapper for the CDP BackgroundService domain.

    Provides observation of background service events (e.g. Background
    Fetch, Background Sync, Periodic Background Sync, Push Messaging,
    Notifications, Payment Handler) for debugging service worker
    background activity.
    """

    async def start_observing(
        self,
        service: str,
    ) -> dict[str, Any]:
        """Start observing events for a background service.

        Args:
            service: Service name (e.g. ``"backgroundFetch"``,
                ``"backgroundSync"``, ``"periodicBackgroundSync"``,
                ``"pushMessaging"``, ``"notifications"``,
                ``"paymentHandler"``, ``"paymentInstallments"``).
        """
        return await self._call(
            "BackgroundService.startObserving",
            {"service": service},
        )

    async def stop_observing(
        self,
        service: str,
    ) -> dict[str, Any]:
        """Stop observing events for a background service.

        Args:
            service: Service name to stop observing.
        """
        return await self._call(
            "BackgroundService.stopObserving",
            {"service": service},
        )

    async def set_recording(
        self,
        should_record: bool,
        service: str,
    ) -> dict[str, Any]:
        """Set recording state for a background service.

        Args:
            should_record: Whether to record events.
            service: Service name to record.
        """
        return await self._call(
            "BackgroundService.setRecording",
            {"shouldRecord": should_record, "service": service},
        )

    async def clear_events(
        self,
        service: str,
    ) -> dict[str, Any]:
        """Clear all stored events for a background service.

        Args:
            service: Service name to clear events for.
        """
        return await self._call(
            "BackgroundService.clearEvents",
            {"service": service},
        )
