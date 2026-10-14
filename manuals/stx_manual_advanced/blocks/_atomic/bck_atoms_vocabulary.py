"""Composing by Atoms — the vocabulary of the composition method.

Covers: atom, composite, list block, section, module tree, flattening,
the block forms S / B / D, the scrolling slide, and the marker roles in
short (the Marker Navigation chapter has the details).
"""

from pathlib import Path

from streamtex import st_block, st_list, st_space, st_write
from streamtex.enums import ListTypes as lt
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


class BlockStyles:
    """Vocabulary styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    term = s.medium + s.text.weights.bold_weight
    body = s.medium


bs = BlockStyles

#: This chapter's own file: it is itself a list block (shown live below).
_CHAPTER_FILE = Path(__file__).resolve().parent.parent / "bck_composing_by_atoms.py"


def _terms(rows):
    """A list of (term, definition) rows, the term in bold, inline."""
    with st_block(s.project.containers.explanation_box):
        with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as lst:
            for term, text in rows:
                with lst.item():
                    st_write(bs.body, (bs.term, term), f" — {text}")


def build():
    st_write(bs.heading, "Composing by Atoms", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        A module can be **composed** from small blocks instead of being
        written as a few long ones: one-slide blocks (*atoms*), a few
        blocks that keep several slides together (*composites*), and
        blocks that only hold the order of other blocks (*list blocks*).
        `st_include` puts one block inside another, `st_sequence` puts
        several in order with a break between two.

        The same atom can then appear in several modules, a list can be
        reordered in one line, and the presenter still steps through one
        slide per arrow press.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Vocabulary
    # ------------------------------------------------------------------
    st_write(bs.sub, "Vocabulary", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, "Each word below has one meaning in this chapter.")
    st_space("v", 1)

    _terms([
        ("Atom", "a block of ONE slide. Its named marker comes first, then its "
                 "content in a slide box; never a break inside."),
        ("Composite", "a block that keeps several slides together (for instance a "
                      "grid spanning several slides). It has breaks inside."),
        ("List block", "a block whose build() only holds the order of other blocks "
                       "(atoms, composites, other list blocks), usually in an ITEMS "
                       "list. No text, no marker of its own; the breaks go between "
                       "its items."),
        ("Section", "a list block that carries a table-of-contents heading. This is "
                    "the only meaning of the word in this chapter."),
        ("Module tree", "module → list blocks → … → atoms and composites → slides, "
                        "with no cycle."),
        ("Flattening", "the slide sequence obtained by a left-hand, depth-first walk "
                       "of the tree. It is what the presenter steps through, whatever "
                       "the depth; pages only cut its loading."),
        ("Leaf", "an inclusion that includes no other block: an atom or a "
                 "composite (used by paginate_by=\"leaf\")."),
    ])
    st_space("v", 2)

    show_code("""\
        # blocks/_atomic/bck_rag_definition.py — an atom: one slide
        from streamtex import st_slide, st_write
        from custom.styles import Styles as s

        def build(**_):
            with st_slide(marker="RAG"):          # its named marker, then its box
                st_write(s.huge, "Retrieval-augmented generation")

        # blocks/bck_rag.py — a list block: only the order of its items
        import streamtex as stx
        from streamtex import st_sequence

        bck_rag_definition = stx.load_atomic_block("bck_rag_definition", __file__)
        bck_rag_pipeline = stx.load_atomic_block("bck_rag_pipeline", __file__)   # a composite

        ITEMS = [bck_rag_definition, bck_rag_pipeline]

        def build(*args, **kwargs):
            st_sequence(ITEMS, *args, **kwargs)""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Block forms
    # ------------------------------------------------------------------
    st_write(bs.sub, "Block forms and the scrolling slide", toc_lvl="+1")
    st_space("v", 1)

    _terms([
        ("Form S", "each slide in a slide box: with st_slide(): … (the atom's form)."),
        ("Form B", "free content cut by breaks, inside a composite: "
                   "with st_slide(cut=True, box=False): …"),
        ("Form D", "content taller than the screen that scrolls, with no box and no "
                   "break: with st_slide(marker=\"X\", box=False): …"),
        ("Scrolling slide", "a slide deliberately taller than the screen. It has one "
                            "marker at its head; the reader then scrolls."),
    ])
    st_space("v", 1)

    st_write(s.large, "st_slide, its marker= and box= options are described in the "
                      "Presentation Mode chapter.")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Marker roles, in short
    # ------------------------------------------------------------------
    st_write(bs.sub, "Marker roles, in short", toc_lvl="+1")
    st_space("v", 1)

    _terms([
        ("Stop", "the arrows, the keys and the counter n / N stop here."),
        ("Listed", "it is a row of the marker list (☰ popup, Markers tab, page titles)."),
        ("In TOC", "it is linked to a table-of-contents entry."),
    ])
    st_space("v", 1)

    show_explanation("""\
        The composition rule is **one stop per slide**: an atom brings its
        own marker, a list block places none, and the breaks that
        `st_sequence` draws between items place none either. When a block
        is included somewhere its markers do not fit, the inclusion changes
        their roles (`st_include(..., markers=…)`, next section) instead of
        the block being edited.

        The three roles, `MarkerRoles` and every combination are documented
        in the **Marker Navigation** chapter.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # This chapter is a list block
    # ------------------------------------------------------------------
    show_details("""\
        **This chapter is itself a list block.** Its entry in `book.py` is
        `blocks.bck_composing_by_atoms`, whose `build()` only calls
        `st_sequence` on its atomic sub-blocks, with `separator=None`
        because a document chapter needs no break between its sections.
        Its file, read live:
    """)
    st_space("v", 1)
    show_code(_CHAPTER_FILE.read_text(encoding="utf-8"))
    st_space("v", 2)
