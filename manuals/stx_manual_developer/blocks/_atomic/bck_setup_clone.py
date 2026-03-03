import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Clone and setup styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Clone and Set Up the Dev Environment",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Clone the repository ---
        st_write(bs.sub, "Clone the repository", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Start by cloning the StreamTeX source repository.
            The project uses uv for dependency management,
            so all dependencies are locked in uv.lock.
        """))
        st_space("v", 1)

        show_code("""\
git clone https://github.com/nicolasguelfi/streamtex.git
cd streamtex""", language="bash")
        st_space("v", 2)

        # --- 2. Install dependencies ---
        st_write(bs.sub, "Install dependencies with uv", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            uv sync reads pyproject.toml and uv.lock to install
            all dependencies in an isolated virtual environment.
            This ensures reproducible builds across all machines.
        """))
        st_space("v", 1)

        show_code("""\
# Install all dependencies (including dev group)
uv sync

# The virtual environment is created at .venv/
# uv manages it automatically — no manual activation needed""", language="bash")
        st_space("v", 2)

        # --- 3. Verify the setup ---
        st_write(bs.sub, "Verify the setup", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Run the test suite and linter to confirm
            everything is working correctly.
        """))
        st_space("v", 1)

        show_code("""\
# Run the full test suite
uv run pytest tests/ -v

# Run the linter
uv run ruff check streamtex/

# Both commands should pass with zero errors""", language="bash")
        st_space("v", 2)

        # --- 4. Quick command summary ---
        st_write(bs.sub, "Command summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Command")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "git clone <url>")
            with g.cell():
                st_write(s.large, "Clone the StreamTeX repository")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv sync")
            with g.cell():
                st_write(s.large, "Install all deps from uv.lock")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv run pytest tests/ -v")
            with g.cell():
                st_write(s.large, "Run the test suite")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv run ruff check streamtex/")
            with g.cell():
                st_write(s.large, "Run the linter")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            Never call python, pip, or pytest directly.

            Always prefix commands with uv run to use the managed environment.

            If uv.lock changes after a git pull, run uv sync again.
        """))
