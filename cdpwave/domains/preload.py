"""Preload domain: control speculative loading and prefetching.

Types:

    ``RuleSetID`` — str. Unique id.

    ``RuleSet`` — dict. Corresponds to SpeculationRuleSet. Fields:
    ``id`` (RuleSetID), ``loaderId`` (str — identifies a document
    which the rule set is associated with), ``sourceText`` (str —
    source text of JSON representing the rule set),
    ``backendNodeId`` (int, optional — BackendNodeId of the relevant
    ``<script>`` tag), ``url`` (str, optional), ``requestId`` (str,
    optional), ``errorType`` (str, optional — ``"SourceIsNotJsonObject"``,
    ``"InvalidRulesSkipped"``, ``"InvalidRulesetLevelTag"``),
    ``tag`` (str, optional).

    ``RuleSetErrorType`` — str. Values: ``"SourceIsNotJsonObject"``,
    ``"InvalidRulesSkipped"``, ``"InvalidRulesetLevelTag"``.

    ``SpeculationAction`` — str. Values: ``"Prefetch"``,
    ``"Prerender"``, ``"PrerenderUntilScript"``.

    ``SpeculationTargetHint`` — str. Values: ``"Blank"``, ``"Self"``.

    ``IngAttemptKey`` — dict. A key that identifies a preloading
    attempt. Fields: ``loaderId`` (str), ``action``
    (SpeculationAction), ``url`` (str), ``formSubmission`` (bool),
    ``targetHint`` (SpeculationTargetHint, optional).

    ``IngAttemptSource`` — dict. Lists sources for a preloading
    attempt. Fields: ``key`` (IngAttemptKey), ``ruleSetIds``
    (list[RuleSetID]), ``nodeIds`` (list[int]).

    ``PipelineID`` — str. Preloading pipeline id.

    ``PrerenderFinalStatus`` — str. List of FinalStatus reasons for
    Prerender2.

    ``IngStatus`` — str. Preloading status values. Values:
    ``"Pending"``, ``"Running"``, ``"Ready"``, ``"Success"``,
    ``"Failure"``, ``"NotSupported"``.

    ``PrefetchStatus`` — str. Prefetch status values.

    ``PrerenderMismatchedHeaders`` — dict. Information of headers to
    be displayed when the header mismatch occurred. Fields:
    ``headerName`` (str), ``initialValue`` (str, optional),
    ``activationValue`` (str, optional).

Events:

    ``Preload.ruleSetUpdated`` — Upsert. Currently, it is only
    emitted when a rule set added. Params: ``ruleSet`` (RuleSet).

    ``Preload.ruleSetRemoved`` — [no description]. Params: ``id``
    (RuleSetID).

    ``Preload.preloadEnabledStateUpdated`` — Fired when a preload
    enabled state is updated. Params: ``disabledByPreference`` (bool),
    ``disabledByDataSaver`` (bool), ``disabledByBatterySaver`` (bool),
    ``disabledByHoldbackPrefetchSpeculationRules`` (bool),
    ``disabledByHoldbackPrerenderSpeculationRules`` (bool).

    ``Preload.prefetchStatusUpdated`` — Fired when a prefetch attempt
    is updated. Params: ``key`` (IngAttemptKey), ``pipelineId``
    (PipelineID), ``initiatingFrameId`` (str — frame id of the frame
    initiating prefetch), ``prefetchUrl`` (str), ``status``
    (IngStatus), ``prefetchStatus`` (PrefetchStatus), ``requestId``
    (str).

    ``Preload.prerenderStatusUpdated`` — Fired when a prerender
    attempt is updated. Params: ``key`` (IngAttemptKey),
    ``pipelineId`` (PipelineID), ``status`` (IngStatus),
    ``prerenderStatus`` (PrerenderFinalStatus, optional),
    ``disallowedMojoInterface`` (str, optional), ``mismatchedHeaders``
    (list[PrerenderMismatchedHeaders], optional).

    ``Preload.preloadingAttemptSourcesUpdated`` — Send a list of
    sources for all preloading attempts in a document. Params:
    ``loaderId`` (str), ``preloadingAttemptSources``
    (list[IngAttemptSource]).
"""

from typing import Any

from cdpwave.domains.base import BaseDomain


class PreloadDomain(BaseDomain):
    """Wrapper for the CDP Preload domain.

    Provides control over speculative loading, prefetching, and
    prerendering of pages for performance optimization.

    **Experimental domain.**

    Events:

    - ``ruleSetUpdated`` — Params: ``ruleSet`` (RuleSet).
    - ``ruleSetRemoved`` — Params: ``id`` (RuleSetID).
    - ``preloadEnabledStateUpdated`` — Params:
      ``disabledByPreference`` (bool), ``disabledByDataSaver`` (bool),
      ``disabledByBatterySaver`` (bool),
      ``disabledByHoldbackPrefetchSpeculationRules`` (bool),
      ``disabledByHoldbackPrerenderSpeculationRules`` (bool).
    - ``prefetchStatusUpdated`` — Params: ``key`` (IngAttemptKey),
      ``pipelineId`` (PipelineID), ``initiatingFrameId`` (str),
      ``prefetchUrl`` (str), ``status`` (IngStatus),
      ``prefetchStatus`` (PrefetchStatus), ``requestId`` (str).
    - ``prerenderStatusUpdated`` — Params: ``key`` (IngAttemptKey),
      ``pipelineId`` (PipelineID), ``status`` (IngStatus),
      ``prerenderStatus`` (PrerenderFinalStatus, optional),
      ``disallowedMojoInterface`` (str, optional),
      ``mismatchedHeaders`` (list[PrerenderMismatchedHeaders],
      optional).
    - ``preloadingAttemptSourcesUpdated`` — Params: ``loaderId``
      (str), ``preloadingAttemptSources`` (list[IngAttemptSource]).
    """

    async def disable(self) -> dict[str, Any]:
        """[no description].

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Preload.disable")

    async def enable(self) -> dict[str, Any]:
        """[no description].

        Returns:
            Empty dict (no return value from CDP).
        """
        return await self._call("Preload.enable")
