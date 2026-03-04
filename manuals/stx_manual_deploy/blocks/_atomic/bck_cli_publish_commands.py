"""Atomic block — CLI Publish Commands reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """CLI publish commands styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    """CLI Publish Commands — stx publish subcommands."""
    with st_block(s.center_txt):
        st_write(bs.heading, "CLI Publish Commands", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The stx publish command group handles package
            verification and publishing to PyPI.
        """)
        st_space("v", 2)

        # --- stx publish check ---
        st_write(bs.sub, "stx publish check", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Verify your package before publishing. This command
            runs a comprehensive set of pre-publish validations.
        """)
        st_space("v", 1)

        show_code("""\
            stx publish check
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        st_write(bs.sub, "Validation steps", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The publish check command performs the following
            validations:

            1. **Version sync** — ensures pyproject.toml version
               matches __version__ in the package source.

            2. **Changelog check** — verifies that CHANGELOG.md
               contains an entry for the current version.

            3. **Test suite** — runs the full test suite and
               requires all tests to pass.

            4. **Lint check** — runs ruff to confirm zero warnings.

            5. **Build check** — builds the sdist and wheel to
               verify packaging is correct.
        """)
        st_space("v", 2)

        # --- stx publish pypi ---
        st_write(bs.sub, "stx publish pypi", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Publish the package to PyPI. Runs stx publish check
            first, then builds and uploads the distribution.
        """)
        st_space("v", 1)

        show_code("""\
            stx publish pypi
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        show_details("""\
            For production releases, prefer using GitHub Releases
            with OIDC trusted publishing. This provides a fully
            automated, auditable pipeline:

            1. **Create a GitHub Release** with the version tag.
            2. **CI builds, checks, and publishes** to PyPI
               using OIDC (no API tokens needed).
            3. **The release is signed** and traceable.

            Use stx publish pypi only for local testing or
            pre-release uploads to TestPyPI.
        """)
        st_space("v", 1)
