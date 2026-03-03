import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """CI workflow styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "CI Workflow (ci.yml)",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Overview ---
        st_write(bs.sub, "Overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The ci.yml workflow runs on every push to main and on
            every pull request targeting main. It ensures that all
            code passes linting and tests before it can be merged.
        """))
        st_space("v", 2)

        # --- Triggers ---
        st_write(bs.sub, "Triggers", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]""", language="yaml")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The workflow fires on two events: direct pushes to main
            and pull requests that target main. This guarantees that
            every change is validated before reaching the main branch.
        """))
        st_space("v", 2)

        # --- Runner and steps ---
        st_write(bs.sub, "Runner and steps", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --frozen

      - name: Lint
        run: uv run ruff check streamtex/

      - name: Test
        run: uv run pytest tests/ -v""", language="yaml")
        st_space("v", 2)

        # --- Frozen installs ---
        st_write(bs.sub, "Why --frozen?", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The --frozen flag tells uv to install exactly what is
            recorded in uv.lock without ever updating it. This
            guarantees reproducible builds: CI uses the same
            dependency versions that developers tested locally.
            If uv.lock is out of date relative to pyproject.toml,
            the command will fail — forcing developers to commit
            an updated lock file before merging.
        """))
        st_space("v", 2)

        # --- Step summary ---
        st_write(bs.sub, "Step summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Step")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "actions/checkout@v4")
            with g.cell():
                st_write(s.large, "Clone the repository")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "astral-sh/setup-uv@v4")
            with g.cell():
                st_write(s.large, "Install the uv package manager")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv sync --frozen")
            with g.cell():
                st_write(s.large, "Install deps from uv.lock (no updates)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "ruff check")
            with g.cell():
                st_write(s.large, "Lint the codebase")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "pytest tests/ -v")
            with g.cell():
                st_write(s.large, "Run the full test suite")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            The CI workflow is intentionally minimal: lint then test.
            Keeping CI fast encourages frequent pushes and quick
            feedback loops for contributors.
        """))
