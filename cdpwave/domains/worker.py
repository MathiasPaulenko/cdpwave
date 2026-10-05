"""Worker domain.

The Worker domain was removed from CDP in modern Chrome versions —
its commands (``enable``, ``sendMessageToWorker``, etc.) and events
(``workerCreated``, ``workerTerminated``) no longer exist. Worker
targets are now managed via the ``Target`` domain
(``Target.setAutoAttach`` / ``Target.attachedToTarget``).

This wrapper exists for API completeness; it has no commands and
subscribing to ``Worker.*`` events will never fire on modern browsers.
"""

from cdpwave.domains.base import BaseDomain


class WorkerDomain(BaseDomain):
    """Wrapper for the CDP Worker domain (removed in modern Chrome).

    Kept for API completeness. To attach to workers, use
    ``Target.setAutoAttach`` on a session and listen for
    ``Target.attachedToTarget`` events.
    """
