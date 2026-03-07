"""Composite block — Architecture Deep-Dive."""

import streamtex as stx
from streamtex import st_include

bck_arch_rendering = stx.load_atomic_block("bck_arch_rendering", __file__)
bck_arch_styles = stx.load_atomic_block("bck_arch_styles", __file__)
bck_arch_blocks = stx.load_atomic_block("bck_arch_blocks", __file__)
bck_arch_export = stx.load_atomic_block("bck_arch_export", __file__)
bck_arch_book = stx.load_atomic_block("bck_arch_book", __file__)


class BlockStyles:
    """Composite block styles."""
    pass


bs = BlockStyles


def build():
    """Include atomic blocks for this section."""
    st_include(bck_arch_rendering)
    st_include(bck_arch_styles)
    st_include(bck_arch_blocks)
    st_include(bck_arch_export)
    st_include(bck_arch_book)
