"""Composite block — Claude Profiles."""

import streamtex as stx
from streamtex import st_include

bck_claude_structure = stx.load_atomic_block("bck_claude_structure", __file__)
bck_claude_profiles_mgmt = stx.load_atomic_block("bck_claude_profiles_mgmt", __file__)


class BlockStyles:
    pass


def build():
    st_include(bck_claude_structure)
    st_include(bck_claude_profiles_mgmt)
