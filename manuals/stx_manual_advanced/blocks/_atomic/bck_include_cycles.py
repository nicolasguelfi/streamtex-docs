"""Composing by Atoms — include cycles (IncludeCycleError).

Covers: a block that includes itself, directly or through other blocks,
is refused with IncludeCycleError naming the chain (raised and caught
live), what the reader sees, and the exit codes of the stx commands.
"""

import types

from streamtex import IncludeCycleError, st_block, st_include, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


class BlockStyles:
    """Include cycle styles."""
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles


# ----------------------------------------------------------------------
# Live demo blocks. A block is any object with a build(): three small
# in-memory modules named like the files of the example, so the chain
# reads lists.a → lists.b → lists.a.
# ----------------------------------------------------------------------
lists_a = types.ModuleType("lists.a")
lists_b = types.ModuleType("lists.b")
atoms_note = types.ModuleType("atoms.note")
lists_repeat = types.ModuleType("lists.repeat")


def _build_a(**_):
    st_include(lists_b)


def _build_b(**_):
    st_include(lists_a)


def _build_note(**_):
    st_write(bs.body, "atoms.note rendered")


def _build_repeat(**_):
    st_include(atoms_note)
    st_include(atoms_note)          # the same block twice in a row: not a cycle


lists_a.build = _build_a
lists_b.build = _build_b
atoms_note.build = _build_note
lists_repeat.build = _build_repeat


def build():
    st_write(bs.sub, "Include cycles — IncludeCycleError", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A module tree has no cycle. A block that includes itself, directly
        or through other blocks, is refused at the **first re-entry**,
        before anything of it is drawn, with an `IncludeCycleError` that
        names the chain. Including the same block several times **in a
        row** stays allowed: only a block still in progress cannot be
        entered again.
    """)
    st_space("v", 1)

    show_code("""\
        # lists/a.py                       # lists/b.py
        def build(**kw):                   def build(**kw):
            st_include(b, **kw)                st_include(a, **kw)   # back to a: a cycle""",
              language="python", line_numbers=False)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Live: a cycle
    # ------------------------------------------------------------------
    st_write(bs.feature, "Live — a cycle raised and caught")
    st_space("v", 1)

    st_write(s.large, "The call below includes lists.a, which includes lists.b, which "
                      "includes lists.a again. The red line is the message the reader "
                      "sees: one message, shown by the innermost inclusion.")
    st_space("v", 1)

    show_code("""\
        try:
            st_include(lists_a)
        except IncludeCycleError as err:
            err.chain    # the cycle, first == last
            err.stack    # every inclusion in progress, outermost first""")
    st_space("v", 1)

    try:
        st_include(lists_a)
    except IncludeCycleError as err:
        with st_block(s.project.containers.result_box):
            with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
                with lst.item():
                    st_write(bs.body, (bs.term, "str(err): "), str(err))
                with lst.item():
                    st_write(bs.body, (bs.term, "err.chain: "), repr(err.chain))
                with lst.item():
                    st_write(bs.body, (bs.term, "err.stack: "), repr(err.stack))
    st_space("v", 1)

    st_write(s.large, "err.stack starts with this chapter and its sub-block: the "
                      "inclusions in progress when the cycle was met.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Live: a repetition is not a cycle
    # ------------------------------------------------------------------
    st_write(bs.feature, "Live — the same block twice in a row")
    st_space("v", 1)

    st_write(s.large, "lists.repeat includes atoms.note twice; no error:")
    st_space("v", 1)
    with st_block(s.project.containers.result_box):
        st_include(lists_repeat)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # What happens where
    # ------------------------------------------------------------------
    st_write(bs.feature, "What the reader and the tools see")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "In the app"),
                         " — one red message per block error, at the innermost inclusion "
                         "(not one per level of nesting); the error then propagates through the "
                         "enclosing inclusions, which add no message. The "
                         "paginated app shows the cycle with st.error and saves no page "
                         "cache.")
            with lst.item():
                st_write(bs.body, (bs.term, "stx export html, stx cache warmup"),
                         " — fail with exit code 1 on an include cycle and write nothing. "
                         "Other block errors are still logged and the entry skipped.")
            with lst.item():
                st_write(bs.body, (bs.term, "stx validate --build"),
                         " — runs each entry through st_include, so the cycle is reported "
                         "with its chain, named from the entry.")
    st_space("v", 1)

    show_details("""\
        The inclusions in progress are recorded by the block's **real file
        path**, so a block reloaded into a new module object, or imported
        under two names, is still recognised as the same block.
    """)
    st_space("v", 2)
