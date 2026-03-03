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
        st_write(bs.heading, "CI Workflows",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Two repos, two CIs ---
        st_write(bs.sub, "Two repos, two CI workflows", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The StreamTeX ecosystem has two GitHub repos with separate CIs:

            - **streamtex** (library): lint + test on every push/PR
            - **streamtex-docs** (documentation): structural checks on every push/PR

            Both use GitHub Actions and share the same pattern:
            trigger on push to main and PRs targeting main.
        """))
        st_space("v", 2)

        # ============================================================
        # LIBRARY CI
        # ============================================================
        st_write(bs.sub, "Library CI (streamtex repo)", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# streamtex/.github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv python install
      - run: uv sync --frozen
      - run: uv run ruff check streamtex/
      - run: uv run pytest tests/ -v""", language="yaml")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The library CI uses **--frozen** because the library is self-contained:
            uv.lock has no local path dependencies, so frozen installs work directly.
            Steps: install deps from lock file, lint with ruff, run full test suite.
        """))
        st_space("v", 2)

        # ============================================================
        # DOCS CI
        # ============================================================
        st_write(bs.sub, "Docs CI (streamtex-docs repo)", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# streamtex-docs/.github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    env:
      UV_NO_SOURCES: "1"
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv python install
      - run: uv sync
      - name: Verify streamtex import
        run: uv run python -c "import streamtex; ..."
      - name: Verify block structure (143 blocks)
        run: uv run python -c "# AST parse + check build() ..."
      - name: Verify composite → atomic links (73 links)
        run: uv run python -c "# regex load_atomic_block ..."
      - name: Verify book.py files (5 books)
        run: uv run python -c "# AST parse ..." """, language="yaml")
        st_space("v", 2)

        # --- UV_NO_SOURCES explained ---
        st_write(bs.sub, "Why UV_NO_SOURCES=1?", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            In local dev, pyproject.toml points streamtex to a sibling folder:

            ```toml
            [tool.uv.sources]
            streamtex = { path = "../streamtex", editable = true }
            ```

            This is great locally — you edit the library and see changes instantly
            in the docs. But in CI, only streamtex-docs is checked out.
            The folder **../streamtex does not exist**.

            **UV_NO_SOURCES=1** tells uv to ignore [tool.uv.sources] entirely
            and install streamtex from PyPI instead. It is set as a **job-level
            env var** so it applies to ALL uv commands (sync, run, etc.).

            The Dockerfile uses the same approach: `uv sync --no-sources`
            then strips the section with sed.
        """))
        st_space("v", 2)

        # --- Structural checks ---
        st_write(bs.sub, "Structural checks explained", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Check")
            with g.cell(): st_write(s.bold + s.large, "Detects")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "Verify streamtex import")
            with g.cell():
                st_write(s.large, "PyPI version missing, unpublished API")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "Verify block structure")
            with g.cell():
                st_write(s.large,
                         "Syntax errors, missing build(), forgotten git add")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "Verify composite links")
            with g.cell():
                st_write(s.large,
                         "Renamed/deleted atomic not updated in composite")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "Verify book.py files")
            with g.cell():
                st_write(s.large, "Syntax error in book orchestration")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            These checks use Python AST parsing — they validate structure
            without importing streamtex or launching Streamlit. This keeps
            CI fast (~20s) while catching the most common errors.
        """))
