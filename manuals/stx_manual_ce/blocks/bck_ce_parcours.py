"""The 3 Pathways — Detailed guide to CE pathways A, B, and C."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """CE Pathways styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.center_txt)
    header_cell = (s.container.borders.solid_border
                   + s.container.paddings.small_padding
                   + s.center_txt + s.bold)


bs = BlockStyles


def build():
    """Render the 3 pathways page."""
    st_space("v", 1)
    st_write(bs.heading, "The 3 Pathways",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Every CE cycle follows one of three pathways, determined during
        the ASSESS phase. The pathway shapes which phases are heavy
        and which are light. You can let CE auto-detect the pathway
        or force one with a flag.
    """)
    st_space("v", 2)

    # ── Pathway A: Import ─────────────────────────────────────────
    st_write(bs.sub, "Pathway A — Import external material", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You have files outside StreamTeX — HTML pages, Marp slides, "
             "PDFs, Markdown notes, or images — and want to turn them into "
             "a StreamTeX project.")
    st_space("v", 1)

    show_explanation("""\
        **When to use:** You received a slide deck from a colleague,
        exported a website, or have lecture notes in Markdown.

        **Key phases:** COLLECT scans and classifies every file.
        PRODUCE uses `stx-import` commands to convert formats.
        REVIEW checks that nothing was lost in conversion.

        **Trigger:** `/stx-ce:go --import ~/sources/ "training course"`
    """)
    st_space("v", 2)

    # ── Pathway B: Improve ────────────────────────────────────────
    st_write(bs.sub, "Pathway B — Improve an existing project", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You already have a StreamTeX project but it needs work: "
             "better structure, updated styles, new sections, or a "
             "design refresh.")
    st_space("v", 1)

    show_explanation("""\
        **When to use:** A project exists but looks dated, has
        inconsistent styles, or needs additional content.

        **Key phases:** ASSESS analyzes the current project deeply.
        PLAN identifies specific improvements. REVIEW compares
        before and after.

        **Trigger:** `/stx-ce:go "modernize the intro and add diagrams"`
        (auto-detected when run inside an existing project)
    """)
    st_space("v", 2)

    # ── Pathway C: Create ─────────────────────────────────────────
    st_write(bs.sub, "Pathway C — Create a new document", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "You start from a description, an outline, or just an idea. "
             "No existing material to import or project to improve.")
    st_space("v", 1)

    show_explanation("""\
        **When to use:** Starting a new course, report, or presentation
        from scratch with only a topic description.

        **Key phases:** PLAN is the heaviest phase — defining structure,
        block breakdown, and style palette. PRODUCE generates everything
        via `stx-designer:init`.

        **Trigger:** `/stx-ce:go "create a 5-chapter ML course"`
    """)
    st_space("v", 2)

    # ── Comparison table ──────────────────────────────────────────
    st_write(bs.sub, "Comparison", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=4, cell_styles=bs.cell) as g:
        # Header row
        with g.cell(): st_write(s.bold + s.large, "")
        with g.cell(): st_write(s.bold + s.large, "A — Import")
        with g.cell(): st_write(s.bold + s.large, "B — Improve")
        with g.cell(): st_write(s.bold + s.large, "C — Create")
        # Starting point
        with g.cell(): st_write(s.bold + s.large, "Starting point")
        with g.cell(): st_write(s.large, "External files")
        with g.cell(): st_write(s.large, "Existing STX project")
        with g.cell(): st_write(s.large, "Description / outline")
        # Heaviest phase
        with g.cell(): st_write(s.bold + s.large, "Heaviest phase")
        with g.cell(): st_write(s.large, "COLLECT + PRODUCE")
        with g.cell(): st_write(s.large, "ASSESS + REVIEW")
        with g.cell(): st_write(s.large, "PLAN + PRODUCE")
        # Main tool
        with g.cell(): st_write(s.bold + s.large, "Main tool")
        with g.cell(): st_write(s.large, "stx-import")
        with g.cell(): st_write(s.large, "stx-designer:update")
        with g.cell(): st_write(s.large, "stx-designer:init")
        # Typical duration
        with g.cell(): st_write(s.bold + s.large, "Typical duration")
        with g.cell(): st_write(s.large, "15-60 min")
        with g.cell(): st_write(s.large, "10-30 min")
        with g.cell(): st_write(s.large, "5-20 min")
    st_space("v", 2)

    show_details("""\
        The durations above are for a single CE cycle with AI assistance.
        Complex projects may require multiple cycles. The COMPOUND phase
        at the end of each cycle ensures that subsequent cycles are faster.
    """)
    st_space("v", 1)
