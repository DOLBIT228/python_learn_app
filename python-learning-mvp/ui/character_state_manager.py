"""Character state manager for UI reactions based on user events."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class CharacterState(str, Enum):
    """Supported visual states for Byte character."""

    IDLE = "idle"
    HAPPY = "happy"
    THINKING = "thinking"
    ERROR = "error"
    CELEBRATION = "celebration"
    LEVEL_UP = "level_up"


@dataclass
class CharacterStateManager:
    """Simple UI manager that maps events to character state and SVG file."""

    assets_dir: Path
    current_state: CharacterState = CharacterState.IDLE

    def set_loading(self) -> CharacterState:
        self.current_state = CharacterState.THINKING
        return self.current_state

    def set_correct_answer(self) -> CharacterState:
        self.current_state = CharacterState.HAPPY
        return self.current_state

    def set_error(self) -> CharacterState:
        self.current_state = CharacterState.ERROR
        return self.current_state

    def set_lesson_completed(self) -> CharacterState:
        self.current_state = CharacterState.CELEBRATION
        return self.current_state

    def set_level_up(self) -> CharacterState:
        self.current_state = CharacterState.LEVEL_UP
        return self.current_state

    def set_idle(self) -> CharacterState:
        self.current_state = CharacterState.IDLE
        return self.current_state

    def get_svg_path(self) -> Path:
        """Return SVG path for current state."""

        return self.assets_dir / f"{self.current_state.value}.svg"

    def get_svg_content(self) -> str:
        """Read current state SVG content for rendering in Streamlit."""

        return self.get_svg_path().read_text(encoding="utf-8")
