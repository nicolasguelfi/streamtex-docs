"""Shared header block for training courses."""

from pathlib import Path
from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t

_LOGO = str(Path(__file__).parent.parent / "logo-stx.png")


class BlockStyles:
    """Shared header styles."""
    header = Style(
        "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "training_header"
    )
    header_text = Style("color: white;", "training_header_text")
    logo = Style("max-width: 120px; margin: 0 auto 16px auto; display: block;", "training_logo")
bs = BlockStyles


def build():
    """Render a standard training course header."""
    st_space("v", 1)

    with st_block(bs.header):
        st_image(bs.logo, uri=_LOGO)
        st_write(
            stx.StxStyles.huge + stx.StxStyles.bold + bs.header_text,
            "StreamTeX Training Course",
            tag=t.div
        )
        st_write(
            stx.StxStyles.large + bs.header_text,
            "A Streamlit-based content rendering framework",
            tag=t.div
        )
    st_space("v", 1)
