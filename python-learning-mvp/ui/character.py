"""Character rendering component with speech bubble."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


_STATE_MESSAGES = {
    "idle": "Готовий до нової пригоди в Python!",
    "thinking": "Думаю... Ти впораєшся 💡",
    "happy": "Супер! Так тримати 🚀",
    "error": "Не хвилюйся, помилки — це частина навчання.",
    "celebration": "Урок завершено! Час святкувати 🎉",
    "level_up": "Рівень підвищено! Неймовірно! ⭐",
}


def render_character(state: str, message: str | None = None) -> None:
    """Render Byte SVG and speech bubble text based on current state."""

    assets_dir = Path(__file__).resolve().parent.parent / "assets" / "characters"
    svg_path = assets_dir / f"{state}.svg"
    svg_content = svg_path.read_text(encoding="utf-8") if svg_path.exists() else ""
    bubble = message or _STATE_MESSAGES.get(state, _STATE_MESSAGES["idle"])

    st.markdown(
        (
            '<div class="ui-character-wrap">'
            f'<div class="ui-character-svg">{svg_content}</div>'
            f'<div class="ui-speech">{bubble}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
