"""Title page — StreamTeX AI Manual hero banner with badges."""

from pathlib import Path

import streamlit as st
from streamtex import st_write, st_space, st_block, st_grid, st_image
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation

_LOGO = str(Path(__file__).parent.parent.parent / "shared-blocks" / "logo-stx.png")

class BlockStyles:
    """Title page styles."""
    heading = s.project.titles.page_title + s.center_txt
    tagline = s.project.colors.cyber_cyan + s.Large + s.center_txt
    intro = s.large + s.center_txt

    # Hero banner
    banner = Style(
        "background: linear-gradient(135deg, rgba(139, 92, 246, 0.10) 0%, "
        "rgba(6, 182, 212, 0.10) 100%); "
        "border-radius: 8px; padding: 32px 20px;",
        "ai_hero_banner",
    )

    # Badge container
    badge = Style(
        "background: rgba(139, 92, 246, 0.08); "
        "border: 1px solid rgba(139, 92, 246, 0.25); "
        "border-radius: 6px; padding: 14px 10px; text-align: center;",
        "ai_badge",
    )
    badge_number = s.project.colors.ai_violet + s.bold + s.LARGE
    badge_label = s.large + s.center_txt
    logo = Style("width: 100%; height: auto;", "ai_logo")
    logo_cell = Style("display: flex; align-items: center; justify-content: center;", "ai_logo_cell")

bs = BlockStyles

def build():
    """Render the AI Manual title page."""
    st_space("v", 1)

    # ── Hero banner ───────────────────────────────────────────────
    with st_block(bs.banner):
        with st_grid(cols="25% 75%", cell_styles=[bs.logo_cell, None]) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button("❤️ Support us!", "https://github.com/sponsors/nicolasguelfi", use_container_width=True)
            with g.cell():
                st_write(bs.heading, "StreamTeX AI Manual",
                         tag=t.div, toc_lvl="1")
        st_space("v", 1)
        st_write(bs.tagline, "AI-Powered Documentation Workflows",
                 tag=t.div)
    st_space("v", 2)

    # ── Badges row ────────────────────────────────────────────────
    with st_grid(cols=4, cell_styles=bs.badge) as g:
        with g.cell():
            st_write(bs.badge_number, "25", tag=t.div)
            st_write(bs.badge_label, "Commands", tag=t.div)
        with g.cell():
            st_write(bs.badge_number, "3", tag=t.div)
            st_write(bs.badge_label, "Agents", tag=t.div)
        with g.cell():
            st_write(bs.badge_number, "7", tag=t.div)
            st_write(bs.badge_label, "Blueprints", tag=t.div)
        with g.cell():
            st_write(bs.badge_number, "4", tag=t.div)
            st_write(bs.badge_label, "Profiles", tag=t.div)
    st_space("v", 2)

    # ── Introduction paragraph ────────────────────────────────────
    show_explanation("""\
        StreamTeX AI combines the power of large language models with
        structured coding standards. Instead of writing every block by
        hand, you describe what you want and an AI agent generates
        production-ready StreamTeX code — styled, documented, and
        ready to deploy. This manual covers every command, agent,
        blueprint, and workflow you need to go from idea to published
        document in minutes.
    """)
    st_space("v", 1)
