"""StreamTeX AI Manual — AI-Powered Workflows with Claude Code & Cursor."""

import streamlit as st
import setup  # noqa: F401
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig, PdfConfig, ExportConfig, ExportMode
from pathlib import Path

from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
import blocks

# Configure static sources
stx.set_static_sources([str(Path(__file__).parent / "static")])

# Page configuration
_logo = str(Path(__file__).parent.parent / "shared-blocks" / "logo-stx.png")
st.set_page_config(
    page_title="StreamTeX - AI Manual",
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

# Orchestrate blocks in pedagogical order
st_book([
    # ── Part 1: Discover ──────────────────────────────────────
    blocks.bck_title,
    blocks.bck_why_ai,
    blocks.bck_ecosystem,
    blocks.bck_two_paths,

    # ── Part 2: Setup ─────────────────────────────────────────
    blocks.bck_prerequisites,
    blocks.bck_workspace,
    blocks.bck_profile_install,
    blocks.bck_claude_md,
    blocks.bck_settings,

    # ── Part 3: Commands ──────────────────────────────────────
    blocks.bck_commands_overview,
    blocks.bck_cmd_project_init,
    blocks.bck_cmd_project_customize,
    blocks.bck_cmd_designer_slides,
    blocks.bck_cmd_designer_styles,
    blocks.bck_cmd_project_other,

    # ── Part 4: Agents ────────────────────────────────────────
    blocks.bck_agents_overview,
    blocks.bck_agent_architect,
    blocks.bck_agent_designer,
    blocks.bck_agent_presentation,

    # ── Part 5: Skills ────────────────────────────────────────
    blocks.bck_skills_overview,
    blocks.bck_blueprints,
    blocks.bck_design_rules,

    # ── Part 6: Best Practices ────────────────────────────────
    blocks.bck_bp_prompting,
    blocks.bck_bp_workflow,
    blocks.bck_bp_collaboration,

    # ── Part 7: Tutorial ─────────────────────────────────────
    blocks.bck_tutorial_presentation,

    # ── Part 8: Advanced ──────────────────────────────────────
    blocks.bck_ai_image_overview,
    blocks.bck_ai_image_usage,
    blocks.bck_ai_image_example,
    blocks.bck_memory,
    blocks.bck_stx_guide,
    blocks.bck_custom_commands,
    blocks.bck_custom_agents,
    blocks.bck_custom_profiles,
    blocks.bck_multi_machine,
    blocks.bck_cli_integration,

    # ── Part 9: Reference ─────────────────────────────────────
    blocks.bck_ref_commands,
    blocks.bck_ref_agents,
    blocks.bck_ref_skills,
    blocks.bck_ref_profiles,
    blocks.bck_faq,
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
            filename="streamtex-ai",
            timestamp=True,
        ),
        ExportConfig(
            format="pdf",
            mode=ExportMode.MANUAL,
            output_dir="./exports",
            filename="streamtex-ai",
            timestamp=True,
            pdf=PdfConfig(
                format="A4", landscape=True,
                margin_top="0", margin_bottom="0",
                margin_left="0", margin_right="0",
            ),
        ),
    ])
