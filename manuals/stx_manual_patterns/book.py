"""StreamTeX Patterns Manual — pattern catalog mechanism documentation."""

from pathlib import Path

import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks


# Configure static sources
stx.set_static_sources([str(Path(__file__).parent / "static")])

# Page configuration
st.set_page_config(
    page_title="StreamTeX - Patterns",
    layout="wide",
    initial_sidebar_state="expanded",
)
sts.theme = dark

# Table of Contents configuration
toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,
    toc_position=None,
    title_style=s.project.titles.section_title + s.center_txt,
    content_style=s.large,
    sidebar_max_level=2,
    search=True,
)

# Marker configuration for navigation
marker_config = MarkerConfig(
    auto_marker_on_toc=1,
    next_keys=["PageDown", "ArrowRight"],
    prev_keys=["PageUp", "ArrowLeft"],
    draggable=True,
    collapsible=True,
)


st_book(
    [
        blocks.bck_intro,
        blocks.bck_format_spec,
        blocks.bck_scan_rule,
        blocks.bck_extrapolation,
        blocks.bck_cli_overview,
        blocks.bck_authoring,
        # Compact galleries — one block per pattern family
        blocks.bck_gallery_atoms,
        blocks.bck_gallery_callouts,
        blocks.bck_gallery_lists,
        blocks.bck_gallery_docs,
        # Dedicated demos — one block per rich template
        blocks.bck_demo_slide_heading,
        blocks.bck_demo_stat_hero,
        blocks.bck_demo_title_slide,
        blocks.bck_demo_evidence_insight,
        blocks.bck_demo_exercise_flow,
        blocks.bck_demo_categorized_grid,
        blocks.bck_demo_narrative_transition,
        # Closing
        blocks.bck_blueprints_vs_patterns,
    ],
    toc_config=toc,
    marker_config=marker_config,
    paginate=False,
    banner=BannerConfig.full(),
)
