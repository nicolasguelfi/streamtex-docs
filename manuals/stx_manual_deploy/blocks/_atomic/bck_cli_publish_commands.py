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

        # --- Publishing a reuse pack via Pack Engineering ---
        st_write(bs.sub, "Publishing a reuse pack (via Pack Engineering)",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The stx publish commands above target generic Python
            packages. For **reuse packs** (packs that ship
            StreamTeX components, design systems, and kits — like
            streamtex-design), there is a higher-level orchestrated
            release flow available via the **Pack Engineering** module.

            Run /stx-pe:publish <pack-path> instead of stx publish pypi
            to get:

            1. **Pre-release validation** — working tree clean check,
               stx component validate on every component, manifest
               validity (PV001-PV010).
            2. **Computed semver bump** — from the pack-master-plan's
               decisions_log (REMOVED -> major, CHANGED -> minor,
               ADDED only -> patch). Pack semver is independent from
               the streamtex library's "stay on 0.7.X" rule.
            3. **CHANGELOG entry generation** — from the cycle's
               decisions log since the last publish_decided entry.
            4. **Atomic bump + commit + signed tag** in one step.
            5. **PyPI publish QCM** — never auto-publishes, always
               requires explicit user approval (even in autonomous
               mode).
            6. **Optional upstream PR** — for fork-packs with mature
               components, propose a PR back to the upstream
               (e.g. PRs from a streamtex-design fork back to
               streamtex-design).

            See the Reuse Architecture manual for the full Pack
            Engineering walkthrough, or .claude/references/pe_cheatsheet_en.md
            for the command reference.
        """)
        st_space("v", 1)

        show_code("""\
            # Release a mature pack via PE
            /stx-pe:publish ../streamtex-design

            # Force a specific bump
            /stx-pe:publish --bump minor ../streamtex-design

            # Tag-only, skip PyPI upload
            /stx-pe:publish --target tag ../streamtex-design

            # Fork-pack: propose upstream PR for mature components
            /stx-pe:publish --pr-upstream streamtex/streamtex-design ../design-edu
        """, language="bash", line_numbers=False)
        st_space("v", 1)
