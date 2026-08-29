"""Composite block: Multilingual Documents — block_kwargs + leaves/T()/TF() pattern."""
import streamtex as stx
from streamtex import st_include

bck_block_kwargs = stx.load_atomic_block("bck_block_kwargs", __file__)
bck_multilingual_pattern = stx.load_atomic_block("bck_multilingual_pattern", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_block_kwargs)
    st_include(bck_multilingual_pattern)
