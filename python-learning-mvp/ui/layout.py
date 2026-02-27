"""Layout wrapper helpers."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st


def render_layout(content_function: Callable[[], None]) -> None:
    """Render page content centered with max width of 720px."""

    st.markdown(
        """
        <style>
        .ui-layout-wrapper {
            max-width: 720px;
            margin: 0 auto;
        }
        </style>
        <div class="ui-layout-wrapper">
        """,
        unsafe_allow_html=True,
    )
    content_function()
    st.markdown("</div>", unsafe_allow_html=True)
