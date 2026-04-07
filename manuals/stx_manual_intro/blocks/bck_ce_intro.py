"""Compound Engineering — Introduction to structured document production.

Bridges to the full CE manual by showing the 7-phase cycle,
the 3 pathways, and how AI agents orchestrate the process.
"""

from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, st_slide_break


class BlockStyles:
    """CE intro styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    ce_banner = Style(
        "background: linear-gradient(135deg, rgba(0,172,193,0.10) 0%, "
        "rgba(79,172,254,0.10) 100%); "
        "border-radius: 8px; padding: 24px;",
        "ce_intro_banner"
    )
    ce_accent = Style("color: #00ACC1;", "ce_intro_accent")
    phase_card = Style(
        "background: rgba(0, 172, 193, 0.06); "
        "border-left: 3px solid #00ACC1; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ce_intro_phase_card"
    )
    phase_number = Style(
        "color: #00ACC1; font-weight: bold; font-size: 22pt; line-height: 1;",
        "ce_intro_phase_num"
    )
    phase_title = s.bold + s.large
    pathway_card = Style(
        "background: rgba(79, 172, 254, 0.06); "
        "border-left: 3px solid #4facfe; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ce_intro_pathway"
    )
    pathway_title = s.project.colors.primary_blue + s.bold + s.Large
    pathway_freq = s.project.colors.neutral_gray + s.medium
    manual_link = Style(
        "background: linear-gradient(135deg, rgba(0,172,193,0.08) 0%, "
        "rgba(79,172,254,0.08) 100%); "
        "border: 1px solid rgba(0,172,193,0.3); "
        "border-radius: 8px; padding: 20px;",
        "ce_intro_manual_link"
    )


bs = BlockStyles


def build():
    """Render the Compound Engineering introduction section."""
    st_space("v", 1)
    st_write(bs.heading, "Compound Engineering: Produce Documents Methodically",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── The insight ─────────────────────────────────────────────────
    with st_block(bs.ce_banner):
        st_write(
            s.Large + s.bold + s.center_txt,
            "From blank page to polished document — systematically",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large + s.center_txt + s.project.colors.neutral_gray,
            "Creating a document is more than writing content. "
            "You need to collect sources, define objectives, plan the structure, "
            "produce, review, fix issues, and capitalize on what you learned. ",
            (s.bold, "Compound Engineering"),
            " is the StreamTeX methodology that structures this entire process "
            "into a repeatable, AI-assisted cycle.",
            tag=t.div,
        )
    st_space("v", 2)

    # ── The 7-phase cycle ───────────────────────────────────────────
    st_write(bs.sub, "The 7-phase cycle", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "Every document goes through seven phases. "
        "Each phase has a dedicated command and specialized AI agents:",
    )
    st_space("v", 1)

    _phase("1", "Collect", "/stx-ce:collect",
           "Inventory and classify your source material (files, URLs, notes).")
    _phase("2", "Assess", "/stx-ce:assess",
           "Evaluate sources and define document objectives — auto-detects your pathway.")
    _phase("3", "Plan", "/stx-ce:plan",
           "Design the document structure, block list, and production schedule.")
    _phase("4", "Produce", "/stx-ce:produce",
           "Execute the plan — orchestrates stx-block and stx-import commands.")
    _phase("5", "Review", "/stx-ce:review",
           "Multi-perspective review: audience, pedagogy, visual, style, editorial.")
    _phase("6", "Fix", "/stx-ce:fix",
           "Correct issues found during review — iterable until quality is met.")
    _phase("7", "Compound", "/stx-ce:compound",
           "Capitalize learnings: production insights, ecosystem feedback, governance.")

    st_space("v", 1)

    show_explanation("""\
        The cycle is **iterative**: after Fix, you can loop back to Review
        until the document meets your quality standards. The Compound phase
        ensures that each project improves your future work.
    """)
    st_space("v", 2)
    st_slide_break()

    # ── Three pathways ──────────────────────────────────────────────
    st_write(bs.sub, "Three pathways", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "Compound Engineering adapts to your starting point "
        "with three distinct pathways:",
    )
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        _pathway(
            "Import",
            "Very frequent",
            "You have existing content (HTML, Marp, LaTeX, Markdown) "
            "and want to convert it into a StreamTeX project.",
        )
        _pathway(
            "Improve",
            "Frequent",
            "You have an existing StreamTeX project and want to "
            "enhance its quality, structure, or visual design.",
        )
        _pathway(
            "Create",
            "Occasional",
            "You start from scratch with a topic and objectives — "
            "the AI helps you build the document step by step.",
        )

    st_space("v", 2)

    # ── Full automation ─────────────────────────────────────────────
    st_write(bs.sub, "Full automation with /stx-ce:go", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        For a fully autonomous run, use **/stx-ce:go "your description"**.
        It executes all 7 phases with 3 validation gates where you can
        review progress and adjust direction. You can also pause
        (**/stx-ce:pause**) and resume (**/stx-ce:continue**) at any time.
    """)
    st_space("v", 2)

    # ── Go further ──────────────────────────────────────────────────
    st_write(bs.sub, "Go further: the CE Manual", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.manual_link):
        st_write(
            s.Large + s.bold + bs.ce_accent,
            "Compound Engineering Manual",
            tag=t.div,
        )
        st_space("v", 0.5)
        st_write(
            bs.body,
            "The dedicated manual covers the full methodology in depth:",
        )
        st_space("v", 0.5)
        with st_list(list_type="ul", li_style=bs.body) as l:
            with l.item(): st_write((s.bold, "Philosophy"), " — why structured production matters")
            with l.item(): st_write((s.bold, "Each phase in detail"), " — inputs, outputs, agents, and commands")
            with l.item(): st_write((s.bold, "Practical guides"), " — import, improve, create, and compound walkthroughs")
            with l.item(): st_write((s.bold, "17 AI agents"), " — content strategist, visual reviewer, and more")
            with l.item(): st_write((s.bold, "Reference"), " — commands, templates, configuration, and FAQ")
        st_space("v", 1)
        st_write(
            bs.body + s.project.colors.neutral_gray,
            "Available in the StreamTeX documentation collection "
            "at docs.streamtex.org.",
        )

    st_space("v", 2)
    st_slide_break()


# ── Helpers ────────────────────────────────────────────────────────

def _phase(number: str, title: str, command: str, description: str):
    """Phase card with number, title, command, and description."""
    st_space("v", 0.3)
    with st_block(bs.phase_card):
        st_write(
            bs.body,
            (bs.phase_number, f"{number}. "),
            (bs.phase_title, title),
            (s.project.colors.neutral_gray + s.medium, f"  {command}"),
        )
        st_space("v", 0.3)
        st_write(s.large, description)


def _pathway(title: str, frequency: str, description: str):
    """Pathway card: title, frequency tag, and description."""
    with st_block(bs.pathway_card):
        st_write(bs.pathway_title, title)
        st_write(bs.pathway_freq, frequency)
        st_space("v", 0.5)
        st_write(bs.body, description)
