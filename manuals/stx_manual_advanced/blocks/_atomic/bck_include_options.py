"""Composing by Atoms — the options of st_include.

Covers: the signature, markers= (True / False / "hidden" / a mapping,
validated live), nesting (the outer inclusion wins), anchors kept,
break_before=, page=, and the reserved keywords.
"""

import streamtex as stx
from streamtex import st_block, st_include, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from streamtex.marker import normalize_markers_arg
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation
import blocks


class BlockStyles:
    """st_include options styles."""
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles

#: The values shown in the live table, with what they do.
_MARKER_VALUES = [
    (True, "unchanged (default)"),
    (False, "no stop, not listed — each marker keeps its anchor and its deep link"),
    ("hidden", "stops kept, none listed"),
    ({"stop": False}, "each key present forces that role; absent keys keep the marker's own"),
    ({"listed": True}, "forces the role on: hidden break markers become listed"),
    ({"toc": False}, "also drops the TOC entries of the included build()"),
]

#: Invalid values: each raises ValueError before build() runs.
_INVALID_VALUES = ["foo", {"toc": True}, {"stop": 1}, {"color": False}]


def build():
    st_write(bs.sub, "st_include — the options of an inclusion", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        `st_include(block)` runs another block's `build()` in place, like
        `\\input` in LaTeX. Positional and keyword arguments reach that
        `build()`; three keywords belong to the inclusion itself and are
        **not** passed on: `markers`, `break_before` and `page`.
    """)
    st_space("v", 1)

    show_code("""\
        st_include(block, *args,
                   markers=True,        # True | False | "hidden" | {"stop"/"listed"/"toc": bool}
                   break_before=False,  # True | False | a SlideBreakConfig
                   page=None,           # None | True | False (paginate_by, below)
                   **kwargs)            # *args and **kwargs reach block.build()""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # markers=
    # ------------------------------------------------------------------
    st_write(bs.feature, "markers= — the roles of the included markers")
    st_space("v", 1)

    show_explanation("""\
        `markers` changes the roles of **every marker the included
        `build()` places**: its own `st_marker` calls, the markers of its
        breaks (and of `st_slide(cut=True)`), the markers of its headings,
        at any depth of nested inclusions. The table below is computed live
        by the function `st_include` uses to read the value.
    """)
    st_space("v", 1)

    stx.st_table({
        "markers=": [repr(v) for v, _ in _MARKER_VALUES],
        "role override": [repr(normalize_markers_arg(v)) for v, _ in _MARKER_VALUES],
        "effect": [effect for _, effect in _MARKER_VALUES],
    })
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "The layout never changes"),
                         " — rules, spacers, spacing and content are drawn identically "
                         "whatever the value; only navigation changes.")
            with lst.item():
                st_write(bs.body, (bs.term, "Anchors are kept"),
                         " — a marker with no role left is still registered with its "
                         "anchor, so ?marker= and #anchor links to it keep working.")
            with lst.item():
                st_write(bs.body, (bs.term, "TOC entries stay"),
                         " — True, False and \"hidden\" never touch the TOC; only "
                         "{\"toc\": False} removes the included headings from it (they are "
                         "still rendered as text, and the following entries renumber).")
            with lst.item():
                st_write(bs.body, (bs.term, "Typical use"),
                         " — a host slide that already has its marker includes a block "
                         "that opens with its own: markers=False gives one stop instead "
                         "of two, without editing the included block.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Nesting
    # ------------------------------------------------------------------
    st_write(bs.feature, "Nested inclusions — the outer inclusion wins")
    st_space("v", 1)

    show_explanation("""\
        The override is inherited by every inclusion made inside the
        included `build()`. When two inclusions set the same role, the
        **outer** one wins: the block that composes decides about what it
        includes, including what its list blocks decided. Markers placed
        by the host itself, before or after the call, are not affected.
    """)
    st_space("v", 1)

    show_code("""\
        # blocks/bck_part.py — a list block hides the names of a composite
        def build(**kwargs):
            st_include(bck_pipeline, markers="hidden", **kwargs)   # {"listed": False}

        # the module includes the list block
        st_include(bck_part, markers=False)        # no marker of the subtree is a stop or listed
        st_include(bck_part, markers={"listed": True})
        # bck_pipeline's markers are listed again: the outer "listed" wins over the inner one""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Validation, live
    # ------------------------------------------------------------------
    st_write(bs.feature, "Invalid values fail before anything is drawn")
    st_space("v", 1)

    st_write(s.large, "Each call below includes the quiz question atom of the live demo "
                      "(last section of this chapter) "
                      "with an invalid markers=. The ValueError is raised before build() "
                      "runs, so the atom never appears. Messages caught live:")
    st_space("v", 1)

    atom = blocks.bck_composing_by_atoms.bck_demo_quiz_list.bck_demo_quiz_question
    messages = []
    for value in _INVALID_VALUES:
        try:
            st_include(atom, markers=value)
        except ValueError as err:
            messages.append(str(err))
    with st_block(s.project.containers.result_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            for msg in messages:
                with lst.item():
                    st_write(bs.body, msg)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # break_before= and page=
    # ------------------------------------------------------------------
    st_write(bs.feature, "break_before= and page=")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            with lst.item():
                st_write(bs.body, (bs.term, "break_before=True"),
                         " — the standard break before the block: the module's break "
                         "settings (set_slide_break_config), no marker. It belongs to the "
                         "host: this inclusion's markers= does not apply to it.")
            with lst.item():
                st_write(bs.body, (bs.term, "break_before=SlideBreakConfig(…)"),
                         " — that break, used as given, its marker included.")
            with lst.item():
                st_write(bs.body, (bs.term, "page=True | False"),
                         " — with st_book(paginate_by=…) other than \"entry\": True starts "
                         "a page with the whole subtree, False keeps it on the enclosing "
                         "page; None (default) lets paginate_by decide. See Pages that "
                         "follow the tree, below.")
    st_space("v", 1)

    show_details("""\
        Any other value of `page` or `break_before` raises `TypeError`.
        `markers`, `break_before` and `page` are reserved keywords of
        `st_include`: a block whose `build()` takes a parameter with one of
        these names can no longer receive it through `st_include`.
    """)
    st_space("v", 2)
