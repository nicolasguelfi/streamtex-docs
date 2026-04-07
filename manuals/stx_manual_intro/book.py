"""StreamTeX Introduction Course - Test Project (Intro Level)."""

import importlib.util
import tomllib

import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig, PdfConfig, ExportConfig, ExportMode, PresentationProfile, ViewMode
from pathlib import Path

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

_doc_version = tomllib.loads((Path(__file__).parent.parent.parent / "pyproject.toml").read_text()).get("project", {}).get("version", "?")
_spec = importlib.util.spec_from_file_location("bck_changelog",
    str(Path(__file__).parent.parent / "shared-blocks" / "blocks" / "bck_changelog.py"))
_bck_changelog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bck_changelog)

# Configure static sources
stx.set_static_sources([str(Path(__file__).parent / "static")])

# Page configuration
_logo = str(Path(__file__).parent.parent / "shared-blocks" / "logo-stx.png")
st.set_page_config(
    page_title="StreamTeX - Introduction",
    page_icon=_logo,
    layout="wide",
    initial_sidebar_state="expanded"
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

# Orchestrate composites in pedagogical order
st_book([
    # Welcome page (gradient header + level badge)
    blocks.bck_level_badge,

    # Video introduction
    blocks.bck_video_intro,

    # Why StreamTeX, audience, and AI introduction
    blocks.bck_why_streamtex,
    blocks.bck_who_should_read,
    blocks.bck_ai_intro,

    # Compound Engineering introduction
    blocks.bck_ce_intro,

    # Library overview (what it is, live showcase)
    blocks.bck_what_is_streamtex,

    # Quick Start (local intro blocks)
    blocks.bck_qs_installation,
    blocks.bck_qs_new_project,
    blocks.bck_qs_first_block,

    blocks.bck_architecture_guide,

    # Text & styling
    blocks.bck_text_and_styling,
    blocks.bck_tags_enum,
    blocks.bck_style_composition,

    # Layout & content
    blocks.bck_containers_and_layout,
    blocks.bck_grids_and_lists,
    blocks.bck_list_styles,

    # Media & advanced
    blocks.bck_media_rendering,
    blocks.bck_navigation_and_organization,
    blocks.bck_zoom_and_responsive,
    blocks.bck_spacing,
    blocks.bck_export_and_sharing,

    # CLI Quick Start
    blocks.bck_cli_quickstart,

    # Feedback & Support
    blocks.bck_feedback,

    # Changelog (shared block)
    _bck_changelog,
    ], toc_config=toc, marker_config=marker_config, paginate=True,
    banner=BannerConfig.full(),
    inspector=stx.InspectorConfig(enabled=True),
    pdf_config=PdfConfig(
        margin_top="0", margin_bottom="0",
        margin_left="0", margin_right="0",
    ),
    # Auto-export to disk (disabled by default — change NEVER to ALWAYS to enable)
    exports=[
        ExportConfig(
            format="html",
            mode=ExportMode.MANUAL,
            output_dir="./exports",
            filename="streamtex-intro",
            timestamp=True,
        ),
        ExportConfig(
            format="pdf",
            mode=ExportMode.MANUAL,
            output_dir="./exports",
            filename="streamtex-intro",
            timestamp=True,
            pdf=PdfConfig(
                format="A4", landscape=True,
                margin_top="0", margin_bottom="0",
                margin_left="0", margin_right="0",
            ),
        ),
    ],
    page_width=80,
    zoom=80,
    view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS],
    doc_version=_doc_version,
    presentation_profiles=PresentationProfile.desktop_mobile_preset())
