"""Welcome page — Gradient header + level badge for CE manual.

Renders a project-specific gradient header and level badge.
Both appear on the same page in paginated mode because they
are in a single module.
"""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s

_LOGO = "https://media.githubusercontent.com/media/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png"


class BlockStyles:
    """CE Welcome styles."""
    # Amber-orange gradient header (CE methodology identity)
    header = Style(
        "background: linear-gradient(135deg, #F39C12 0%, #E74C3C 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "ce_header"
    )
    level_box = Style(
        "background: rgba(243, 156, 18, 0.08); "
        "border-left: 4px solid #F39C12; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "ce_level_box"
    )
    level_label = Style(
        "color: #F39C12; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "ce_level_label"
    )
    logo = Style("width: 100%; height: auto;", "ce_logo")
    logo_cell = Style(
        "display: flex; flex-direction: column; align-items: center; "
        "justify-content: center; gap: 4px;",
        "ce_logo_cell"
    )
    description = s.large + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Render CE gradient header + level badge on the same page."""
    # --- CE gradient header ---
    st_space("v", 1)
    with st_block(bs.header):
        with st_grid(
            cols="25% 1fr", breakpoint="600px",
            cell_styles=[bs.logo_cell, None]
        ) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button(
                    "❤️ Support us!",
                    "https://github.com/sponsors/nicolasguelfi",
                    use_container_width=True,
                )
            with g.cell():
                st_write(
                    stx.StxStyles.LARGE + stx.StxStyles.bold + "color:white;",
                    "StreamTeX Manual: Compound Document Engineering",
                    tag=t.div,
                    toc_lvl="1",
                )
                st_write(
                    stx.StxStyles.large + "color:white;",
                    "A structured methodology for document production",
                    tag=t.div,
                )
    st_space("v", 1)

    # --- CE level badge ---
    with st_block(bs.level_box):
        st_write(bs.level_label, "Methodology Guide")
        st_space("v", 0.5)
        st_write(
            s.Large + s.text.weights.bold_weight,
            "The 9-Phase Iterative/Incremental Cycle for Document Engineering",
        )
        st_space("v", 1)
        st_write(
            bs.description,
            "This manual covers the ",
            (s.bold, "Compound Document Engineering"),
            " methodology — a ",
            (s.bold, "repeatable cycle"),
            " to produce, review, and improve documents with ",
            (s.bold, "AI assistance"),
            ".",
        )
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.medium,
                    (s.project.colors.accent_teal, "COLLECT"),
                    " → ",
                    (s.project.colors.accent_teal, "ASSESS"),
                    " → ",
                    (s.project.colors.accent_teal, "PLAN"),
                    " → ",
                    (s.project.colors.accent_teal, "PROTOTYPE"),
                    " → ",
                    (s.project.colors.accent_teal, "PRODUCE"),
                    " → ",
                    (s.project.colors.accent_teal, "REVIEW"),
                    " → ",
                    (s.project.colors.accent_teal, "FIX"),
                    " → ",
                    (s.project.colors.accent_teal, "COMPOUND"),
                    " → ",
                    (s.project.colors.accent_teal, "INTEGRATE"),
                )
            with l.item():
                st_write(
                    s.medium,
                    "Three pathways: ",
                    (s.project.colors.highlight_amber, "Import"),
                    ", ",
                    (s.project.colors.highlight_amber, "Improve"),
                    ", ",
                    (s.project.colors.highlight_amber, "Create"),
                )
            with l.item():
                st_write(s.medium, "Practical guides, agent details, and command reference")

    st_space("v", 2)
