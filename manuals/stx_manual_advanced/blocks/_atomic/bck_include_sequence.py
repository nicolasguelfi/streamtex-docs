"""Composing by Atoms — list blocks and st_sequence.

Covers: st_sequence(items, *args, separator=, markers=, **kwargs), the
list-block pattern, the equivalent with st_include(break_before=), and a
live list block of two atoms whose registry entries are read back.
"""

from streamtex import st_block, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


class BlockStyles:
    """st_sequence styles."""
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles


def build():
    st_write(bs.sub, "List blocks — st_sequence", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        `st_sequence(items, *args, separator="break", markers=True, **kwargs)`
        includes blocks in order and draws a separator **between** two of
        them: never before the first, never after the last. It is the
        whole body of a list block.
    """)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_part_one.py — a list block
                from streamtex import st_sequence
        import blocks

        bck_intro = stx.load_atomic_block("bck_intro", __file__)
        bck_detail = stx.load_atomic_block("bck_detail", __file__)

        ITEMS = [bck_intro, bck_detail, blocks.bck_examples]   # two atoms, then another list block

        def build(*args, **kwargs):
            st_sequence(ITEMS, *args, **kwargs)              # args and kwargs reach every item""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "separator=\"break\""),
                         " (default) — the standard break: the module's break settings, "
                         "no marker, since each item brings its own.")
            with lst.item():
                st_write(bs.body, (bs.term, "separator=SlideBreakConfig(…)"),
                         " — that break, used as given (set marker=False to keep one "
                         "stop per slide).")
            with lst.item():
                st_write(bs.body, (bs.term, "separator=None"),
                         " — nothing between the items.")
            with lst.item():
                st_write(bs.body, (bs.term, "separator=<a block>"),
                         " — its build() between two items, as st_book(separator=…); it "
                         "receives the same args and kwargs.")
            with lst.item():
                st_write(bs.body, (bs.term, "markers="),
                         " — passed to every item's st_include; the breaks have no marker "
                         "anyway.")
    st_space("v", 1)

    show_details("""\
        **Why the break carries no marker.** Each item already opens with
        its own stop. A full `st_slide_break()` between items would add a
        second stop at every boundary: one arrow press would not move the
        screen. One break before a single inclusion is
        `st_include(block, break_before=True)`; `st_sequence(ITEMS)` is the
        same as including the first item, then each other one with
        `break_before=True`.
    """)
    st_space("v", 2)

    st_write(s.large, "The last section of this chapter renders a list block of two "
                      "atoms live, with the registry entries its markers place.")
    st_space("v", 2)
