"""Composite block — Presentation Mode."""

import streamtex as stx
from streamtex import st_include

bck_presentation_mode = stx.load_atomic_block("bck_presentation_mode", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_presentation_mode)
