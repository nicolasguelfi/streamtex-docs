import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Dependency management styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Dependency Management",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Core dependencies ---
        st_write(bs.sub, "Core dependencies", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Core dependencies are declared in pyproject.toml under
            [project.dependencies]. These are installed for every
            user of the package.
        """)
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[project]
dependencies = [
    "streamlit>=1.40",
    "beautifulsoup4>=4.12",
    "pygments>=2.17",
    # ... other core deps
]""", language="toml")
        st_space("v", 2)

        # --- Optional dependencies ---
        st_write(bs.sub, "Optional dependencies", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[project.optional-dependencies]
inspector = ["streamlit-inspector>=0.1"]
cli = ["click>=8.1", "rich>=13.0"]""", language="toml")
        st_space("v", 1)

        show_explanation("""\
            Optional dependency groups are installed with:
            uv sync --extra inspector or uv sync --extra cli.
            These are for features that not all users need.
        """)
        st_space("v", 2)

        # --- Dev dependencies ---
        st_write(bs.sub, "Dev dependencies", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    # ... other dev tools
]""", language="toml")
        st_space("v", 1)

        show_explanation("""\
            Dev dependencies are only needed for development and
            testing. They are declared under [dependency-groups]
            and installed by default with uv sync (unless you
            explicitly exclude them).
        """)
        st_space("v", 2)

        # --- Adding dependencies ---
        st_write(bs.sub, "Adding dependencies", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Add a core dependency
uv add <package>

# Add a dev dependency
uv add --group dev <package>

# Add an optional dependency
uv add --optional cli <package>""", language="bash")
        st_space("v", 2)

        # --- Locking and syncing ---
        st_write(bs.sub, "Locking and syncing", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Generate/update uv.lock from pyproject.toml
uv lock

# Install from lock file (never modify it)
uv sync --frozen""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            uv lock resolves all dependencies and writes exact
            versions to uv.lock. This file must be committed to git.

            uv sync --frozen installs exactly what uv.lock specifies,
            without resolving or updating anything. If uv.lock is
            out of date, the command fails — ensuring that CI and
            other developers always use the same versions.
        """)
        st_space("v", 2)

        # --- Command summary ---
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
                         "uv add <pkg>")
            with g.cell():
                st_write(s.large, "Add a core dependency")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv add --group dev <pkg>")
            with g.cell():
                st_write(s.large, "Add a dev dependency")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv lock")
            with g.cell():
                st_write(s.large, "Resolve and write uv.lock")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv sync --frozen")
            with g.cell():
                st_write(s.large, "Install from lock (no updates)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv sync")
            with g.cell():
                st_write(s.large, "Sync and update lock if needed")
        st_space("v", 2)

        show_details("""\
            Always commit uv.lock after running uv lock or uv add.
            Other developers and CI rely on this file for reproducible
            installs. Never add uv.lock to .gitignore.
        """)
