"""StreamTeX Reuse Architecture Manual — packs, components, design systems, kits."""

from pathlib import Path

import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks


stx.set_static_sources([str(Path(__file__).parent / "static")])

st.set_page_config(
    page_title="StreamTeX - Reuse Architecture",
    layout="wide",
    initial_sidebar_state="expanded",
)
sts.theme = dark

toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,
    toc_position=None,
    title_style=s.project.titles.section_title + s.center_txt,
    content_style=s.large,
    sidebar_max_level=2,
    search=True,
)

marker_config = MarkerConfig(
    auto_marker_on_toc=1,
    next_keys=["PageDown", "ArrowRight"],
    prev_keys=["PageUp", "ArrowLeft"],
    draggable=True,
    collapsible=True,
)


st_book(
    [
        # ── Part 1: Concepts ─────────────────────────────────────
        blocks.bck_reuse_welcome,
        blocks.bck_reuse_vocabulary,
        blocks.bck_reuse_layers,
        blocks.bck_component_format,
        blocks.bck_reference_card,
        # ── Part 2: Pack lifecycle ───────────────────────────────
        blocks.bck_pack_source_resolution,
        blocks.bck_pack_consumption,
        # ── Part 3: Authoring ────────────────────────────────────
        blocks.bck_pack_authoring,
        blocks.bck_component_authoring,
        blocks.bck_kit_format,
        blocks.bck_cli_template_format,
        # ── Part 4: Distribution ─────────────────────────────────
        blocks.bck_pack_distribution,
        # ── Part 5: CE flows ─────────────────────────────────────
        blocks.bck_ce_capture,
        blocks.bck_ce_promote,
        # ── Part 5bis: Pack Engineering (orchestrated lifecycle) ─
        blocks.bck_pack_engineering_overview,
        blocks.bck_pack_engineering_bootstrap,
        blocks.bck_pack_engineering_refine,
        # ── Part 6: Quality & migration ──────────────────────────
        blocks.bck_validation,
        blocks.bck_troubleshooting,
        blocks.bck_migration_from_patterns,
        # ── Part 7: Self-demonstration ───────────────────────────
        # Manual consumes streamtex-design and renders every
        # component for real:
        blocks.bck_gallery_components,
        blocks.bck_gallery_design_systems,
        # ── Part 8: Advanced (custom artefacts) ──────────────────
        blocks.bck_custom_import_mapping,
        # ── Part 9: FAQ ──────────────────────────────────────────
        blocks.bck_faq,
    ],
    toc_config=toc,
    marker_config=marker_config,
    paginate=False,
    banner=BannerConfig.full(),
)
