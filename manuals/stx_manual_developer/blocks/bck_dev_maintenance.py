"""Composite block — Maintenance."""

import streamtex as stx
from streamtex import st_include

bck_maint_deps = stx.load_atomic_block("bck_maint_deps", __file__)
bck_maint_ruff = stx.load_atomic_block("bck_maint_ruff", __file__)
bck_maint_tooling = stx.load_atomic_block("bck_maint_tooling", __file__)


class BlockStyles:
    pass


def build():
    st_include(bck_maint_deps)
    st_include(bck_maint_ruff)
    st_include(bck_maint_tooling)
