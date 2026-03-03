"""Composite block — Development Setup."""

import streamtex as stx
from streamtex import st_include

bck_setup_clone = stx.load_atomic_block("bck_setup_clone", __file__)
bck_setup_workspace = stx.load_atomic_block("bck_setup_workspace", __file__)
bck_setup_editable = stx.load_atomic_block("bck_setup_editable", __file__)


class BlockStyles:
    """Composite block styles."""
    pass


def build():
    """Include atomic blocks for this section."""
    st_include(bck_setup_clone)
    st_include(bck_setup_workspace)
    st_include(bck_setup_editable)
