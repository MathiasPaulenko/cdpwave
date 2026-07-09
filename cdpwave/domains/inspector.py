"""Inspector domain: inspector lifecycle events.

The Inspector domain is event-only — it emits ``detached`` and
``targetCrashed`` events but has no commands. This wrapper exists
for API completeness and event documentation.
"""

from cdpwave.domains.base import BaseDomain


class InspectorDomain(BaseDomain):
    """Wrapper for the CDP Inspector domain.

    The Inspector domain is event-only. It emits:
    - ``Inspector.detached`` — when the inspector is detached.
    - ``Inspector.targetCrashed`` — when the target crashes.

    Use ``session.on("Inspector.detached", handler)``
    to subscribe to these events.
    """
