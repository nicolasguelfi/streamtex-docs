import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Other tooling styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Other Tooling",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- .python-version ---
        st_write(bs.sub, ".python-version", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# .python-version
3.10""", language="text")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            This file pins the Python version for uv. When you run
            uv sync or uv run, uv reads .python-version to determine
            which Python interpreter to use. This ensures all
            developers and CI use the same Python version.
        """))
        st_space("v", 2)

        # --- .gitattributes ---
        st_write(bs.sub, ".gitattributes", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# .gitattributes — Git LFS tracking
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
*.woff2 filter=lfs diff=lfs merge=lfs -text""", language="text")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Binary files (images, fonts, PDFs) are tracked with
            Git LFS to keep the repository lightweight. Git stores
            pointers in the repo and the actual files on the LFS
            server. This prevents repository bloat from large
            binary assets.
        """))
        st_space("v", 2)

        # --- .env ---
        st_write(bs.sub, ".env and python-dotenv", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# .env — local environment variables
STX_DEBUG=true
STX_LOG_LEVEL=debug
# NEVER commit secrets to .env — use .env.example as template""", language="text")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The .env file holds local environment variables.
            StreamTeX uses python-dotenv to auto-load these
            variables at startup. The .env file should be listed
            in .gitignore — never commit secrets. Provide a
            .env.example template with placeholder values for
            new developers.
        """))
        st_space("v", 2)

        # --- pytest config ---
        st_write(bs.sub, "Pytest configuration", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]""", language="toml")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Pytest is configured in pyproject.toml:
            - testpaths: tells pytest to look in tests/ by default.
            - pythonpath: adds the project root to sys.path so
              imports resolve correctly without installation.
        """))
        st_space("v", 2)

        # --- Summary grid ---
        st_write(bs.sub, "Tooling summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "File")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         ".python-version")
            with g.cell():
                st_write(s.large, "Pin Python version for uv")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         ".gitattributes")
            with g.cell():
                st_write(s.large, "Git LFS tracking for binaries")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         ".env")
            with g.cell():
                st_write(s.large, "Local environment variables")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "pyproject.toml [tool.pytest]")
            with g.cell():
                st_write(s.large, "Pytest test paths and Python path")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            These configuration files form the foundation of the
            development environment. They ensure consistency across
            machines and CI. Review them when onboarding new
            developers to understand the project conventions.
        """))
