"""Composite block — GitHub Issues and /stx-issue command."""

import streamtex as stx
from streamtex import st_include

bck_github_issues = stx.load_atomic_block("bck_github_issues", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_github_issues)
