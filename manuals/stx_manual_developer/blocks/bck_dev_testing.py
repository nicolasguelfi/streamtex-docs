"""Composite block — Testing."""

import streamtex as stx
from streamtex import st_include

bck_testing_run = stx.load_atomic_block("bck_testing_run", __file__)
bck_testing_patterns = stx.load_atomic_block("bck_testing_patterns", __file__)
bck_testing_gotchas = stx.load_atomic_block("bck_testing_gotchas", __file__)
bck_testing_coverage = stx.load_atomic_block("bck_testing_coverage", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_testing_run)
    st_include(bck_testing_patterns)
    st_include(bck_testing_gotchas)
    st_include(bck_testing_coverage)
