"""Composite block — Release Process."""

import streamtex as stx
from streamtex import st_include

bck_release_checklist = stx.load_atomic_block("bck_release_checklist", __file__)
bck_release_version_sync = stx.load_atomic_block("bck_release_version_sync", __file__)
bck_release_publish = stx.load_atomic_block("bck_release_publish", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_release_checklist)
    st_include(bck_release_version_sync)
    st_include(bck_release_publish)
