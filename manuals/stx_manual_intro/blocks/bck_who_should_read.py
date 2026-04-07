"""Who Should Read This Manual — prerequisites, goals, and orientation."""

from streamtex import *
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, st_slide_break


class BlockStyles:
    """Who should read styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    check_yes = s.project.colors.success_green + s.large
    check_no = s.project.colors.accent_teal + s.large
    manual_card = Style(
        "background: rgba(79, 172, 254, 0.06); "
        "border-left: 3px solid #4facfe; "
        "padding: 12px 16px; border-radius: 0 6px 6px 0;",
        "who_manual_card"
    )
    manual_title = s.project.colors.primary_blue + s.bold + s.large
    manual_desc = s.medium


bs = BlockStyles


def build():
    """Render the Who Should Read This Manual section."""
    st_space("v", 1)
    st_write(bs.heading, "Who Should Read This Manual?",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Prerequisites ───────────────────────────────────────────────
    st_write(bs.sub, "Prerequisites", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.bold + s.large, "What you need")
        st_space("v", 0.5)
        with st_list(list_type="ul", li_style=bs.body) as l:
            with l.item():
                st_write(
                    (s.bold, "No programming experience required"),
                    " — all examples are progressive and explained step by step",
                )
            with l.item():
                st_write(
                    (s.bold, "Basic Python knowledge"),
                    " is recommended to go further (variables, functions) "
                    "but not essential for the AI-assisted path",
                )

    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(s.bold + s.large, "What you do NOT need to know")
        st_space("v", 0.5)
        with st_list(list_type="ul", li_style=bs.body) as l:
            with l.item(): st_write("HTML, CSS, or JavaScript — StreamTeX handles all the web technology for you")
            with l.item(): st_write("LaTeX — built-in support for diagrams and formulas, no LaTeX installation needed")
            with l.item(): st_write("DevOps or Docker — deployment is pre-configured and optional")

    st_space("v", 1)

    show_explanation("""\
        **Two paths, same manual.** Whether you write code yourself
        or describe what you want to an AI assistant, this manual
        teaches the concepts that make you effective with StreamTeX.
        Understanding the building blocks helps you get better
        results — by hand or through AI.
    """)
    st_space("v", 2)

    # ── What you will learn ─────────────────────────────────────────
    st_write(bs.sub, "What you will learn", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "By the end of this manual, you will be able to:",
    )
    st_space("v", 0.5)

    with st_list(list_type="ol", li_style=bs.body) as l:
        with l.item(): st_write("Install StreamTeX and create your first project")
        with l.item(): st_write("Write styled text and compose visual styles")
        with l.item(): st_write("Build layouts with grids, lists, and containers")
        with l.item(): st_write("Add images, code blocks, and diagrams")
        with l.item(): st_write("Organize pages with book navigation and table of contents")
        with l.item(): st_write("Export to HTML or PDF and deploy online")
    st_space("v", 2)

    # ── Other manuals ───────────────────────────────────────────────
    st_write(bs.sub, "The other manuals", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "This Introduction covers the fundamentals. "
        "Five specialized manuals go deeper:",
    )
    st_space("v", 1)

    _manual(
        "Compound Engineering Manual",
        "Structured document production: a 7-phase cycle "
        "(collect → assess → plan → produce → review → fix → compound) "
        "with 17 AI agents and 3 pathways (import, improve, create).",
    )
    _manual(
        "AI Manual",
        "Learn to create and maintain documents entirely through natural "
        "language — without writing code. Commands, agents, and best practices.",
    )
    _manual(
        "Advanced Manual",
        "Deep dive into styles, overlays, advanced grids, diagrams, "
        "and the full rendering pipeline.",
    )
    _manual(
        "Deploy Manual",
        "Docker, Render, Streamlit Cloud, Hugging Face Spaces — "
        "deploy your documents to the web.",
    )
    _manual(
        "Developer Manual",
        "Contribute to the StreamTeX library: architecture, testing, "
        "CI/CD, and release process.",
    )
    _manual(
        "Collection Hub",
        "Browse all manuals in one place — the central documentation portal.",
    )

    st_space("v", 1)
    st_slide_break()


# ── Helpers ────────────────────────────────────────────────────────

def _manual(title: str, description: str):
    """Manual orientation card."""
    st_space("v", 0.3)
    with st_block(bs.manual_card):
        st_write(bs.manual_title, title)
        st_space("v", 0.3)
        st_write(bs.manual_desc, description)
