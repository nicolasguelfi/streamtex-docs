"""Collection home — gradient header + project cards from collection.toml.

Cards are generated dynamically from collection.toml.
To add a manual: add a [projects.xxx] section in collection.toml
and set STX_URL_XXX env var in Coolify. No code change needed.
"""

import math
import os
import tomllib
from pathlib import Path

import streamlit as st
from custom.styles import Styles as s

import streamtex as stx
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style

_LOGO = "https://media.githubusercontent.com/media/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png"

# Load collection config once
_TOML_PATH = Path(__file__).parent.parent / "collection.toml"
with open(_TOML_PATH, "rb") as _f:
    _CONFIG = tomllib.load(_f)

_CARDS_PER_ROW = _CONFIG.get("collection", {}).get("cards_per_row", 3)

# Build sorted project list with resolved URLs
_PROJECTS = []
for _key, _data in sorted(
    _CONFIG.get("projects", {}).items(),
    key=lambda item: item[1].get("order", 0),
):
    env_key = "STX_URL_" + _key.upper().replace("-", "_")
    _PROJECTS.append({
        "key": _key,
        "title": _data.get("title", _key),
        "description": _data.get("description", ""),
        "emoji": _data.get("emoji", "📄"),
        "button_label": _data.get("button_label", "Open"),
        "url": os.environ.get(env_key, _data.get("project_url", "#")),
    })


class BlockStyles:
    """Styles for the collection home page."""

    header = Style(
        "background: linear-gradient(135deg, #f46b45 0%, #eea849 100%); "
        "padding: 40px 20px; border-radius: 8px;",
        "collection_header",
    )
    level_box = Style(
        "background: rgba(46, 196, 182, 0.08); "
        "border-left: 4px solid #2EC4B6; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "collection_level_box",
    )
    level_label = Style(
        "color: #2EC4B6; font-weight: bold; font-size: 14pt; "
        "text-transform: uppercase; letter-spacing: 2px;",
        "collection_level_label",
    )
    description = s.large
    logo = Style("width: 100%; max-width: 200px;", "collection_logo")
    logo_cell = Style("display: flex; flex-direction: column; align-items: center; gap: 12px;", "collection_logo_cell")
    card_container = Style(
        "border: 1px solid rgba(255,255,255,0.1); "
        "border-radius: 12px; padding: 24px; "
        "background: rgba(255,255,255,0.03); "
        "transition: transform 0.2s, box-shadow 0.2s;",
        "collection_card",
    )
    card_description = s.medium
    project_title = Style(
        "font-weight: bold; font-size: 22pt;",
        "project_title",
    )
    grid_with_gap = stx.StxStyles.container.grid.gap_24
    footer = Style.create(
        s.medium + s.text.colors.white + "opacity:0.6;text-align:center;",
        "collection_footer",
    )


bs = BlockStyles


def _render_card(project: dict) -> None:
    """Render a single project card from a project dict."""
    with st_block(bs.card_container):
        st_space("v", 1)
        st_write(s.huge + "text-align:center;", project["emoji"])
        st_space("v", 1)
        st_write(bs.project_title + "text-align:center;", project["title"])
        st_space("v", 1)
        st_write(bs.card_description + "text-align:center;", project["description"])
        st_space("v", 2)
        # Styled full-width anchor — gradient background matching the
        # header.  We bypass st.link_button (its theming is hard to
        # override and inside Streamlit columns it cannot span 100% of
        # the card width because of the column padding).
        _button_css = (
            "display:block;width:100%;box-sizing:border-box;"
            "padding:14px 24px;"
            "background:linear-gradient(135deg,#f46b45 0%,#eea849 100%);"
            "color:white;text-align:center;"
            "border-radius:8px;text-decoration:none;"
            "font-weight:600;font-size:15px;letter-spacing:0.3px;"
            "box-shadow:0 2px 8px rgba(244,107,69,0.25);"
            "transition:transform 0.15s,box-shadow 0.15s;"
        )
        st.html(
            f'<a href="{project["url"]}" target="_blank" rel="noopener" '
            f'style="{_button_css}">'
            f'{project["emoji"]} {project["button_label"]}</a>'
        )
        st_space("v", 1)


def build():
    """Render the collection home: header, level badge, project cards."""

    # === Gradient header ===
    st_space("v", 1)
    with st_block(bs.header):
        with st_grid(cols="25% 1fr", breakpoint="600px", cell_styles=[bs.logo_cell, None]) as g:
            with g.cell():
                st_image(bs.logo, uri=_LOGO)
                st.link_button("❤️ Support us!", "https://github.com/sponsors/nicolasguelfi", use_container_width=True)
            with g.cell():
                st_write(
                    stx.StxStyles.LARGE + stx.StxStyles.text.colors.white,
                    "StreamTeX Training Course",
                    tag=t.div,
                    toc_lvl="1",
                )
                st_write(
                    stx.StxStyles.large + stx.StxStyles.text.colors.white,
                    "A Streamlit-based content rendering framework",
                    tag=t.div,
                )
    st_space("v", 1)

    # === Level badge ===
    with st_block(bs.level_box):
        st_write(bs.level_label, "Collection Hub")
        st_space("v", 0.5)
        st_write(
            s.Large + s.text.weights.bold_weight,
            "Discover and Explore Our Learning Paths",
        )
        st_space("v", 1)
        st_write(
            bs.description,
            "Browse the curated StreamTeX training courses. "
            "Each course is self-contained and can be launched independently. "
            "AI-powered workflows let you create content without writing a single line of Python.",
        )
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            for proj in _PROJECTS:
                with l.item(): st_write(s.medium, f"{proj['title']}: {proj['description']}")

    # === Project cards — dynamic rows ===
    st_space("v", 2)

    num_rows = math.ceil(len(_PROJECTS) / _CARDS_PER_ROW)
    for row_idx in range(num_rows):
        row_projects = _PROJECTS[row_idx * _CARDS_PER_ROW:(row_idx + 1) * _CARDS_PER_ROW]
        cols_in_row = len(row_projects)

        with st_grid(cols=cols_in_row, responsive=True, grid_style=bs.grid_with_gap):
            for proj in row_projects:
                _render_card(proj)

        if row_idx < num_rows - 1:
            st_space("v", 1)

    # === Footer ===
    st_space("v", 3)
    st.divider()
    st_space("v", 2)
    st_write(
        bs.footer,
        "StreamTeX Training Collection © 2026 | "
        "Interactive documentation for modern web education",
    )
    st_space("v", 2)
