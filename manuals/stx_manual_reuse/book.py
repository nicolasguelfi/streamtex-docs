"""StreamTeX Reuse Architecture Manual — packs, components, design systems, kits."""

import importlib.util
import tomllib

import streamlit as st
import streamtex as stx
from streamtex import (
    st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig, PdfConfig,
    ExportConfig, ExportMode, PresentationProfile, ViewMode,
)
from pathlib import Path

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

_doc_version = tomllib.loads(
    (Path(__file__).parent.parent.parent / "pyproject.toml").read_text()
).get("project", {}).get("version", "?")

_spec = importlib.util.spec_from_file_location(
    "bck_changelog",
    str(Path(__file__).parent.parent / "shared-blocks" / "blocks" / "bck_changelog.py"),
)
_bck_changelog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bck_changelog)

stx.set_static_sources([str(Path(__file__).parent / "static")])

_logo = str(Path(__file__).parent.parent / "shared-blocks" / "logo-stx.png")
st.set_page_config(
    page_title="StreamTeX - Reuse Architecture",
    page_icon=_logo,
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


st_book([
    # Welcome page (gradient header + level badge — matches intro pattern)
    blocks.bck_reuse_level_badge,

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

    # ── Part 6: Quality ──────────────────────────────────────
    blocks.bck_validation,
    blocks.bck_troubleshooting,

    # ── Part 7: Self-demonstration ───────────────────────────
    # Manual consumes streamtex-design and renders every
    # component for real:
    blocks.bck_gallery_components,
    blocks.bck_gallery_design_systems,

    # ── Part 8: Advanced (custom artefacts) ──────────────────
    blocks.bck_custom_import_mapping,

    # ── Part 9: FAQ ──────────────────────────────────────────
    blocks.bck_faq,

    # Changelog (shared block)
    _bck_changelog,
    ], toc_config=toc, marker_config=marker_config, paginate=True,
    banner=BannerConfig.full(),
    inspector=stx.InspectorConfig(enabled=True),
    pdf_config=PdfConfig(
        margin_top="0", margin_bottom="0",
        margin_left="0", margin_right="0",
    ),
    exports=[
        ExportConfig(
            format="html",
            mode=ExportMode.MANUAL,
            output_dir="./exports",
            filename="streamtex-reuse",
            timestamp=True,
        ),
        ExportConfig(
            format="pdf",
            mode=ExportMode.MANUAL,
            output_dir="./exports",
            filename="streamtex-reuse",
            timestamp=True,
            pdf=PdfConfig(
                format="A4", landscape=True,
                margin_top="0", margin_bottom="0",
                margin_left="0", margin_right="0",
            ),
        ),
    ],
    page_width=80,
    view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS],
    doc_version=_doc_version,
    presentation_profiles=PresentationProfile.desktop_mobile_preset())
