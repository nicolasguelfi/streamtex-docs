"""Atomic block — Test coverage matrix."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Coverage matrix styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Test Coverage Matrix", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The StreamTeX test suite contains 44 test files organized
            by functional area. The target is >80% line coverage for
            all modules. Below is the full inventory grouped by area.
        """)
        st_space("v", 2)

        # --- Core rendering ---
        st_write(bs.sub, "Core rendering", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_write.py")
            with g.cell(): st_write(s.large, "st_write, text rendering, inline tuples")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_container.py")
            with g.cell(): st_write(s.large, "st_block, st_span context managers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_grid.py")
            with g.cell(): st_write(s.large, "st_grid layout, cell rendering")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_list.py")
            with g.cell(): st_write(s.large, "st_list, ordered/unordered/custom lists")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_code.py")
            with g.cell(): st_write(s.large, "st_code, Pygments syntax highlighting")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_image.py")
            with g.cell(): st_write(s.large, "st_image, base64 encoding")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_space.py")
            with g.cell(): st_write(s.large, "st_space, st_br spacing utilities")
        st_space("v", 2)

        # --- Navigation ---
        st_write(bs.sub, "Navigation", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_toc.py")
            with g.cell(): st_write(s.large, "Table of contents registry and rendering")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_marker.py")
            with g.cell(): st_write(s.large, "In-page anchor markers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_book_integration.py")
            with g.cell(): st_write(s.large, "st_book pagination and block orchestration")
        st_space("v", 2)

        # --- Export ---
        st_write(bs.sub, "Export", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_export.py")
            with g.cell(): st_write(s.large, "Export buffer, AST guard, HTML generation")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_export_widgets.py")
            with g.cell(): st_write(s.large, "Widget export (dataframe, charts)")
        st_space("v", 2)

        # --- Data ---
        st_write(bs.sub, "Data", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_bib.py")
            with g.cell(): st_write(s.large, "Bibliography registry and citations")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_gsheet.py")
            with g.cell(): st_write(s.large, "Google Sheets integration")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_auth.py")
            with g.cell(): st_write(s.large, "Authentication and credentials")
        st_space("v", 2)

        # --- Diagrams ---
        st_write(bs.sub, "Diagrams", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_mermaid.py")
            with g.cell(): st_write(s.large, "Mermaid diagram rendering")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_plantuml.py")
            with g.cell(): st_write(s.large, "PlantUML diagram rendering")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_tikz.py")
            with g.cell(): st_write(s.large, "TikZ diagram rendering via LaTeX")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_latex.py")
            with g.cell(): st_write(s.large, "LaTeX math rendering")
        st_space("v", 2)

        # --- CLI ---
        st_write(bs.sub, "CLI", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_project.py")
            with g.cell(): st_write(s.large, "stx project create/init commands")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_workspace.py")
            with g.cell(): st_write(s.large, "stx workspace management")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_deploy.py")
            with g.cell(): st_write(s.large, "stx deploy command")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_publish.py")
            with g.cell(): st_write(s.large, "stx publish to PyPI")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_claude.py")
            with g.cell(): st_write(s.large, "stx claude integration commands")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_cli_bib.py")
            with g.cell(): st_write(s.large, "stx bib bibliography commands")
        st_space("v", 2)

        # --- Infrastructure ---
        st_write(bs.sub, "Infrastructure", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Test file")
            with g.cell(): st_write(s.bold + s.large, "Covers")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_blocks.py")
            with g.cell(): st_write(s.large, "Block registry, lazy loading, include")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_block_helpers.py")
            with g.cell(): st_write(s.large, "show_code, show_explanation, show_details")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_inspector.py")
            with g.cell(): st_write(s.large, "Block inspector and debug tools")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "test_styles.py")
            with g.cell(): st_write(s.large, "Style class, composition, CSS generation")
        st_space("v", 2)

        # --- Coverage target ---
        show_explanation("""\
            To check current coverage for a specific module, run:
        """)
        st_space("v", 1)

        show_code(textwrap.dedent("""\
            # Coverage for a single module
            uv run pytest tests/test_write.py --cov=streamtex.write -v

            # Full coverage report
            uv run pytest --cov=streamtex --cov-report=term-missing tests/\
        """), language="bash")
        st_space("v", 2)

        show_details("""\
            The target is >80% line coverage for all modules.

            If coverage drops below the threshold, the CI pipeline
            will warn but not fail (soft gate). Focus coverage efforts
            on core rendering and export modules first, as they carry
            the highest risk of user-facing regressions.
        """)
