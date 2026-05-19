"""Why StreamTeX — Profiles, capabilities, and 10 reasons to choose the library."""

from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s


class BlockStyles:
    """Why StreamTeX styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    pitch = Style(
        "background: linear-gradient(135deg, rgba(79,172,254,0.08) 0%, "
        "rgba(0,242,254,0.08) 100%); border-radius: 8px; padding: 24px;",
        "why_pitch"
    )
    profile_card = Style(
        "background: rgba(79, 172, 254, 0.06); "
        "border-left: 3px solid #4facfe; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "why_profile_card"
    )
    profile_icon = s.huge + s.center_txt
    profile_title = s.project.colors.accent_teal + s.bold + s.large
    profile_pain = Style("color: #F1C40F;", "why_profile_pain") + s.medium
    profile_gain = s.project.colors.success_green + s.medium
    reason_number = Style(
        "color: #4facfe; font-weight: bold; font-size: 28pt; "
        "line-height: 1;",
        "why_reason_number"
    )
    reason_title = s.bold + s.large
    reason_body = s.large
    ai_highlight = Style(
        "background: linear-gradient(135deg, rgba(142,68,223,0.10) 0%, "
        "rgba(79,172,254,0.10) 100%); "
        "border-left: 4px solid #8E44DF; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "why_ai_highlight"
    )
    ai_label = Style(
        "color: #8E44DF; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "why_ai_label"
    )


bs = BlockStyles


def build():
    """Render the Why StreamTeX section."""
    st_space("v", 1)
    st_write(bs.heading, "Why StreamTeX?", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Opening pitch ───────────────────────────────────────────────
    with st_block(bs.pitch):
        st_write(
            s.Large + s.bold + s.center_txt,
            "Creating rich documents should not require choosing "
            "between power and simplicity.",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large + s.center_txt + s.project.colors.neutral_gray,
            "Traditional tools force a compromise: visual editors "
            "are easy but limited, while technical tools like LaTeX "
            "are powerful but hard to learn. StreamTeX removes this "
            "trade-off — you write in Python and get professional "
            "documents, with or without coding.",
            tag=t.div,
        )

    st_space("v", 2)
    st_slide_break()

    # ── 10 reasons ──────────────────────────────────────────────────
    st_write(bs.sub, "10 reasons to choose StreamTeX", toc_lvl="+1")
    st_space("v", 1)

    # Reason 1 — AI native (highlighted)
    with st_block(bs.ai_highlight):
        st_write(bs.ai_label, "Reason #1")
        st_space("v", 0.5)
        st_write(
            s.Large + s.bold,
            "Built for generative AI",
        )
        st_space("v", 0.5)
        st_write(
            bs.body,
            "StreamTeX uses ",
            (s.bold, "Python and Markdown"),
            " — two of the languages best understood by large language "
            "models. This makes it the ",
            (s.bold, "only document library designed for AI-driven creation"),
            ". You can describe what you want in plain language, and the AI "
            "generates, modifies, and maintains the entire document for you.",
        )
        st_space("v", 0.5)
        st_write(
            bs.body,
            "You keep ",
            (s.bold, "full control"),
            " at all times: every file is readable text, editable by hand "
            "or by AI, with no limits imposed by the software or provider. "
            "No black box, no lock-in.",
        )

    st_space("v", 1)

    # Reasons 2–10
    _reason(
        2, "Zero HTML, zero CSS",
        "All formatting is done through composable Style objects in Python. "
        "You don't need to know web technologies to produce professional results.",
    )
    _reason(
        3, "Pure Python, nothing else",
        "One language for content, logic, and style. No proprietary syntax "
        "to learn, no opaque binary format. Your documents are code — "
        "readable, diffable, reviewable.",
    )
    _reason(
        4, "Total composability",
        "Styles combine with the + operator, blocks nest freely, documents "
        "are structured like code: functions, modules, reuse. Build complex "
        "layouts from simple, testable parts.",
    )
    _reason(
        5, "Complete independence",
        "No account, no subscription, no mandatory server. Your files are "
        "yours — version them in Git, read them in any text editor, "
        "run them on any machine with Python.",
    )
    _reason(
        6, "Universal export",
        "Self-contained HTML (one file, no dependencies), PDF, cloud "
        "deployment. Your document works everywhere, forever.",
    )
    _reason(
        7, "Built-in diagrams",
        "Mermaid, PlantUML, TikZ, and LaTeX — rendered natively, "
        "no external tool to install, no complex configuration.",
    )
    _reason(
        8, "Book navigation",
        "Table of contents, pagination, continuous or page-by-page mode, "
        "navigation markers. Documents that read like real books.",
    )
    _reason(
        9, "The Streamlit ecosystem",
        "Access all Streamlit widgets (interactive charts, data tables, "
        "user inputs) while keeping professional typography and layout.",
    )
    _reason(
        10, "One-command deployment",
        "Pre-configured Docker and Hetzner/Coolify setup. From local "
        "prototype to online document in minutes.",
    )

    st_space("v", 2)
    st_slide_break()

    # ── Who is StreamTeX for? ───────────────────────────────────────
    st_write(bs.sub, "Who is StreamTeX for?", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        _profile(
            "Teachers & trainers",
            "Create courses, tutorials, and training materials. "
            "Frustrated by the limits of PowerPoint and Google Slides "
            "for structured, interactive content.",
            "Interactive, navigable educational documents with "
            "professional layouts — no CSS required.",
        )
        _profile(
            "Professionals & consultants",
            "Produce reports, dashboards, and internal documentation. "
            "Depend on proprietary tools (Notion, Confluence) with "
            "limited export and vendor lock-in.",
            "Self-contained exportable documents (HTML/PDF), "
            "independent of any vendor or subscription.",
        )
        _profile(
            "Developers & engineers",
            "Document projects, APIs, and architectures. "
            "Frustrated by static Markdown and inflexible wikis.",
            "Native Python, composable, Git-versioned, with "
            "syntax highlighting and integrated diagrams.",
        )
        _profile(
            "Researchers & scientists",
            "Write articles, reports, and technical documentation. "
            "Caught between LaTeX (powerful but rigid) and Word "
            "(easy but limited).",
            "LaTeX-quality typesetting + web interactivity + "
            "built-in diagrams (Mermaid, PlantUML, TikZ).",
        )

    st_space("v", 2)

    # ── What StreamTeX lets you do ──────────────────────────────────
    st_write(bs.sub, "What StreamTeX lets you do", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        with st_block(s.project.containers.good_callout):
            st_write(s.project.titles.subsection_title, "Create")
            st_space("v", 0.5)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("Structured documents and manuals")
                with l.item(): st_write("Navigable presentations")
                with l.item(): st_write("Multi-chapter books")
                with l.item(): st_write("Multi-project collections")

        with st_block(s.project.containers.tip_callout):
            st_write(s.project.titles.subsection_title, "Style")
            st_space("v", 0.5)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("Professional layouts (CSS grids, styled lists)")
                with l.item(): st_write("Composable styles in pure Python")
                with l.item(): st_write("150+ named colors, gradients, containers")
                with l.item(): st_write("No HTML or CSS knowledge needed")

        with st_block(s.project.containers.note_callout):
            st_write(s.project.titles.subsection_title, "Publish")
            st_space("v", 0.5)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("Self-contained HTML export (single file)")
                with l.item(): st_write("PDF export via Playwright")
                with l.item(): st_write("Cloud deployment (Docker, Hetzner/Coolify)")
                with l.item(): st_write("Instant sharing, works everywhere")

    st_space("v", 1)

    with st_grid(
        cols="1fr",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        with st_block(s.project.containers.explanation_box):
            st_write(s.project.titles.subsection_title, "Maintain & Improve")
            st_space("v", 0.5)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("Structured production cycle (Compound Engineering)")
                with l.item(): st_write("Import, improve, or create from scratch — 3 guided pathways")
                with l.item(): st_write("Multi-perspective review with 17 AI agents")
                with l.item(): st_write("Continuous improvement through capitalization")

    st_space("v", 2)
    st_slide_break()


# ── Helpers ────────────────────────────────────────────────────────

def _profile(title: str, pain: str, gain: str):
    """User profile card: who they are, their frustration, what they gain."""
    with st_block(bs.profile_card):
        st_write(bs.profile_title, title)
        st_space("v", 0.5)
        st_write(bs.profile_pain, pain)
        st_space("v", 0.5)
        st_write(
            bs.profile_gain,
            (s.bold, "With StreamTeX: "),
            gain,
        )


def _reason(number: int, title: str, body: str):
    """Numbered reason card."""
    st_space("v", 0.5)
    with st_block(s.project.containers.explanation_box):
        st_write(
            bs.body,
            (bs.reason_number, f"#{number} "),
            (bs.reason_title, title),
        )
        st_space("v", 0.3)
        st_write(bs.reason_body, body)
