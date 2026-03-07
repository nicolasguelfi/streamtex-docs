"""Shared footer block for training courses."""

import streamlit as st
from streamtex import *
import streamtex as stx


class BlockStyles:
    """Shared footer styles."""
    pass
bs = BlockStyles


def build():
    """Render a standard training course footer."""
    st_space("v", 2)
    st.divider()
    st_write(
        stx.StxStyles.small + stx.StxStyles.text.colors.reset + stx.StxStyles.center_txt,
        "StreamTeX © 2026 Nicolas Guelfi | "
        "[GitHub](https://github.com/nicolasguelfi/streamtex) · "
        "[Sponsor](https://github.com/sponsors/nicolasguelfi)"
    )
