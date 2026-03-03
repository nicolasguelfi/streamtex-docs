"""Composite block — Repository Structure."""

import streamtex as stx
from streamtex import st_include

bck_repo_overview = stx.load_atomic_block("bck_repo_overview", __file__)
bck_repo_source_modules = stx.load_atomic_block("bck_repo_source_modules", __file__)
bck_repo_support_files = stx.load_atomic_block("bck_repo_support_files", __file__)


class BlockStyles:
    pass


def build():
    st_include(bck_repo_overview)
    st_include(bck_repo_source_modules)
    st_include(bck_repo_support_files)
