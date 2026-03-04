from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Publish to PyPI styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Publishing to PyPI",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Pre-publish checks ---
        st_write(bs.sub, "Pre-publish checks", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Verify version consistency, changelog, and git status
stx publish check""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Before publishing, stx publish check verifies:

            - Version in **pyproject.toml** matches **streamtex/__init__.py**.
            - **CHANGELOG.md** contains an entry for the current version.
            - Working directory is clean (no uncommitted changes).
            - Current branch is **main**.
        """)
        st_space("v", 2)

        # --- Automated publishing ---
        st_write(bs.sub, "Automated publishing (recommended)", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The recommended approach is to create a GitHub Release.
            This triggers publish.yml, which builds and publishes
            the package automatically using OIDC Trusted Publishing.
            No manual steps are needed after creating the release.
        """)
        st_space("v", 1)

        show_code("""\
# 1. Push your tagged commit
git push origin main --tags

# 2. Create a GitHub Release from the tag
#    Go to: github.com/<owner>/<repo>/releases/new
#    Select the tag, write release notes, click "Publish release"
#    → publish.yml runs automatically""", language="bash")
        st_space("v", 2)

        # --- Manual publishing ---
        st_write(bs.sub, "Manual publishing (alternative)", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Build the package locally
uv build

# This creates:
#   dist/streamtex-X.Y.Z-py3-none-any.whl
#   dist/streamtex-X.Y.Z.tar.gz

# Publish via the stx CLI
stx publish pypi""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Manual publishing is available via stx publish pypi as
            a fallback. However, the automated GitHub Release flow
            is preferred because it uses Trusted Publishing (OIDC)
            and does not require any local API tokens.
        """)
        st_space("v", 2)

        # --- Trusted Publishing ---
        st_write(bs.sub, "How Trusted Publishing works", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Trusted Publishing eliminates the need for PyPI API tokens.
            Here is how it works:

            1. When publish.yml runs, GitHub mints a **short-lived OIDC
               token** that identifies the repository and workflow.
            2. The **pypa/gh-action-pypi-publish** action sends this token
               to PyPI along with the built package.
            3. PyPI **verifies the token** against the trusted publisher
               configuration you set up in your project settings.
            4. If the token is valid, PyPI **accepts the upload**.

            Benefits:

            - **No stored secrets** in the repository.
            - **Tokens are short-lived** and scoped to the workflow.
            - **Full audit trail** on both GitHub and PyPI.
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
                         "stx publish check")
            with g.cell():
                st_write(s.large, "Verify version, changelog, git status")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx publish pypi")
            with g.cell():
                st_write(s.large, "Build and publish manually")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv build")
            with g.cell():
                st_write(s.large, "Build .whl and .tar.gz in dist/")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "GitHub Release")
            with g.cell():
                st_write(s.large, "Trigger automated publish via OIDC")
        st_space("v", 2)

        show_details("""\
            Always prefer the automated GitHub Release path over manual
            publishing. It provides a consistent, auditable process and
            avoids the need to manage API tokens locally.
        """)
