"""Block — Hetzner + Coolify Deployment."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Hetzner deployment block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Hetzner + Coolify Deployment", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation(
            "The recommended production deployment path. "
            "Hetzner provides affordable ARM servers (cax21, ~4 EUR/mo), "
            "fast provisioning, and excellent EU hosting. "
            "Coolify is an open-source PaaS that handles Docker orchestration, "
            "auto-SSL via Traefik, and deployment automation."
        )
        st_space("v", 2)

        # --- Architecture ---
        st_write(bs.sub, "Architecture overview", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            Hetzner Cloud Server (cax21 ARM)
            +-----------------------------------------------+
            |  Coolify (open-source PaaS)                   |
            |  +------------------------------------------+ |
            |  |  Traefik (reverse proxy + auto-SSL)      | |
            |  |  +-------------------------------------+ | |
            |  |  |  Docker containers                  | | |
            |  |  |  +------+ +------+ +------+         | | |
            |  |  |  | docs | |intro | | ai   |  ...    | | |
            |  |  |  +------+ +------+ +------+         | | |
            |  |  +-------------------------------------+ | |
            |  +------------------------------------------+ |
            +-----------------------------------------------+
                          |
                  streamtex.org (Cloudflare DNS + CDN)
        """, language="text")
        st_space("v", 2)

        # --- Two deployment paths ---
        st_write(bs.sub, "Two deployment paths", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "You can deploy either through the CLI (step-by-step commands) "
            "or through Claude (autonomous or guided). Both paths produce "
            "the same result."
        )
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell():
                st_write(s.bold + s.large, "CLI path (step-by-step)")
                st_space("v", 1)
                show_code("""\
                    stx deploy setup
                    stx deploy provision
                    stx deploy secure
                    stx deploy install-coolify
                    stx deploy configure-domain
                    stx deploy hetzner
                """, language="bash", line_numbers=False)
            with g.cell():
                st_write(s.bold + s.large, "Claude path (autonomous)")
                st_space("v", 1)
                show_code("""\
                    # Full autonomous deployment
                    /stx-deploy:go

                    # Or individual steps
                    /stx-deploy:setup
                    /stx-deploy:provision
                    /stx-deploy:deploy
                """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- CLI commands detail ---
        st_write(bs.sub, "CLI commands in detail", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "**stx deploy setup** — Interactive local setup. Creates .stx-deploy.env "
            "with your Hetzner API token, SSH key path, server size, and domain."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy setup
            # Prompts for:
            #   Hetzner API token
            #   SSH key path (default: ~/.ssh/hetzner_streamtex)
            #   Server type (default: cax21)
            #   Domain (default: streamtex.org)
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation(
            "**stx deploy provision** — Creates the Hetzner cloud server. "
            "Allocates a cax21 ARM instance, attaches your SSH key, "
            "and waits for the server to be reachable."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy provision
            # Creates server via Hetzner API
            # Output: Server IP, server ID
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation(
            "**stx deploy secure** — Hardens the server. Disables password auth, "
            "configures UFW firewall (ports 22, 80, 443, 8000), "
            "and sets up automatic security updates."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy secure
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation(
            "**stx deploy install-coolify** — Installs Coolify on the server. "
            "Runs the official Coolify installer, waits for the dashboard "
            "to be available, and stores the admin URL."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy install-coolify
            # Dashboard: https://coolify.streamtex.org
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation(
            "**stx deploy configure-domain** — Configures DNS and SSL. "
            "Points your domain to the server IP via Cloudflare, "
            "sets up wildcard DNS for subdomains, "
            "and enables SSL Full (strict) mode."
        )
        st_space("v", 1)

        show_code("""\
            stx deploy configure-domain
            # Configures: *.streamtex.org -> server IP
            # SSL: Cloudflare Full (strict)
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation(
            "**stx deploy hetzner [PATH]** — Deploys a project to Coolify. "
            "Creates the Coolify application, sets env vars (FOLDER), "
            "triggers Docker build, and waits for health check."
        )
        st_space("v", 1)

        show_code("""\
            # Deploy the docs collection
            stx deploy hetzner

            # Deploy a specific project
            stx deploy hetzner projects/my_project
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- State files ---
        st_write(bs.sub, "State files", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "Two files track deployment state and credentials."
        )
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "File")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell(): st_write(s.bold + s.large, "Git-tracked?")

            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    ".stx-deploy.env")
            with g.cell(): st_write(s.large,
                                    "API tokens, SSH key path, domain, server IP")
            with g.cell(): st_write(s.project.colors.warning_red + s.large, "No (.gitignore)")

            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    ".stx-deploy.json")
            with g.cell(): st_write(s.large,
                                    "Service UUIDs, last deploy timestamps, health status")
            with g.cell(): st_write(s.project.colors.success_green + s.large, "Yes")

        st_space("v", 2)

        # --- Daily management ---
        st_write(bs.sub, "Daily management", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "Once deployed, use these commands for ongoing management."
        )
        st_space("v", 1)

        show_code("""\
            # Check status of all deployed services
            stx deploy status

            # Rebuild and redeploy (full Docker build)
            stx deploy update

            # Quick restart (no rebuild, faster)
            stx deploy update --quick

            # Redeploy a specific service
            stx deploy update docs-intro
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- Auto-deploy via GitHub Actions ---
        st_write(bs.sub, "Auto-deploy via GitHub Actions", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(
            "The hetzner-deploy.yml workflow automates deployment on every push to main. "
            "It detects which files changed, waits for the new PyPI version to be available, "
            "then triggers Coolify redeployment only for affected services."
        )
        st_space("v", 1)

        show_code("""\
            # .github/workflows/hetzner-deploy.yml
            # Triggers:
            #   - push to main
            #   - manual dispatch (workflow_dispatch)
            #
            # Steps:
            #   1. Detect changed files
            #   2. Wait for PyPI version (if library changed)
            #   3. Call Coolify API for each affected service:
            #      GET /api/v1/deploy?uuid=<service-uuid>
            #
            # Required secret: COOLIFY_API_TOKEN
        """, language="text")
        st_space("v", 2)

        # --- Services table ---
        st_write(bs.sub, "Deployed services", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=3, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Service")
            with g.cell(): st_write(s.bold + s.large, "URL")
            with g.cell(): st_write(s.bold + s.large, "FOLDER")

            with g.cell(): st_write(s.large, "docs")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manuals_collection")

            with g.cell(): st_write(s.large, "docs-intro")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-intro.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_intro")

            with g.cell(): st_write(s.large, "docs-advanced")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-advanced.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_advanced")

            with g.cell(): st_write(s.large, "docs-deploy")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-deploy.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_deploy")

            with g.cell(): st_write(s.large, "docs-developer")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-developer.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_developer")

            with g.cell(): st_write(s.large, "docs-ai")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-ai.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_ai")

            with g.cell(): st_write(s.large, "docs-ce")
            with g.cell(): st_write(s.project.colors.accent_teal + s.large,
                                    "docs-ce.streamtex.org")
            with g.cell(): st_write(s.project.colors.neutral_gray + s.large,
                                    "manuals/stx_manual_ce")

        st_space("v", 2)

        show_details(
            "**Server**: Hetzner cax21 ARM (4 vCPU, 8 GB RAM, 40 GB SSD) at 138.199.148.59\n\n"
            "**Domain**: streamtex.org registered at OVH, DNS managed by Cloudflare (free CDN + WAF)\n\n"
            "**Coolify admin**: https://coolify.streamtex.org\n\n"
            "**SSH access**: `ssh root@138.199.148.59 -i ~/.ssh/hetzner_streamtex`\n\n"
            "**Tokens**: Hetzner and Coolify API tokens are stored in streamtex/.env "
            "(HETZNER_API_TOKEN, COOLIFY_API_TOKEN) and in GitHub secrets."
        )
