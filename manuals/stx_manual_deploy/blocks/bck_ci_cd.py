"""Block — CI/CD with GitHub Actions."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import os

# Resolve path to the workflow file
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(_project_root)))
_ci_yml_path = os.path.join(_repo_root, ".github", "workflows", "ci.yml")


class BlockStyles:
    """CI/CD block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "CI/CD with GitHub Actions", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation(
            "Automated testing and Docker builds on every push and pull request. "
            "The workflow uses uv for fast dependency installation "
            "and verifies the Docker image with a health check."
        )
        st_space("v", 2)

        # --- What it does ---
        st_write(bs.sub, "Pipeline overview", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Job")
            with g.cell(): st_write(s.bold + s.large, "Trigger")
            with g.cell(): st_write(s.bold + s.large, "Steps")

            with g.cell(): st_write(s.project.colors.accent_teal + s.large, "Tests & Lint")
            with g.cell(): st_write(s.large, "Every push and PR")
            with g.cell(): st_write(s.large,
                                    "Install uv → Install Python → Sync deps → Lint → Tests")

            with g.cell(): st_write(s.project.colors.accent_teal + s.large, "Docker Build")
            with g.cell(): st_write(s.large, "Push to main only")
            with g.cell(): st_write(s.large,
                                    "Build image → Start container → Health check → Stop")

        st_space("v", 2)

        # --- The workflow file ---
        st_write(bs.sub, "The workflow file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "Located at .github/workflows/ci.yml. "
            "Uses the official astral-sh/setup-uv action for fast dependency caching."
        )
        st_space("v", 1)

        try:
            with open(_ci_yml_path) as f:
                ci_content = f.read()
        except FileNotFoundError:
            ci_content = "# ci.yml not found"

        show_code(ci_content, language="yaml")
        st_space("v", 2)

        # --- How to use ---
        st_write(bs.sub, "How it works", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The workflow runs automatically. No manual setup required beyond "
            "having the file in .github/workflows/. "
            "GitHub provides free CI/CD minutes for public repos."
        )
        st_space("v", 1)

        show_code("""\
            # The workflow triggers automatically on:
            # - Push to main branch
            # - Pull request targeting main

            # To check status:
            # 1. Go to your repo on GitHub
            # 2. Click the "Actions" tab
            # 3. See the workflow runs and their status

            # Failed runs block PR merges (if branch protection is enabled)
        """, language="text")
        st_space("v", 2)

        show_details(
            "The **Docker Build** job only runs on **push to main** (not on PRs) to save CI minutes. "
            "It builds the image, starts a container, waits 10 seconds, "
            "then verifies the **health endpoint** responds.\n\n"
            "To add deployment automation, extend the workflow with push-to-registry steps."
        )
        st_space("v", 3)

        # --- Hetzner auto-deploy workflow ---
        st_write(bs.sub, "Hetzner auto-deploy (hetzner-deploy.yml)", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "A dedicated workflow automates deployment to Hetzner/Coolify "
            "on every push to main. It also supports manual dispatch."
        )
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Feature")
            with g.cell(): st_write(s.bold + s.large, "Details")

            with g.cell(): st_write(s.large, "Triggers")
            with g.cell(): st_write(s.large, "Push to main + manual dispatch (workflow_dispatch)")

            with g.cell(): st_write(s.large, "PyPI version guard")
            with g.cell(): st_write(s.large,
                                    "Waits for the new library version to be published on PyPI "
                                    "before deploying (Coolify installs from PyPI, not local)")

            with g.cell(): st_write(s.large, "Change detection")
            with g.cell(): st_write(s.large,
                                    "Selective deploy based on changed files — only affected "
                                    "services are redeployed")

            with g.cell(): st_write(s.large, "Deploy mechanism")
            with g.cell(): st_write(s.large,
                                    "Coolify API: GET /api/v1/deploy?uuid=<service-uuid>")

            with g.cell(): st_write(s.large, "Required secret")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large, "COOLIFY_API_TOKEN")

        st_space("v", 2)

        show_explanation(
            "The workflow deploys 7 services, each identified by its Coolify UUID."
        )
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Service")
            with g.cell(): st_write(s.bold + s.large, "Subdomain")

            with g.cell(): st_write(s.large, "docs (collection hub)")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large, "docs.streamtex.org")

            with g.cell(): st_write(s.large, "docs-intro")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-intro.streamtex.org")

            with g.cell(): st_write(s.large, "docs-advanced")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-advanced.streamtex.org")

            with g.cell(): st_write(s.large, "docs-deploy")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-deploy.streamtex.org")

            with g.cell(): st_write(s.large, "docs-developer")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-developer.streamtex.org")

            with g.cell(): st_write(s.large, "docs-ai")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-ai.streamtex.org")

            with g.cell(): st_write(s.large, "docs-ce")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-ce.streamtex.org")

        st_space("v", 2)

        show_code("""\
            # Example: triggering a single service deploy via Coolify API
            curl -s -H "Authorization: Bearer $COOLIFY_API_TOKEN" \\
              "https://coolify.streamtex.org/api/v1/deploy?uuid=<service-uuid>"
        """, language="bash")
        st_space("v", 2)

        show_details(
            "The **PyPI version guard** is critical: Coolify builds Docker images that "
            "install streamtex from PyPI. If you deploy before the new version is published, "
            "the containers will use the old version and new features will be missing.\n\n"
            "The workflow polls PyPI every 15 seconds until the expected version appears."
        )
