"""Shared changelog block — reads CHANGELOG.md and renders it as the last section."""

import streamlit as st
from pathlib import Path
from streamtex import st_write, st_space, st_block
from streamtex.styles import Style
from streamtex.enums import Tags as t


# manuals/shared-blocks/blocks/bck_changelog.py → ../../../../CHANGELOG.md
_CHANGELOG = Path(__file__).resolve().parent.parent.parent.parent / "CHANGELOG.md"


class BlockStyles:
    heading = Style("font-size:1.6em; font-weight:bold; text-align:center;", "changelog_heading")
    body = Style("font-size:1.1em; line-height:1.6;", "changelog_body")


bs = BlockStyles


def build():
    """Render the documentation changelog."""
    st_space("v", 2)
    st.markdown('<div id="changelog"></div>', unsafe_allow_html=True)
    st_write(
        bs.heading,
        "Changelog",
        tag=t.div,
        toc_lvl="1",
    )
    st_space("v", 1)
    if _CHANGELOG.exists():
        content = _CHANGELOG.read_text(encoding="utf-8")
        # Skip the "# Changelog ..." header line
        lines = content.split("\n")
        start = 0
        for i, line in enumerate(lines):
            if line.startswith("# "):
                start = i + 1
                break
        body = "\n".join(lines[start:]).strip()
        with st_block(bs.body):
            st.markdown(body)
    else:
        st_write(None, "No changelog available.")
    st_space("v", 2)
