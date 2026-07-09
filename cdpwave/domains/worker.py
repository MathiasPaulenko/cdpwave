"""Worker domain: dedicated worker lifecycle events.

The Worker domain is event-only — it emits ``dedicatedWorkerStarted``
and ``dedicatedWorkerTerminated`` events but has no commands.
This wrapper exists for API completeness and event documentation.
"""

from cdpwave.domains.base import BaseDomain


class WorkerDomain(BaseDomain):
    """Wrapper for the CDP Worker domain.

    The Worker domain is event-only. It emits:
    - ``Worker.dedicatedWorkerStarted`` — when a dedicated worker starts.
    - ``Worker.dedicatedWorkerTerminated`` — when a dedicated worker terminates.

    Use ``session.on("Worker.dedicatedWorkerStarted", handler)``
    to subscribe to these events.
    """
