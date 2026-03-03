import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Version sync styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Version Synchronization",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Two sources of truth ---
        st_write(bs.sub, "Two places where version must match", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The package version is declared in two files. Both must
            contain the exact same version string at all times.
        """)
        st_space("v", 1)

        show_code("""\
# 1. pyproject.toml — used by build tools and PyPI
[project]
name = "streamtex"
version = "X.Y.Z"

# 2. streamtex/__init__.py — used at runtime
__version__ = "X.Y.Z\"""", language="python")
        st_space("v", 2)

        # --- Why both? ---
        st_write(bs.sub, "Why both files?", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            pyproject.toml is read by build backends (uv build, pip)
            to set the version on PyPI. streamtex/__init__.py exposes
            the version at runtime so users can call:

                import streamtex
                print(streamtex.__version__)

            If these two values drift apart, published packages will
            report an incorrect version at runtime.
        """)
        st_space("v", 2)

        # --- Verification command ---
        st_write(bs.sub, "Verifying version consistency", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Use the stx CLI to check that versions match
stx publish check""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            The stx publish check command reads both files, compares
            the version strings, and reports any mismatch. It also
            verifies that CHANGELOG.md contains an entry for the
            current version and checks the git status for uncommitted
            changes. Run this command before every release.
        """)
        st_space("v", 2)

        # --- Summary grid ---
        st_write(bs.sub, "File locations", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "File")
            with g.cell(): st_write(s.bold + s.large, "Field")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "pyproject.toml")
            with g.cell():
                st_write(s.large, "version = \"X.Y.Z\"")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "streamtex/__init__.py")
            with g.cell():
                st_write(s.large, "__version__ = \"X.Y.Z\"")
        st_space("v", 2)

        show_details("""\
            A future improvement may use dynamic versioning
            (single source of truth), but for now the two-file
            approach is explicit and easy to verify with stx publish check.
        """)
