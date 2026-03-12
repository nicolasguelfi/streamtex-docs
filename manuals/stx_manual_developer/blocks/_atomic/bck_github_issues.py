"""GitHub Issues — /stx-issue:* commands and issue tracking workflow."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """GitHub issues styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "GitHub Issues — /stx-issue:*",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Overview ---
        st_write(bs.sub, "Overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The /stx-issue namespace provides 6 commands for GitHub
            issue management: 4 creation commands (bug, feature,
            question, docs) and 2 management commands (comment, list).
            Creation commands auto-collect environment metadata,
            detect the target repository, and compose a well-structured
            issue for you to review before submission.
        """)
        st_space("v", 2)

        # --- Issue Types ---
        st_write(bs.sub, "Issue Types", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Type")
            with g.cell(): st_write(s.bold + s.large, "Label")
            with g.cell(): st_write(s.bold + s.large, "Use Case")
            with g.cell(): st_write(s.large, "bug")
            with g.cell(): st_write(s.large, "bug")
            with g.cell(): st_write(s.large, "Report a defect")
            with g.cell(): st_write(s.large, "feature")
            with g.cell(): st_write(s.large, "enhancement")
            with g.cell(): st_write(s.large, "Request a new feature")
            with g.cell(): st_write(s.large, "question")
            with g.cell(): st_write(s.large, "question")
            with g.cell(): st_write(s.large, "Ask about usage")
            with g.cell(): st_write(s.large, "docs")
            with g.cell(): st_write(s.large, "documentation")
            with g.cell(): st_write(s.large, "Improve documentation")
        st_space("v", 2)

        # --- Usage ---
        st_write(bs.sub, "Usage", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Report a bug
/stx-issue:bug st_grid does not render when cols="1fr 2fr" on mobile

# Request a feature
/stx-issue:feature Add dark mode toggle to st_book sidebar

# Ask a question
/stx-issue:question How to use st_collection with custom routes?

# Documentation improvement
/stx-issue:docs Add example for st_overlay positioning

# Comment on an existing issue
/stx-issue:comment 42 Fixed in v0.3.1, please verify

# List open issues
/stx-issue:list
/stx-issue:list --repo nicolasguelfi/streamtex --state all""", language="bash")
        st_space("v", 2)

        # --- Workflow ---
        st_write(bs.sub, "How It Works", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The creation commands (bug, feature, question, docs) follow
            a 10-step workflow:

            1. Check gh CLI is installed and authenticated
            2. Collect environment metadata (versions, OS, project)
            3. Detect the target repository (streamtex, streamtex-docs, or streamtex-claude)
            4. Check your permissions on the target repo
            5. Gather additional details (reproduction steps for bugs, motivation for features)
            6. Choose language (English recommended, French supported)
            7. Compose the issue with structured template
            8. Preview the full issue for your review
            9. Create the issue after your explicit confirmation
            10. Report the issue URL

            The comment command verifies the issue exists, previews
            the comment, and creates it after confirmation.
            The list command is read-only (no confirmation needed).
        """)
        st_space("v", 2)

        # --- Metadata ---
        st_write(bs.sub, "Auto-Collected Metadata", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The following metadata is collected automatically
            and included in every issue:

            - StreamTeX library version (from uv pip show)
            - Python version
            - Operating system (uname)
            - uv version
            - Project name (from pyproject.toml)
            - Workspace preset (from stx.toml)
            - Claude profile (from .claude/.stx-profile)
            - Current git branch
            - Last commit hash
        """)
        st_space("v", 2)

        # --- Repository Routing ---
        st_write(bs.sub, "Repository Routing", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The command automatically routes issues to the correct repo:

            - Library bugs (st_* functions, Python errors) go to streamtex
            - Documentation issues (manuals, blocks) go to streamtex-docs
            - Profile issues (commands, installation) go to streamtex-claude
            - If ambiguous, the command asks you to choose
        """)
        st_space("v", 2)

        # --- Permissions ---
        st_write(bs.sub, "Permissions and Safety", toc_lvl="+1")
        st_space("v", 1)

        show_details("""\
            The command checks your GitHub permissions before creating issues:

            - With write access: labels are applied automatically
            - With read-only access: labels are skipped, type prefix is added to the title
            - No access: the command stops with a clear error message

            Issues are always previewed before creation. You must explicitly
            confirm before the issue is submitted. No sensitive data (API keys,
            tokens) is ever included in the issue body.
        """)
        st_space("v", 2)

        # --- Prerequisites ---
        st_write(bs.sub, "Prerequisites", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Install GitHub CLI
brew install gh          # macOS
# See https://cli.github.com for other platforms

# Authenticate
gh auth login

# Verify
gh auth status""", language="bash")
        st_space("v", 2)

        # --- Issue Templates ---
        st_write(bs.sub, "GitHub Issue Templates", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            All three StreamTeX repositories include GitHub issue templates
            (.github/ISSUE_TEMPLATE/) for bug reports, feature requests,
            questions, and documentation improvements. These templates
            are also used when creating issues via the GitHub web interface.
        """)
        st_space("v", 2)
