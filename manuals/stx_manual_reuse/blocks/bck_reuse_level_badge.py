"""Welcome page — Reuse Architecture header + level badge.

Renders a project-specific gradient header and level badge for the Reuse
Architecture manual. Modeled on the intro manual's bck_level_badge: same
structure (gradient header with logo + Support button + title, then a level
box with headline + description + bullet list).

The identity colour for Reuse is green (matching the 🧩 emoji used in the
collection hub) to differentiate it from intro (blue), advanced, ai, etc.
"""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s

_LOGO = "https://media.githubusercontent.com/media/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png"


class BlockStyles:
    """Level badge styles — green identity for Reuse Architecture."""
    # Green gradient header (Reuse identity — matches the 🧩 emoji)
    header = Style(
        "background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "reuse_header"
    )
    level_box = Style(
        "background: rgba(46, 204, 113, 0.08); "
        "border-left: 4px solid #2ecc71; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "reuse_level_box"
    )
    level_label = Style(
        "color: #2ecc71; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "reuse_level_label"
    )
    logo = Style("width: 100%; height: auto;", "reuse_logo")
    logo_cell = Style(
        "display: flex; flex-direction: column; align-items: center; "
        "justify-content: center; gap: 4px;",
        "reuse_logo_cell"
    )
    description = s.large + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Render Reuse Architecture header + level badge on the same page."""
    # --- Reuse gradient header ---
    st_space("v", 1)
    with st_block(bs.header):
        with st_grid(cols="25% 1fr", breakpoint="600px",
                     cell_styles=[bs.logo_cell, None]) as g:
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
                    "StreamTeX Reuse Architecture",
                    tag=t.div,
                    toc_lvl="1",
                )
                st_write(
                    stx.StxStyles.large + "color:white;",
                    "Packs, components, design systems, kits — and Pack Engineering",
                    tag=t.div,
                )
    st_space("v", 1)

    # --- Reuse level badge ---
    with st_block(bs.level_box):
        st_write(bs.level_label, "Reuse Level")
        st_space("v", 0.5)
        st_write(
            s.Large + s.text.weights.bold_weight,
            "The streamtex reuse layer, end-to-end",
        )
        st_space("v", 1)
        st_write(
            bs.description,
            "This manual covers the ",
            (s.bold, "reuse architecture"),
            " of streamtex: how reusable artefacts (",
            (s.bold, "components, design systems, kits"),
            ") ship inside Python ",
            (s.bold, "packs"),
            ", how projects consume them, and how ",
            (s.bold, "Pack Engineering"),
            " orchestrates their full lifecycle across N projects.",
        )
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.medium,
                    "Concepts: packs, components, design systems, kits",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Authoring: scaffold components, design systems, kits, "
                    "and CLI templates",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Pack Engineering (/stx-pe): bootstrap, specialize, refine, "
                    "audit, adopt, publish",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Self-demonstration: this manual consumes streamtex-design "
                    "and renders every component for real",
                )

    st_space("v", 2)
