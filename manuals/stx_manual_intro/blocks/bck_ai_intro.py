"""StreamTeX + AI — Introduction to AI-assisted document creation.

Bridges to the full AI manual by showing what is possible
with natural language, without requiring any code.
"""

from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, st_slide_break


class BlockStyles:
    """AI intro styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    ai_banner = Style(
        "background: linear-gradient(135deg, rgba(142,68,223,0.10) 0%, "
        "rgba(79,172,254,0.10) 100%); "
        "border-radius: 8px; padding: 24px;",
        "ai_intro_banner"
    )
    ai_accent = Style("color: #8E44DF;", "ai_intro_accent")
    prompt_box = Style(
        "background: rgba(142, 68, 223, 0.06); "
        "border-left: 3px solid #8E44DF; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ai_intro_prompt"
    )
    result_box = Style(
        "background: rgba(39, 174, 96, 0.06); "
        "border-left: 3px solid #27AE60; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ai_intro_result"
    )
    prompt_label = Style(
        "color: #8E44DF; font-weight: bold;", "ai_intro_prompt_label"
    ) + s.large
    result_label = s.project.colors.success_green + s.bold + s.large
    path_card = Style(
        "background: rgba(79, 172, 254, 0.06); "
        "border-left: 3px solid #4facfe; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ai_intro_path_card"
    )
    path_title = s.project.colors.primary_blue + s.bold + s.Large
    path_subtitle = s.project.colors.neutral_gray + s.medium
    task_icon = s.large + s.bold
    manual_link = Style(
        "background: linear-gradient(135deg, rgba(142,68,223,0.08) 0%, "
        "rgba(79,172,254,0.08) 100%); "
        "border: 1px solid rgba(142,68,223,0.3); "
        "border-radius: 8px; padding: 20px;",
        "ai_intro_manual_link"
    )


bs = BlockStyles


def build():
    """Render the AI introduction section."""
    st_space("v", 1)
    st_write(bs.heading, "StreamTeX + AI: Create Without Coding",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── The insight ─────────────────────────────────────────────────
    with st_block(bs.ai_banner):
        st_write(
            s.Large + s.bold + s.center_txt,
            "AI understands StreamTeX natively",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large + s.center_txt + s.project.colors.neutral_gray,
            "Large language models like Claude excel at Python and "
            "Markdown — the two languages StreamTeX is built on. "
            "This means an AI assistant can ",
            (s.bold, "create, modify, and maintain"),
            " your documents as well as a human developer, "
            "from a simple description in plain language.",
            tag=t.div,
        )
    st_space("v", 2)

    # ── Two paths ───────────────────────────────────────────────────
    st_write(bs.sub, "Two paths, one tool", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "StreamTeX supports two complementary approaches. "
        "Both produce ",
        (s.bold, "exactly the same result"),
        " — the difference is how you get there.",
    )
    st_space("v", 1)

    with st_grid(
        cols="repeat(auto-fit, minmax(300px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        with st_block(bs.path_card):
            st_write(bs.path_title, "Zero-code path")
            st_write(bs.path_subtitle, "For everyone")
            st_space("v", 1)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("You describe what you want in ", (s.bold, "natural language"))
                with l.item(): st_write("The AI generates the entire project")
                with l.item(): st_write("You review and adjust the result visually")
                with l.item(): st_write("No Python knowledge required")

        with st_block(bs.path_card):
            st_write(bs.path_title, "Code-first path")
            st_write(bs.path_subtitle, "For developers")
            st_space("v", 1)
            with st_list(list_type="ul", li_style=bs.body) as l:
                with l.item(): st_write("You write the code ", (s.bold, "yourself"))
                with l.item(): st_write("The AI assists, audits, and fixes")
                with l.item(): st_write("Full control over every detail")
                with l.item(): st_write("Basic Python knowledge recommended")

    st_space("v", 2)
    st_slide_break(marker_label="What AI Can Do")

    # ── What AI can do ──────────────────────────────────────────────
    st_write(bs.sub, "What AI can do with StreamTeX", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.body,
        "Here are concrete examples of what you can ask "
        "an AI assistant to do — in plain language:",
    )
    st_space("v", 1)

    _ai_task(
        "Create a complete document",
        "Create a training course on photosynthesis with 5 chapters, "
        "a table of contents, and a blue/green color scheme",
        "The AI generates the full project: book.py, blocks, styles, "
        "ready to run with stx run.",
    )
    _ai_task(
        "Modify the style",
        "Make all titles blue, increase the body text size, "
        "and add a gradient background to the header",
        "The AI updates the Style objects in custom/styles.py "
        "and every block inherits the change automatically.",
    )
    _ai_task(
        "Restructure the content",
        "Move chapter 3 before chapter 2, add a summary at the "
        "beginning, and split chapter 5 into two parts",
        "The AI reorders blocks in book.py, creates new block "
        "files, and preserves all existing content.",
    )
    _ai_task(
        "Add diagrams",
        "Add a diagram showing the water cycle using Mermaid, "
        "and a flowchart of the scientific method",
        "The AI generates st_mermaid() calls with the diagram "
        "code, positioned inside the appropriate blocks.",
    )
    _ai_task(
        "Export and deploy",
        "Generate a PDF of this document and deploy it online",
        "The AI configures PdfConfig, runs the export, and "
        "sets up Docker/Render deployment.",
    )
    _ai_task(
        "Audit and fix",
        "Check if all styles are consistent and fix any "
        "layout problems",
        "The AI runs /stx-designer:audit, identifies issues, "
        "and applies fixes with /stx-designer:fix.",
    )

    st_space("v", 2)

    # ── Why this matters ────────────────────────────────────────────
    st_write(bs.sub, "Why this changes everything", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Traditional document tools (Word, PowerPoint, Notion) store
        content in binary or proprietary formats that AI cannot
        reliably read or modify. LaTeX is text-based but too complex
        for AI to generate consistently.

        StreamTeX is different: every document is a collection of
        **short Python files** using a **small, well-defined API**.
        AI models have seen millions of Python examples during
        training — they understand StreamTeX code as naturally as
        they understand English.

        The result: **you can create and maintain complex documents
        entirely through conversation**, while retaining the ability
        to edit any file by hand at any time. No vendor lock-in,
        no feature ceiling, no hidden limitations.
    """)
    st_space("v", 2)

    # ── Go further ──────────────────────────────────────────────────
    st_write(bs.sub, "Go further: the AI Manual", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.manual_link):
        st_write(
            s.Large + s.bold + bs.ai_accent,
            "The AI Manual",
            tag=t.div,
        )
        st_space("v", 0.5)
        st_write(
            bs.body,
            "The dedicated AI manual covers everything you need "
            "to work with StreamTeX through AI:",
        )
        st_space("v", 0.5)
        with st_list(list_type="ul", li_style=bs.body) as l:
            with l.item(): st_write((s.bold, "Setup"), " — install AI profiles and configure your workspace")
            with l.item(): st_write((s.bold, "Commands"), " — /stx-designer:init, update, audit, fix")
            with l.item(): st_write((s.bold, "Agents"), " — architect, designer, and presentation specialists")
            with l.item(): st_write((s.bold, "Best practices"), " — prompting techniques and team workflows")
            with l.item(): st_write((s.bold, "AI images"), " — generate illustrations with OpenAI, Google, or fal.ai")
        st_space("v", 1)
        st_write(
            bs.body + s.project.colors.neutral_gray,
            "Available in the StreamTeX documentation collection "
            "at streamtex.onrender.com.",
        )

    st_space("v", 2)
    st_slide_break(marker_label="The AI Manual")


# ── Helpers ────────────────────────────────────────────────────────

def _ai_task(title: str, prompt: str, result: str):
    """AI task example: what you say → what happens."""
    st_space("v", 0.5)
    with st_grid(
        cols="repeat(auto-fit, minmax(280px, 1fr))",
        grid_style=stx.StxStyles.container.grid.gap_24,
    ):
        with st_block(bs.prompt_box):
            st_write(bs.prompt_label, title)
            st_space("v", 0.3)
            st_write(
                s.medium + Style("font-style: italic;", "ai_prompt_italic"),
                f'"{prompt}"',
            )
        with st_block(bs.result_box):
            st_write(bs.result_label, "What happens")
            st_space("v", 0.3)
            st_write(s.medium, result)
