import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Release checklist styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Release Checklist",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Versioning scheme ---
        st_write(bs.sub, "Versioning scheme", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX follows semantic versioning (semver):
            MAJOR.MINOR.PATCH (e.g. 1.2.3).

            - MAJOR: incompatible API changes.
            - MINOR: new features, backward-compatible.
            - PATCH: backward-compatible bug fixes.

            Decide which component to bump based on the
            changes included in this release.
        """)
        st_space("v", 2)

        # --- Step-by-step ---
        st_write(bs.sub, "Step-by-step release process", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# 1. Update CHANGELOG.md with the new version section
#    Add a heading: ## [X.Y.Z] - YYYY-MM-DD
#    List all notable changes under Added / Changed / Fixed

# 2. Update version in pyproject.toml
#    version = "X.Y.Z"

# 3. Update version in streamtex/__init__.py
#    __version__ = "X.Y.Z"

# 4. Run the full test suite
uv run pytest tests/ -v

# 5. Run the linter
uv run ruff check streamtex/

# 6. Commit the release
git commit -am "Release vX.Y.Z"

# 7. Tag the release
git tag vX.Y.Z

# 8. Push to main with tags
git push origin main --tags

# 9. Create a GitHub Release from the tag
#    → This triggers publish.yml automatically""", language="bash")
        st_space("v", 2)

        # --- Checklist summary ---
        st_write(bs.sub, "Checklist summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Step")
            with g.cell(): st_write(s.bold + s.large, "Action")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "1")
            with g.cell():
                st_write(s.large, "Decide version bump (major / minor / patch)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "2")
            with g.cell():
                st_write(s.large, "Update CHANGELOG.md")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "3")
            with g.cell():
                st_write(s.large, "Update version in pyproject.toml")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "4")
            with g.cell():
                st_write(s.large, "Update __version__ in streamtex/__init__.py")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "5")
            with g.cell():
                st_write(s.large, "Run uv run pytest tests/ -v")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "6")
            with g.cell():
                st_write(s.large, "Run uv run ruff check streamtex/")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "7")
            with g.cell():
                st_write(s.large, "git commit -am \"Release vX.Y.Z\"")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "8")
            with g.cell():
                st_write(s.large, "git tag vX.Y.Z")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "9")
            with g.cell():
                st_write(s.large, "git push origin main --tags")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "10")
            with g.cell():
                st_write(s.large, "Create GitHub Release from tag")
        st_space("v", 2)

        show_details("""\
            Always run tests and lint before tagging. A failed CI
            on the publish workflow means the package will not reach
            PyPI, but the tag and release will still exist on GitHub.
        """)
