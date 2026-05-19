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
        # Concepts (5 blocks ported in Wave 2):
        blocks.bck_reuse_welcome,
        blocks.bck_reuse_vocabulary,
        blocks.bck_reuse_layers,
        blocks.bck_component_format,
        blocks.bck_reference_card,
        # Self-demonstration (Wave 4 follow-up) — the manual consumes
        # streamtex-design and renders every component for real:
        blocks.bck_gallery_components,
        blocks.bck_gallery_design_systems,
        # Remaining blocks deferred from PLAN §19.2 (#5-7, #9-14, #17-20):
        #   bck_component_authoring, bck_kit_format, bck_cli_template_format,
        #   bck_pack_authoring, bck_pack_distribution, bck_pack_consumption,
        #   bck_ce_capture, bck_ce_promote, bck_validation,
        #   bck_troubleshooting, bck_migration_from_patterns,
        #   bck_custom_import_mapping, bck_faq.
    ],
    toc_config=toc,
    marker_config=marker_config,
    paginate=False,
    banner=BannerConfig.full(),
)
