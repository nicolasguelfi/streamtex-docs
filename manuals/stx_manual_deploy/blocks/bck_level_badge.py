"""Welcome page — Deployment header + level badge.

Renders a project-specific gradient header and level badge.
Both appear on the same page in paginated mode because they
are in a single module.
"""

from pathlib import Path

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s

_LOGO = str(Path(__file__).parent.parent.parent / "shared-blocks" / "logo-stx.png")


class BlockStyles:
    """Level badge styles."""
    # Green-teal gradient header (Deploy identity)
    header = Style(
        "background: linear-gradient(135deg, #0ba360 0%, #3cba92 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "deploy_header"
    )
    level_box = Style(
        "background: rgba(11, 163, 96, 0.08); "
        "border-left: 4px solid #0ba360; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "deploy_level_box"
    )
    level_label = Style(
        "color: #0ba360; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "deploy_level_label"
    )
    logo = Style("width: 100%; height: auto;", "deploy_logo")
    logo_cell = Style("display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;", "deploy_logo_cell")
    description = s.large + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Render Deployment header + level badge on the same page."""
    # --- Deployment gradient header ---
    st_space("v", 1)
    with st_block(bs.header):
        with st_grid(cols="25% 75%", cell_styles=[bs.logo_cell, None]) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button("❤️ Support us!", "https://github.com/sponsors/nicolasguelfi", use_container_width=True)
            with g.cell():
                st_write(
                    stx.StxStyles.LARGE + stx.StxStyles.bold + "color:white;",
                    "StreamTeX Training Course: Deploy",
                    tag=t.div,
                    toc_lvl="1",
                )
                st_write(
                    stx.StxStyles.large + "color:white;",
                    "A Streamlit-based content rendering framework",
                    tag=t.div
                )
    st_space("v", 1)

    # --- Deployment level badge ---
    with st_block(bs.level_box):
        st_write(bs.level_label, "Deployment Guide")
        st_space("v", 0.5)
        st_write(
            s.Large + s.text.weights.bold_weight,
            "Deploy StreamTeX Projects to Any Platform",
        )
        st_space("v", 1)
        st_write(
            bs.description,
            "This manual covers every deployment option for StreamTeX projects: "
            "from local Docker testing to production cloud hosting. "
            "Each section includes step-by-step instructions and automation scripts.",
        )
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, "Local: Docker build and compose for testing")
            with l.item(): st_write(s.medium, "Cloud: Streamlit Cloud, HuggingFace Spaces, Render.com")
            with l.item(): st_write(s.medium, "Production: GCP VM + Ansible, CI/CD pipelines")

    st_space("v", 2)
