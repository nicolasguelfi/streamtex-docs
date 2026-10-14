"""Composite block — Composing by Atoms (a list block of 7 atomic sub-blocks)."""

import streamtex as stx
from streamtex import st_sequence

bck_atoms_vocabulary = stx.load_atomic_block("bck_atoms_vocabulary", __file__)
bck_include_options = stx.load_atomic_block("bck_include_options", __file__)
bck_include_sequence = stx.load_atomic_block("bck_include_sequence", __file__)
bck_include_cycles = stx.load_atomic_block("bck_include_cycles", __file__)
bck_include_hot_reload = stx.load_atomic_block("bck_include_hot_reload", __file__)
bck_pages_follow_tree = stx.load_atomic_block("bck_pages_follow_tree", __file__)
bck_composition_live_demo = stx.load_atomic_block("bck_composition_live_demo", __file__)
# The demo list block of the chapter (not a section of it): _atomic/bck_demo_quiz_list.py,
# whose two atoms sit in its own _atomic/ folder. The sections reach it through this module.
bck_demo_quiz_list = stx.load_atomic_block("bck_demo_quiz_list", __file__)

ITEMS = [
    bck_atoms_vocabulary,
    bck_include_options,
    bck_include_sequence,
    bck_include_cycles,
    bck_include_hot_reload,
    bck_pages_follow_tree,
    bck_composition_live_demo,
]


class BlockStyles:
    """Composite block styles."""
    pass


bs = BlockStyles


def build():
    """A list block: only the order of its sections, nothing between them."""
    st_sequence(ITEMS, separator=None)
