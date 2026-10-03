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
            Check deployment status for a specific platform.
            Supports coolify (Hetzner) and huggingface.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy status coolify              # Hetzner/Coolify services
            stx deploy status coolify docs-intro   # specific service
            stx deploy status huggingface          # HuggingFace Spaces
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy diff (0.7.38) ---
        st_write(bs.sub, "stx deploy diff [PATH]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Show how the project's Dockerfile, entrypoint.sh and
            nginx.conf differ from the current StreamTeX templates, as a
            unified diff (template → project). Nothing is written:
            stx deploy only generates these files when they are missing,
            so a project keeps its own copy.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy diff
            stx deploy diff path/to/project
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx deploy ci (0.7.38) ---
        st_write(bs.sub, "stx deploy ci [PATH]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Write .github/workflows/stx-validate.yml: install without the
            local streamtex source, ruff, then stx validate --build on
            every push and pull request. --force overwrites an existing
            workflow file.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy ci
            stx deploy ci --force
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

        # --- stx deploy scale ---
        st_write(bs.sub, "stx deploy scale TARGET --replicas N", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Scale a service to N containers. All replicas share the same
            URL — Traefik load-balances automatically. Use before a course
            session with many concurrent users, then scale back to 1 after.
        """)
        st_space("v", 1)

        show_code("""\
            # Scale up for 100 students
            stx deploy scale ai4se6d-genai-intro --replicas 5

            # Scale back
            stx deploy scale ai4se6d-genai-intro --replicas 1
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- stx export html ---
        st_write(bs.sub, "stx export html [PATH]", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Export a StreamTeX project to static HTML. Run by the generated
            entrypoint at container start-up (dual/static-only serve modes;
            no longer at image build time), or standalone for offline archives.
        """)
        st_space("v", 1)

        show_code("""\
            stx export html .
            stx export html --output /app/static-html/ ./manuals/stx_manual_intro
            stx export html --lang fr .                  # <html lang="fr">
            STX_LANG=fr stx export html --suffix -fr .   # env drives blocks AND <html lang>; writes <project>-fr.html
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation("""\
            `--lang` sets the `<html lang>` attribute of the export
            (resolution: `--lang` > `$STX_LANG` > `en`); `--suffix` is
            appended to the output basename so one directory can hold every
            language. See the *Multilingual Documents* chapter of the
            advanced manual for the one-export-per-language loop.
        """)
        st_space("v", 2)

        # --- stx deploy env-sync ---
        st_write(bs.sub, "stx deploy env-sync", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Sync environment variables to deployed services.
            Reads from .stx-deploy.env and pushes to Coolify.
        """)
        st_space("v", 1)

        show_code("""\
            stx deploy env-sync
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # ============================================================
        # Validation and running (0.7.38 / 0.7.39)
        # ============================================================
        st_space("v", 2)
        st_write(bs.heading, "Validation & Running", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- stx validate ---
        st_write(bs.sub, "stx validate", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Validates the current project: packs, components, design
            systems, kits, the project rules of stx.toml, and — since
            0.7.38 — version coherence (.stx-version / pyproject.toml /
            uv.lock), hygiene (git conflict markers: error; deprecated
            stx.toml sections such as `[patterns]`: warning) and, since
            0.7.40, facts whose source has moved on (warning).
            Exit codes: 0 clean, 1 warnings, 2 errors.
        """)
        st_space("v", 1)

        show_code("""\
            stx validate                          # every check except the build
            stx validate --strict                 # warnings promoted to errors (exit 2)
            stx validate --build                  # + real build() of every block
            stx validate --build --book book.py   # only this book (repeatable)
            stx validate --build --timeout 300    # seconds per book (default 180)
            stx validate --build --published      # against the PUBLISHED streamtex
            stx validate --build --snapshot before.json   # HTML fingerprint per block
            stx validate --build --against before.json    # blocks that render differently
        """, language="bash", line_numbers=False)
        st_space("v", 2)

        # --- pre-commit hooks of new projects ---
        st_write(bs.sub, "Pre-commit hooks of new projects", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            stx project new writes a .pre-commit-config.yaml with ruff and,
            since 0.7.38, two hooks of pre-commit-hooks: check-merge-conflict
            (no `<<<<<<<` / `>>>>>>>` marker reaches a commit) and check-toml.
            stx validate reports the same conflict markers as errors in an
            existing project.
        """)
        st_space("v", 1)

        show_code("""\
            repos:
              - repo: https://github.com/astral-sh/ruff-pre-commit
                rev: v0.11.2
                hooks:
                  - id: ruff
                    args: [--fix, --exit-non-zero-on-fix]
              # A merge that leaves <<<<<<< / >>>>>>> markers in 46 files was once
              # committed and deployed; these hooks stop it before the commit.
              - repo: https://github.com/pre-commit/pre-commit-hooks
                rev: v5.0.0
                hooks:
                  - id: check-merge-conflict
                  - id: check-toml
        """, language="yaml", line_numbers=False)
        st_space("v", 2)

        # --- stx run --set (0.7.39) ---
        st_write(bs.sub, "stx run — several documents (--set)", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            stx run [BOOK] runs one project (shortcut for streamlit run).
            With --set it runs every document declared in the stx.toml
            `[[run.documents]]` tables (id, book, port) together, in the
            background, each one receiving `$STX_URL_<ID>` for every
            document. State and logs live in .stx_run/ next to stx.toml.
            stx run without these options is unchanged.
        """)
        st_space("v", 1)

        show_code("""\
            stx run --set                          # start every declared document
            stx run --set --doc survey             # only this document id
            stx run --list                         # declared documents and their state
            stx run --kill                         # stop them (or --doc ones)
            stx run --set --fresh                  # stop, clear the page cache, start again
            stx run --set --lang fr                # URLs carry ?lang=fr
            stx run --set --ports-offset 100       # add 100 to every declared port
            stx run --set --open --chrome-profile ~/.stx-projection-chrome
        """, language="bash", line_numbers=False)
        st_space("v", 1)

        show_explanation("""\
            --chrome-profile DIR opens the documents in a dedicated Chrome
            profile allowed to autoplay media (projection). See the intro
            manual (CLI Quick Start) for the `[[run.documents]]` declaration.
        """)
        st_space("v", 2)

