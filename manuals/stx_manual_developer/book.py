"""StreamTeX Developer Guide - Library Contributors Manual."""

import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

# Page configuration
st.set_page_config(
    page_title="StreamTeX - Developer Guide",
    layout="wide",
    initial_sidebar_state="expanded"
)
sts.theme = dark

# Table of Contents configuration
toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,
    toc_position=0,
    title_style=s.project.titles.section_title + s.center_txt,
    content_style=s.large,
    sidebar_max_level=2,
    search=True,
)

# Marker configuration for navigation
marker_config = MarkerConfig(
    auto_marker_on_toc=1,
    next_keys=["PageDown"],
    prev_keys=["PageUp"],
)

# Orchestrate composites in developer guide order
st_book([
    # Welcome and prerequisites
    blocks.bck_dev_welcome,

    # Repository structure
    blocks.bck_dev_repo_structure,

    # Development setup
    blocks.bck_dev_setup,

    # Architecture deep-dive
    blocks.bck_dev_architecture,

    # Coding standards
    blocks.bck_dev_coding_standards,

    # Testing
    blocks.bck_dev_testing,

    # CI/CD pipelines
    blocks.bck_dev_ci_cd,

    # Release process
    blocks.bck_dev_release,

    # CLI architecture
    blocks.bck_dev_cli,

    # Maintenance
    blocks.bck_dev_maintenance,

    # Claude profiles
    blocks.bck_dev_claude_profiles,
], toc_config=toc, marker_config=marker_config, paginate=True,
   banner=BannerConfig.full(),
   inspector=stx.InspectorConfig(enabled=True))
