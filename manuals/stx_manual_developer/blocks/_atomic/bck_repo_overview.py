"""Atomic block — Repository tree overview."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Repository overview styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Repository Structure", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The StreamTeX repository is a single Python package with a flat module
            layout. All source code lives under `streamtex/`, tests mirror the
            package structure, and project configuration is centralised in
            `pyproject.toml`.
        """)
        st_space("v", 2)

        # --- Top-level tree ---
        st_write(bs.sub, "Top-Level Layout", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            streamtex/
            ├── streamtex/           # Main Python package (38 modules)
            │   ├── __init__.py      # Public API exports
            │   ├── cli/             # CLI commands (10 files)
            │   ├── styles/          # Style system
            │   └── static/          # CSS assets
            ├── tests/               # Test suite (44 files)
            ├── documentation/       # Developer docs & maintenance
            ├── .github/workflows/   # CI/CD
            ├── pyproject.toml       # Build system & deps
            ├── CHANGELOG.md         # Version history
            └── uv.lock              # Pinned dependencies\
        """, language="text")
        st_space("v", 2)

        show_details("""\
            The repository follows the src-less layout: the package directory
            `streamtex/` sits at the repository root, alongside `tests/`,
            configuration files, and CI workflows.

            All static assets (CSS, fonts) are bundled inside `streamtex/static/`
            and shipped with the wheel.
        """)
