from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Publish workflow styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Publish Workflow (publish.yml)",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Overview ---
        st_write(bs.sub, "Overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The publish.yml workflow is triggered when a GitHub Release
            is published. It builds the package, runs final checks, and
            publishes to PyPI using OIDC Trusted Publishing — no stored
            API tokens or secrets required.
        """)
        st_space("v", 2)

        # --- Trigger ---
        st_write(bs.sub, "Trigger", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
on:
  release:
    types: [published]""", language="yaml")
        st_space("v", 1)

        show_explanation("""\
            The workflow only runs when a GitHub Release is published.
            This ensures that only tagged, reviewed releases reach PyPI.
            Draft releases do not trigger publication.
        """)
        st_space("v", 2)

        # --- Permissions ---
        st_write(bs.sub, "Permissions", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
permissions:
  contents: read
  id-token: write""", language="yaml")
        st_space("v", 1)

        show_explanation("""\
            Two permissions are required:

            - **contents: read** — to check out the repository code.
            - **id-token: write** — to request an OIDC token from GitHub,
              which PyPI uses to verify the publisher identity.
        """)
        st_space("v", 2)

        # --- Full workflow ---
        st_write(bs.sub, "Full workflow", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync --frozen

      - name: Test
        run: uv run pytest tests/ -v

      - name: Lint
        run: uv run ruff check streamtex/

      - name: Build
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1""", language="yaml")
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
                         "uv python install")
            with g.cell():
                st_write(s.large, "Install Python via uv")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv sync --frozen")
            with g.cell():
                st_write(s.large, "Install locked dependencies")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "pytest + ruff")
            with g.cell():
                st_write(s.large, "Final safety checks before publish")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv build")
            with g.cell():
                st_write(s.large, "Build .whl and .tar.gz in dist/")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "gh-action-pypi-publish")
            with g.cell():
                st_write(s.large, "Upload to PyPI via OIDC")
        st_space("v", 2)

        # --- Trusted Publishing setup ---
        st_write(bs.sub, "Setting up Trusted Publishing on PyPI", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Trusted Publishing uses OpenID Connect (OIDC) so GitHub Actions
            can publish to PyPI without storing any API tokens. To set it up:

            1. **Go to pypi.org** and navigate to your project settings.
            2. **Add a new publisher** under "Publishing".
            3. **Select "GitHub Actions"** as the provider.
            4. **Enter the repository** owner and name (e.g. nicolasguelfi/streamtex).
            5. **Set the workflow name** to "publish.yml".
            6. **Set the environment name** (optional, leave blank for default).
            7. **Save** — PyPI will now accept tokens from that workflow.

            When the workflow runs, GitHub mints a short-lived OIDC token.
            The pypa/gh-action-pypi-publish action exchanges this token
            with PyPI to authenticate the upload. No long-lived secrets
            are ever stored in the repository.
        """)
        st_space("v", 2)

        show_details("""\
            Trusted Publishing is the recommended approach for all new
            PyPI packages. It eliminates the risk of leaked API tokens
            and provides an auditable chain of trust from GitHub to PyPI.
        """)
