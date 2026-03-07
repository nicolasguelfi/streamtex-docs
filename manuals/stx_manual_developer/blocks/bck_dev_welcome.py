"""Developer Guide welcome page — prerequisites and overview."""

from pathlib import Path

import streamlit as st
from custom.styles import Styles as s
import streamtex as stx
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style

_LOGO = str(Path(__file__).parent.parent.parent / "shared-blocks" / "logo-stx.png")


class BlockStyles:
    header = Style(
        "background: linear-gradient(135deg, #1a237e 0%, #00897b 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "dev_header",
    )
    level_box = Style(
        "background: rgba(0, 188, 212, 0.08); "
        "border-left: 4px solid #00BCD4; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "dev_level_box",
    )
    level_label = Style(
        "color: #00BCD4; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "dev_level_label",
    )
    logo = Style("width: 100%; height: auto;", "dev_logo")
    logo_cell = Style("display: flex; align-items: center; justify-content: center;", "dev_logo_cell")
    prereq_box = Style(
        "background: rgba(39, 174, 96, 0.08); "
        "border-left: 4px solid #27AE60; "
        "padding: 16px 20px; border-radius: 0 8px 8px 0;",
        "dev_prereq_box",
    )

bs = BlockStyles


def build():
    st_space("v", 1)
    with st_block(bs.header):
        with st_grid(cols="25% 75%", cell_styles=[bs.logo_cell, None]) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button("❤️ Support us!", "https://github.com/sponsors/nicolasguelfi", use_container_width=True)
            with g.cell():
                st_write(
                    stx.StxStyles.LARGE + stx.StxStyles.text.colors.white,
                    "StreamTeX Developer Guide",
                    tag=t.div,
                    toc_lvl="1",
                )
                st_write(
                    stx.StxStyles.large + stx.StxStyles.text.colors.white,
                    "Contributing to the StreamTeX library",
                    tag=t.div,
                )
    st_space("v", 1)

    with st_block(bs.level_box):
        st_write(bs.level_label, "Developer Manual")
        st_space("v", 0.5)
        st_write(
            s.Large + s.text.weights.bold_weight,
            "Everything You Need to Contribute to StreamTeX",
        )
        st_space("v", 1)
        st_write(
            s.large + s.project.colors.neutral_gray,
            "This guide covers the complete developer workflow: from cloning the repo "
            "to publishing a new release on PyPI. It is aimed at library contributors "
            "and maintainers.",
        )
    st_space("v", 2)

    # Prerequisites
    with st_block(bs.prereq_box):
        st_write(s.project.titles.section_subtitle, "Prerequisites", toc_lvl="+1")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, "Python 3.11+ (see .python-version)")
            with l.item(): st_write(s.large, "git (version control)")
            with l.item(): st_write(s.large, "uv — fast Python package manager (replaces pip/venv)")
            with l.item(): st_write(s.large, "A code editor (VS Code, PyCharm, etc.)")
    st_space("v", 2)

    # Guide overview
    st_write(s.project.titles.section_subtitle, "What This Guide Covers", toc_lvl="+1")
    st_space("v", 1)
    with st_list(list_type="ol") as l:
        with l.item(): st_write(s.large, "Repository Structure — understanding the 38 source modules")
        with l.item(): st_write(s.large, "Development Setup — clone, install, workspace management")
        with l.item(): st_write(s.large, "Architecture — rendering pipeline, styles, blocks, export, book")
        with l.item(): st_write(s.large, "Coding Standards — conventions, module patterns, export guards")
        with l.item(): st_write(s.large, "Testing — pytest, patterns, gotchas, coverage matrix")
        with l.item(): st_write(s.large, "CI/CD — GitHub Actions workflows")
        with l.item(): st_write(s.large, "Release Process — versioning, changelog, PyPI publishing")
        with l.item(): st_write(s.large, "CLI Architecture — click groups, adding commands")
        with l.item(): st_write(s.large, "Maintenance — dependencies, ruff, tooling")
        with l.item(): st_write(s.large, "Claude Profiles — .claude/ structure, profile management")
