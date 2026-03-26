"""Atomic block — CLI Deploy Commands reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """CLI deploy commands styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    """CLI Deploy Commands — stx deploy subcommands."""
    with st_block(s.center_txt):
        st_write(bs.heading, "CLI Deploy Commands", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The stx deploy command group handles all deployment
            workflows. Each subcommand targets a specific platform
            or deployment step.
        """)
        st_space("v", 2)

        # --- stx deploy preflight ---
        st_write(bs.sub, "stx deploy preflight", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Run pre-deployment checks before deploying to any
            platform. Validates project structure, dependencies,
            and configuration files.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy preflight
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy docker ---
        st_write(bs.sub, "stx deploy docker", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Build a Docker image and run it locally.
            Uses the repository Dockerfile with the correct
            FOLDER build-arg for your project.
        """)
        st_space("v", 1)

        show_code("""\
            # Build and run with default settings
            stx deploy docker

            # Specify a custom port
            stx deploy docker --port 8502
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy render ---
        st_write(bs.sub, "stx deploy render", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Deploy your project to Render.com. Generates the
            render.yaml blueprint and triggers the deployment
            pipeline.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy render
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy huggingface ---
        st_write(bs.sub, "stx deploy huggingface", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Deploy your project to HuggingFace Spaces.
            Pushes the project as a Docker Space with the
            correct app configuration.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy huggingface
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy status ---
        st_write(bs.sub, "stx deploy status", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Check the current deployment status across all
            configured platforms. Reports build state, URL,
            and last deployment timestamp.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy status
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # ============================================================
        # Hetzner/Coolify Commands
        # ============================================================
        st_write(bs.heading, "Hetzner/Coolify Commands", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            Commands for deploying to Hetzner Cloud with Coolify.
            Run them in order for first-time setup, or individually
            for ongoing management.
        """)
        st_space("v", 2)

        # --- stx deploy setup ---
        st_write(bs.sub, "stx deploy setup", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Interactive local setup. Prompts for Hetzner API token,
            SSH key path, server type, and domain. Saves credentials
            to .stx-deploy.env (git-ignored).
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy setup
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy provision ---
        st_write(bs.sub, "stx deploy provision", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Create a Hetzner cloud server. Allocates the instance,
            attaches your SSH key, and waits until the server
            is reachable via SSH.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy provision
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy secure ---
        st_write(bs.sub, "stx deploy secure", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Harden the server. Disables password authentication,
            configures UFW firewall (ports 22, 80, 443, 8000),
            and enables automatic security updates.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy secure
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy install-coolify ---
        st_write(bs.sub, "stx deploy install-coolify", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Install Coolify on the provisioned server. Runs the
            official Coolify installer and waits for the admin
            dashboard to become available.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy install-coolify
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy configure-domain ---
        st_write(bs.sub, "stx deploy configure-domain", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Configure DNS and SSL. Points your domain to the
            server IP via Cloudflare, sets up wildcard DNS
            for subdomains, and enables SSL Full (strict).
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy configure-domain
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy hetzner ---
        st_write(bs.sub, "stx deploy hetzner [PATH]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Deploy a project to Coolify. Creates the application,
            sets the FOLDER env var, triggers a Docker build,
            and waits for the health check to pass.
        """)
        st_space("v", 1)

        show_code("""\
            # Deploy the default project (docs collection)
            stx deploy hetzner

            # Deploy a specific project
            stx deploy hetzner projects/my_project
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy update ---
        st_write(bs.sub, "stx deploy update [TARGET]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Rebuild and redeploy services on Coolify. Without
            arguments, redeploys all services. Use --quick for
            a restart without a full Docker rebuild.
        """)
        st_space("v", 1)

        show_code("""\
            # Rebuild all services
            stx deploy update

            # Quick restart (no rebuild)
            stx deploy update --quick

            # Redeploy a specific service
            stx deploy update docs-intro
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy env-sync ---
        st_write(bs.sub, "stx deploy env-sync", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Sync environment variables to deployed services.
            Reads from .stx-deploy.env and pushes to Coolify
            (or Render for legacy deployments).
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy env-sync
        """, language="bash", line_numbers=False)
        st_space("v", 2)
