"""Animation domain: inspect and control CSS/Web animations."""

from typing import Any

from cdpwave.domains.base import BaseDomain


class AnimationDomain(BaseDomain):
    """Wrapper for the CDP Animation domain.

    Provides inspection and control of CSS animations, Web Animations,
    and transitions. Enable the domain to receive ``Animation.animationStarted``
    and ``Animation.animationCanceled`` events.
    """

    async def enable(self) -> dict[str, Any]:
        """Enable the Animation domain.

        Activates Animation domain events and reporting.
        Must be called before using other methods in this domain.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Animation.enable")

    async def disable(self) -> dict[str, Any]:
        """Disable the Animation domain.

        Deactivates Animation domain events and reporting.

        Returns:
            Response dict from the CDP.
        """
        return await self._call("Animation.disable")

    async def get_current_time(
        self,
        animation_id: str,
    ) -> dict[str, Any]:
        """Get the current time of an animation.

        Args:
            animation_id: Animation ID.

        Returns:
            Dict with ``currentTime`` in milliseconds.
        """
        return await self._call(
            "Animation.getCurrentTime",
            {"id": animation_id},
        )

    async def get_playback_rate(self) -> dict[str, Any]:
        """Get the playback rate of the document timeline.

        Returns:
            Dict with ``playbackRate`` for animations on page.
        """
        return await self._call("Animation.getPlaybackRate")

    async def resolve_animation(
        self,
        animation_id: str,
    ) -> dict[str, Any]:
        """Get the remote object of an Animation.

        Args:
            animation_id: Animation ID to resolve.

        Returns:
            Dict with ``remoteObject`` of the corresponding Animation.
        """
        return await self._call(
            "Animation.resolveAnimation",
            {"animationId": animation_id},
        )

    async def seek_animations(
        self,
        animations: list[str],
        current_time: int,
    ) -> dict[str, Any]:
        """Seek a set of animations to a particular time.

        Args:
            animations: List of animation IDs to seek.
            current_time: Target time in milliseconds.
        """
        return await self._call(
            "Animation.seekAnimations",
            {"animations": animations, "currentTime": current_time},
        )

    async def set_paused(
        self,
        animations: list[str],
        paused: bool,
    ) -> dict[str, Any]:
        """Pause or resume animations.

        Args:
            animations: List of animation IDs to pause/resume.
            paused: Whether to pause (True) or resume (False).
        """
        return await self._call(
            "Animation.setPaused",
            {"animations": animations, "paused": paused},
        )

    async def set_playback_rate(
        self,
        playback_rate: float,
    ) -> dict[str, Any]:
        """Set the global animation playback rate.

        Args:
            playback_rate: Playback rate (1.0 = normal speed).
        """
        return await self._call(
            "Animation.setPlaybackRate",
            {"playbackRate": playback_rate},
        )

    async def set_timing(
        self,
        animation_id: str,
        duration: int,
        delay: int,
    ) -> dict[str, Any]:
        """Set the timing of an animation.

        Args:
            animation_id: Animation ID.
            duration: Duration in milliseconds.
            delay: Delay in milliseconds.
        """
        return await self._call(
            "Animation.setTiming",
            {"animationId": animation_id, "duration": duration, "delay": delay},
        )

    async def release_animations(
        self,
        animations: list[str],
    ) -> dict[str, Any]:
        """Release animations to free resources.

        Args:
            animations: List of animation IDs to release.
        """
        return await self._call(
            "Animation.releaseAnimations",
            {"animations": animations},
        )

    async def seek_to(
        self,
        animations: list[str],
        current_time: int,
    ) -> dict[str, Any]:
        """Seek animations to a specific time.

        Alias for :meth:`seek_animations`.

        Args:
            animations: List of animation IDs.
            current_time: Target time in milliseconds.
        """
        return await self.seek_animations(animations, current_time)

    async def replay(
        self,
        animations: list[str],
    ) -> dict[str, Any]:
        """Replay animations from the beginning.

        Args:
            animations: List of animation IDs to replay.

        Returns:
            Dict with ``currentTime`` in milliseconds.
        """
        return await self._call(
            "Animation.replay",
            {"animations": animations},
        )
