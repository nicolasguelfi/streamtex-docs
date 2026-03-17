import streamlit as st
import streamtex as stx
from streamtex import (
    st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig,
    PresentationConfig, set_presentation_config,
    PdfConfig, ExportConfig, ExportMode,
)
from pathlib import Path

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

# Configure static sources
stx.set_static_sources([str(Path(__file__).parent / "static")])

# Page configuration
st.set_page_config(
    page_title="My Presentation",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject dark theme
sts.theme = dark

# ── Presentation mode (fullscreen 16/9) ──────────────────────────────────
set_presentation_config(PresentationConfig(
    title="My Presentation",
    aspect_ratio="16/9",
    footer=True,
    center_content=False,
    hide_streamlit_header=False,
    enforce_ratio=False,
))

# ── Table of Contents (sidebar only, level 1) ────────────────────────────
toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,
    toc_position=None,
    title_style=s.project.titles.slide_title + s.center_txt,
    content_style=s.large + s.text.colors.reset,
    sidebar_max_level=1,
    search=True,
)

# ── Navigation (PageDown/PageUp + arrow keys) ────────────────────────────
marker_config = MarkerConfig(
    auto_marker_on_toc=1,
    next_keys=["PageDown", "ArrowRight"],
    prev_keys=["PageUp", "ArrowLeft"],
    draggable=True,
    collapsible=True,
)

# ── Orchestrate slides ───────────────────────────────────────────────────
st_book(
    [
        blocks.bck_title,
        blocks.bck_features,
        blocks.bck_grid_demo,
        blocks.bck_lists_demo,
        blocks.bck_conclusion,
    ],
    toc_config=toc,
    marker_config=marker_config,
    paginate=True,
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=80,
    # Auto-export to disk (disabled by default — change NEVER to ALWAYS to enable)
    exports=[
        ExportConfig(
            format="html",
            mode=ExportMode.NEVER,
            output_dir="./exports",
            filename="my-presentation",
            timestamp=True,
        ),
        ExportConfig(
            format="pdf",
            mode=ExportMode.NEVER,
            output_dir="./exports",
            filename="my-presentation",
            timestamp=True,
            pdf=PdfConfig(
                format="A4", landscape=True,
                margin_top="0", margin_bottom="0",
                margin_left="0", margin_right="0",
            ),
        ),
    ],
)
