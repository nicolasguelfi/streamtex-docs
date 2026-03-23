"""StreamTeX CE Manual - Compound Document Engineering."""

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
    page_title="StreamTeX - Compound Engineering",
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
    show_nav_ui=True,
)

st_book([
    # Welcome page (gradient header + level badge)
    blocks.bck_ce_welcome,

    # Part 1: Introduction
    blocks.bck_ce_overview,
    blocks.bck_ce_philosophy,
    blocks.bck_ce_parcours,
    blocks.bck_ce_quickstart,

    # Part 2: The Cycle (7 phases)
    blocks.bck_ce_collect,
    blocks.bck_ce_assess,
    blocks.bck_ce_plan,
    blocks.bck_ce_plan_interactive,
    blocks.bck_ce_produce,
    blocks.bck_ce_review,
    blocks.bck_ce_fix,
    blocks.bck_ce_compound,
    blocks.bck_ce_go,

    # Part 3: Agents
    blocks.bck_ce_agents_overview,
    blocks.bck_ce_agents_collect,
    blocks.bck_ce_agents_assess,
    blocks.bck_ce_agents_plan,
    blocks.bck_ce_agents_produce,
    blocks.bck_ce_agents_review,

    # Part 4: Practical Guides
    blocks.bck_ce_guide_import,
    blocks.bck_ce_guide_improve,
    blocks.bck_ce_guide_create,
    blocks.bck_ce_guide_compound,

    # Part 5: Reference
    blocks.bck_ce_commands_ref,
    blocks.bck_ce_templates_ref,
    blocks.bck_ce_config_ref,
    blocks.bck_ce_faq,

    # Changelog (shared block)
    _bck_changelog,
    ], toc_config=toc, marker_config=marker_config, paginate=True,
    banner=BannerConfig.full(),
    inspector=stx.InspectorConfig(enabled=True),
    pdf_config=PdfConfig(
        format="A4",
        landscape=True,
    ),
    exports=[
        ExportConfig(
            format="html",
            mode=ExportMode.NEVER,
            output_dir="./exports",
            filename="stx-manual-ce",
            timestamp=True,
        ),
    ],
    page_width=60,
    view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS],
    doc_version=_doc_version,
    presentation_profiles=PresentationProfile.desktop_mobile_preset(),
)
