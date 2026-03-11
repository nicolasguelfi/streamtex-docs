"""Composite block: PDF Export."""
import streamtex as stx
from streamtex import st_include

bck_pdf = stx.load_atomic_block("bck_pdf_export", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_pdf)
