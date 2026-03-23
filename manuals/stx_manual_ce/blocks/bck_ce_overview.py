"""What is Compound Document Engineering? — CE methodology overview."""

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """CE Overview styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Render the CE overview page."""
    st_space("v", 1)
    st_write(bs.heading, "What is Compound Document Engineering?",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Why CE exists ─────────────────────────────────────────────
    st_write(bs.sub, "Why CE exists", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Most document projects do not start from a blank page.
        You have slides from a previous talk, notes from a meeting,
        a PDF from a colleague, or HTML from a website.

        Traditional approaches assume top-down authoring: outline first,
        then write. CE takes the opposite approach — **bottom-up** — because
        that matches how real work happens: you start from existing material
        and shape it into a coherent document.
    """)
    st_space("v", 1)

    # ── Ad-hoc vs CE ─────────────────────────────────────────────
    st_write(bs.sub, "Ad-hoc production vs CE", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             (s.bold, "Ad-hoc production"), " copies, pastes, and reformats "
             "material by hand. It works for small tasks but does not scale: "
             "lessons are lost, quality is inconsistent, and every project "
             "starts from scratch.")
    st_space("v", 1)
    st_write(s.large,
             (s.bold, "CE"), " adds structure with a repeatable 7-phase cycle. "
             "Each cycle produces a better document ", (s.italic, "and"),
             " captures what you learned for next time.")
    st_space("v", 2)

    # ── The 7-phase cycle ─────────────────────────────────────────
    st_write(bs.sub, "The 7-phase cycle", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A CE cycle has seven phases executed in order.
        Each phase has a clear input, output, and validation gate.

        **COLLECT** — Inventory and classify existing material.
        **ASSESS** — Evaluate material and define document objectives.
        **PLAN** — Design the production plan (structure, blocks, styles).
        **PRODUCE** — Execute the plan using stx-designer and stx-import.
        **REVIEW** — Multi-perspective quality review (5 lenses).
        **FIX** — Correct issues found during review.
        **COMPOUND** — Capitalize learnings for future cycles.
    """)
    st_space("v", 1)

    with st_list(list_type=lt.ordered, li_style=s.large, align="center") as l:
        with l.item(): st_write((s.project.titles.phase_kw, "COLLECT"), " — scan files, classify formats, evaluate importability")
        with l.item(): st_write((s.project.titles.phase_kw, "ASSESS"), " — detect pathway (A/B/C), define objectives and constraints")
        with l.item(): st_write((s.project.titles.phase_kw, "PLAN"), " — structure, block list, style choices, production order")
        with l.item(): st_write((s.project.titles.phase_kw, "PRODUCE"), " — create or import blocks, wire book.py, apply styles")
        with l.item(): st_write((s.project.titles.phase_kw, "REVIEW"), " — audience, pedagogy, visual, style, editorial checks")
        with l.item(): st_write((s.project.titles.phase_kw, "FIX"), " — correct automatable issues, verify manually")
        with l.item(): st_write((s.project.titles.phase_kw, "COMPOUND"), " — production log, ecosystem feedback, governance")
    st_space("v", 2)

    # ── Iterative nature ──────────────────────────────────────────
    st_write(bs.sub, "Iterative, not waterfall", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        The REVIEW and FIX phases form a tight inner loop: review
        findings feed directly into fixes, and you can re-review
        until quality gates pass.

        The COMPOUND phase closes the outer loop: lessons learned
        in one cycle improve the next. Over time, your templates,
        styles, and processes get better automatically.

        You can run a full cycle with `/stx-ce:go "description"`
        or execute phases individually for fine-grained control.
    """)
    st_space("v", 1)
