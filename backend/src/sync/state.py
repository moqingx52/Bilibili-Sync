from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PlaybackState:
    video_url: Optional[str] = None
    status: str = "paused"
    position_ms: int = 0
    last_actor: Optional[str] = None

    def snapshot(self) -> dict:
        return {
            "url": self.video_url,
            "status": self.status,
            "position_ms": self.position_ms,
            "actor": self.last_actor,
        }

    def set_video(self, url: str):
        self.video_url = url
        self.position_ms = 0
        self.status = "paused"
        self.last_actor = None

    def apply(self, event_type: str, position_ms: Optional[int], actor: Optional[str]) -> Optional[dict]:
        if event_type not in {"play", "pause", "seek"}:
            return None
        if event_type == "seek" and position_ms is not None:
            self.position_ms = max(0, int(position_ms))
        if event_type in {"play", "pause"}:
            self.status = "playing" if event_type == "play" else "paused"
            if position_ms is not None:
                self.position_ms = max(0, int(position_ms))
        if position_ms is None and self.position_ms < 0:
            self.position_ms = 0
        self.last_actor = actor
        return self.snapshot()


playback_state = PlaybackState()
