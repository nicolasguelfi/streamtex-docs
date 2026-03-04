"""Ecosystem Overview — the four StreamTeX repositories and how they connect."""

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_details


class BlockStyles:
    """Ecosystem block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Repo card
    card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 3px solid #8B5CF6; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ecosystem_card",
    )
    card_icon = s.LARGE + s.center_txt
    card_name = s.project.colors.ai_violet + s.bold + s.Large
    card_desc = s.large

    # Connection flow box
    flow_box = Style(
        "background: rgba(6, 182, 212, 0.08); "
        "border: 1px solid rgba(6, 182, 212, 0.25); "
        "border-radius: 8px; padding: 20px;",
        "ecosystem_flow",
    )
    flow_step = s.project.colors.cyber_cyan + s.bold + s.large
    flow_text = s.large


bs = BlockStyles


def build():
    """Render the ecosystem overview with repo cards and flow."""
    st_space("v", 1)
    st_write(bs.heading, "The StreamTeX AI Ecosystem",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Repository cards ──────────────────────────────────────────
    st_write(bs.sub, "Four repositories, one workflow", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.card):
                st_write(bs.card_name, "streamtex", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.card_desc, """\
                    The core Python library (PyPI). Provides st_write,
                    st_grid, Style composition, book navigation, export,
                    and every rendering function.
                """)
        with g.cell():
            with st_block(bs.card):
                st_write(bs.card_name, "streamtex-docs", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.card_desc, """\
                    Five manuals (intro, advanced, deploy, developer, AI)
                    plus shared blocks and templates. The documentation
                    you are reading right now.
                """)
        with g.cell():
            with st_block(bs.card):
                st_write(bs.card_name, "streamtex-claude", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.card_desc, """\
                    AI profiles, slash commands, and agent definitions.
                    Install a profile into any project to unlock
                    AI-powered generation and audit.
                """)
        with g.cell():
            with st_block(bs.card):
                st_write(bs.card_name, "projects/", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.card_desc, """\
                    Your own StreamTeX projects. Each project has a
                    book.py, blocks/, custom/styles.py, and optional
                    .claude/ configuration.
                """)
    st_space("v", 2)

    # ── How they connect ──────────────────────────────────────────
    st_write(bs.sub, "How they connect", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.flow_box):
        with st_list(list_type="ol") as l:
            with l.item():
                st_write(
                    bs.flow_step,
                    "streamtex-claude ",
                    (bs.flow_text, "installs AI profiles INTO your project"),
                )
            with l.item():
                st_write(
                    bs.flow_step,
                    "Your project ",
                    (bs.flow_text, "imports and uses the "),
                    (s.project.colors.ai_violet + s.bold, "streamtex"),
                    (bs.flow_text, " library for rendering"),
                )
            with l.item():
                st_write(
                    bs.flow_step,
                    "streamtex-docs ",
                    (bs.flow_text, "documents every function, style, and pattern"),
                )
            with l.item():
                st_write(
                    bs.flow_step,
                    "AI agents ",
                    (bs.flow_text, "read the docs and standards to generate correct code"),
                )
    st_space("v", 2)

    show_details("""\
        The streamtex-claude repository is optional. You can use
        StreamTeX without any AI tooling — it is a standalone Python
        library. The AI layer simply accelerates your workflow by
        automating block scaffolding, style composition, and
        structural audits.
    """)
    st_space("v", 1)
