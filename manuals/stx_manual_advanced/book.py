"""StreamTeX Advanced Course - Test Project (Advanced Level + Phase 1/2 Features)."""

import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig, PdfConfig
from streamtex.bib import BibConfig, BibFormat, CitationStyle

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

# ============================================================================
# PHASE 1 & 2 DEMO: Multi-source blocks and static resolution
# ============================================================================

# Configure shared blocks (Phase 1: LazyBlockRegistry)
from pathlib import Path
_shared_blocks_path = str(Path(__file__).parent.parent / "shared-blocks" / "blocks")
_static_shared_path = str(Path(__file__).parent.parent / "shared-blocks" / "static")

shared_blocks = stx.LazyBlockRegistry([_shared_blocks_path])

# Configure static sources for multi-directory resolution
stx.set_static_sources([
    str(Path(__file__).parent / "static"),
    _static_shared_path,
])

# ============================================================================
# Page configuration
# ============================================================================
_logo = str(Path(__file__).parent.parent / "shared-blocks" / "logo-stx.png")
st.set_page_config(
    page_title="StreamTeX - Advanced",
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
    search=True,
    sidebar_max_level=2,
)

# Marker configuration for navigation
marker_config = MarkerConfig(
    auto_marker_on_toc=1,
    next_keys=["PageDown"],
    prev_keys=["PageUp"],
)

# ============================================================================
# Bibliography configuration
# ============================================================================
bib_sources = [
    str(Path(__file__).parent / "static" / "various" / "references.bib"),
]

bib_config = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    hover_enabled=True,
    hover_show_abstract=True,
)

# ============================================================================
# Orchestrate composites — reorganized into logical sections
# ============================================================================
st_book([
    # Welcome page (gradient header + level badge)
    blocks.bck_level_badge,

    # --- Section 1: Architecture & Patterns ---
    blocks.bck_lazy_block_registry_demo,
    blocks.bck_shared_blocks_usage,
    blocks.bck_static_resolution_demo,
    blocks.bck_block_helpers_patterns,
    blocks.bck_atomic_blocks_pattern,

    # --- Section 2: UI Avancee ---
    blocks.bck_overlays_positioning,
    blocks.bck_visibility_control,
    blocks.bck_custom_themes,
    blocks.bck_hover_and_preview,
    blocks.bck_ui_components,

    # --- Section 3: Navigation & Book ---
    blocks.bck_navigation_markers,
    blocks.bck_banner_config,
    blocks.bck_inspector_config,
    blocks.bck_collections_and_discovery,

    # --- Section 4: Langages documentaires ---
    blocks.bck_document_languages,
    blocks.bck_latex_documents,
    blocks.bck_diagrams_and_viz,

    # --- Section 5: Donnees & Integrations ---
    blocks.bck_data_and_charts,
    blocks.bck_gsheet_import,
    blocks.bck_bibliography_references,
    blocks.bck_interactive_and_state,

    # --- Section 6: Export ---
    blocks.bck_export_aware_widgets,
    blocks.bck_export_advanced,
    blocks.bck_static_assets_loading,
    blocks.bck_deployment_strategies,

    # --- Appendix: Migration ---
    blocks.bck_upgrade_guide,

    # Shared block footer
    shared_blocks.bck_footer_training,
], toc_config=toc, marker_config=marker_config, paginate=True,
   banner=BannerConfig.full(),
   bib_sources=bib_sources, bib_config=bib_config,
   inspector=stx.InspectorConfig(enabled=True),
   pdf_config=PdfConfig(
       margin_top="0", margin_bottom="0",
       margin_left="0", margin_right="0",
   ))
