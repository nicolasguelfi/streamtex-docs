"""Shared header block for training courses."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t

_LOGO = "https://raw.githubusercontent.com/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png"


class BlockStyles:
    """Shared header styles."""
    header = Style(
        "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "training_header"
    )
    header_text = Style("color: white;", "training_header_text")
    logo = Style("width: 100%; height: auto;", "training_logo")
    logo_cell = Style("display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;", "training_logo_cell")
bs = BlockStyles


def build():
    """Render a standard training course header."""
    st_space("v", 1)

    with st_block(bs.header):
        with st_grid(cols="25% 75%", cell_styles=[bs.logo_cell, None]) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button("❤️ Support us!", "https://github.com/sponsors/nicolasguelfi", use_container_width=True)
            with g.cell():
                st_write(
                    stx.StxStyles.LARGE + stx.StxStyles.bold + bs.header_text,
                    "StreamTeX Training Course",
                    tag=t.div
                )
                st_write(
                    stx.StxStyles.large + bs.header_text,
                    "A Streamlit-based content rendering framework",
                    tag=t.div
                )
    st_space("v", 1)
