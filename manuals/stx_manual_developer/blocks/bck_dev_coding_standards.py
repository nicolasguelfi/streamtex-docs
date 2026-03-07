"""Composite block — Coding Standards."""

import streamtex as stx
from streamtex import st_include

bck_standards_general = stx.load_atomic_block("bck_standards_general", __file__)
bck_standards_module = stx.load_atomic_block("bck_standards_module", __file__)
bck_standards_export_guard = stx.load_atomic_block("bck_standards_export_guard", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_standards_general)
    st_include(bck_standards_module)
    st_include(bck_standards_export_guard)
