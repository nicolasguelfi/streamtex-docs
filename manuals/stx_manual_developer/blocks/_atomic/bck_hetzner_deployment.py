from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Hetzner/Coolify deployment styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Hetzner/Coolify Architecture",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- coolify.py module overview ---
        st_write(bs.sub, "coolify.py module overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The ``streamtex.cli.coolify`` module is the **shared foundation** for all
            Hetzner/Coolify deployment operations. It is used by both the Python CLI
            commands (``stx deploy``) and the Claude agent commands.

            The module provides:

            - **CoolifyClient** — HTTP client wrapping the Coolify v4 REST API
            - **DeployState** — typed schema for ``.stx-deploy.json`` state files
            - **Constants** — single source of truth for SSH paths, server types, ports
            - **Utility functions** — ``load_typed_state()``, ``save_typed_state()``,
              ``_parse_env_file()``
        """)
        st_space("v", 2)

        # --- Constants ---
        st_write(bs.sub, "Constants (single source of truth)", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# streamtex/cli/coolify.py — constants
DEFAULT_SSH_KEY_PATH = "~/.ssh/hetzner_streamtex"
DEFAULT_SSH_KEY_NAME = "streamtex-deploy"
DEFAULT_SSH_USER = "deploy"
DEFAULT_SERVER_TYPE = "cax21"       # ARM, 4 vCPU, 8 GB RAM
DEFAULT_SERVER_LOCATION = "fsn1"    # Falkenstein, Germany
DEFAULT_SERVER_IMAGE = "ubuntu-24.04"
DEFAULT_SERVER_NAME = "streamtex-prod"
DEFAULT_DEPLOY_TIMEOUT = 300        # seconds
STREAMLIT_PORT = 8501
COOLIFY_DASHBOARD_PORT = 8000""", language="python")
        st_space("v", 1)

        show_explanation("""\
            These constants are imported by CLI commands, Claude profiles, and tests.
            Changing a value here propagates everywhere — no more hardcoded strings
            scattered across deploy scripts.
        """)
        st_space("v", 2)

        # --- DeployState schema ---
        st_write(bs.sub, "DeployState schema", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            ``DeployState`` is a typed dataclass that maps to ``.stx-deploy.json``.
            It is built up **incrementally** as each deployment phase completes.
            All fields are optional (``None`` by default).
        """)
        st_space("v", 1)

        show_code("""\
@dataclass
class DeployState:
    version: str = "2.0"
    server: ServerInfo | None = None        # Hetzner server details
    domain: DomainInfo | None = None        # Domain + registrar
    coolify: CoolifyInfo | None = None      # Coolify URL, UUIDs
    applications: list[AppEntry] | None = None  # Deployed apps
    phases_completed: dict[str, str] | None = None  # Phase timestamps
    cdn: dict | None = None                 # Cloudflare CDN config
    security: dict | None = None            # Firewall, fail2ban

# Supporting dataclasses:
@dataclass
class ServerInfo:
    name: str = ""
    id: int = 0
    type: str = DEFAULT_SERVER_TYPE    # "cax21"
    location: str = DEFAULT_SERVER_LOCATION  # "fsn1"
    ipv4: str = ""
    ssh_key_path: str = DEFAULT_SSH_KEY_PATH

@dataclass
class AppEntry:
    name: str = ""
    uuid: str = ""           # Coolify application UUID
    subdomain: str = ""      # e.g. "docs-intro"
    url: str = ""            # e.g. "https://docs-intro.streamtex.org"
    folder: str = ""         # e.g. "manuals/stx_manual_intro"
    branch: str = "main"
    deployed_at: str = ""    # ISO timestamp
    replicas: int = 1        # Number of containers (1 = no replicas)
    replica_uuids: list[str] | None = None  # UUIDs of secondary replicas
    serve_mode: str = "streamlit-only"  # dual, static-only, streamlit-only

    @property
    def all_uuids(self) -> list[str]:
        \"\"\"Primary UUID + all replica UUIDs.\"\"\"
        ...""", language="python")
        st_space("v", 1)

        show_details("""\
            The ``to_dict()`` method serializes to plain dict for JSON storage,
            skipping falsy values to keep the file compact. ``from_dict()`` handles
            both v1 (legacy) and v2 formats, filtering unknown keys via
            ``__dataclass_fields__`` to stay forward-compatible.
        """)
        st_space("v", 2)

        # --- CoolifyClient API surface ---
        st_write(bs.sub, "CoolifyClient API surface", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            ``CoolifyClient`` wraps the Coolify v4 REST API using only ``urllib``
            (no external HTTP dependency). It is constructed from credentials
            found in ``.stx-deploy.env``, environment variables, or
            ``.stx-deploy.json``.
        """)
        st_space("v", 1)

        show_code("""\
client = CoolifyClient.from_env()       # auto-discover credentials

# --- Application lifecycle ---
apps = client.list_apps()               # GET /api/v1/applications
app  = client.get_app("uuid")           # GET /api/v1/applications/{uuid}
resp = client.create_app(               # POST /api/v1/applications
    project_uuid="...", server_uuid="...",
    name="docs-intro", repository="owner/repo",
)
client.delete_app("uuid")              # DELETE /api/v1/applications/{uuid}

# --- Deployments ---
result = client.rebuild("uuid")         # POST .../start (full rebuild)
result = client.restart("uuid")         # POST .../restart (container only)
result = client.stop("uuid")            # POST .../stop
ok = client.wait_healthy("uuid", timeout=300)  # poll until healthy

# --- Configuration ---
client.set_env_var("uuid", "FOLDER", "manuals/stx_manual_intro")
client.set_fqdn("uuid", "https://docs-intro.streamtex.org")

# --- Scaling (replicas) ---
app = client.scale_app(app_entry, 3, project_uuid, server_uuid)  # scale to 3
results = client.rebuild_all_replicas(app_entry)   # rebuild primary + replicas
results = client.restart_all_replicas(app_entry)   # restart primary + replicas

# --- Diagnostics ---
valid = client.verify_token()           # True if token works""", language="python")
        st_space("v", 1)

        show_details("""\
            **rebuild vs restart**: ``rebuild()`` calls the ``/start`` endpoint which
            triggers a full pipeline — git pull, Docker build, PyPI install. Use this
            after code changes. ``restart()`` only restarts the existing container —
            use for env var or config changes that do not require a new image.

            Both return a ``DeployResult`` dataclass with ``success``, ``message``,
            and ``deployment_uuid`` fields.
        """)
        st_space("v", 2)

        # --- deploy_cmd.py command structure ---
        st_write(bs.sub, "deploy_cmd.py command structure", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The ``stx deploy`` CLI commands live in ``streamtex/cli/deploy_cmd.py``
            and are organized around shared helpers from ``coolify.py``:

            ```
            stx deploy status        # list apps + health status
            stx deploy rebuild       # full rebuild (all or specific app)
            stx deploy restart       # quick restart
            stx deploy logs          # fetch recent logs
            stx deploy setup         # interactive first-time setup
            ```

            Each command follows the same pattern:

            1. Load credentials via ``CoolifyClient.from_env()``
            2. Load state via ``load_typed_state()``
            3. Perform API calls
            4. Update state via ``save_typed_state()``
        """)
        st_space("v", 1)

        show_code("""\
# Typical command pattern (simplified)
def deploy_rebuild(app_name: str | None = None):
    client = CoolifyClient.from_env()
    state = load_typed_state()

    # Find target app(s) from state
    targets = state.applications or []
    if app_name:
        targets = [a for a in targets if a.name == app_name]

    for app in targets:
        result = client.rebuild(app.uuid)
        if result.success:
            ok = client.wait_healthy(app.uuid, timeout=300)
            print(f"{app.name}: {'healthy' if ok else 'timeout'}")""", language="python")
        st_space("v", 2)

        # --- State file lifecycle ---
        st_write(bs.sub, "State file lifecycle", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Two state files drive the deployment workflow:

            **``.stx-deploy.env``** — credentials (never committed to git):
            ```
            COOLIFY_URL=https://coolify.streamtex.org
            COOLIFY_API_TOKEN=...
            HETZNER_API_TOKEN=...
            ```

            **``.stx-deploy.json``** — infrastructure state (committed to git):
            ```json
            {
              "version": "2.0",
              "infrastructure": {
                "server": { "name": "streamtex-prod", "ipv4": "138.199.148.59" },
                "coolify": { "url": "https://coolify.streamtex.org" },
                "domain": { "base": "streamtex.org" }
              },
              "applications": [ ... ],
              "phases_completed": { "provision": "2026-03-20T10:00:00" }
            }
            ```

            The state file is updated after each deployment phase.
            ``load_typed_state()`` and ``save_typed_state()`` handle
            serialization through the ``DeployState`` dataclass.
        """)
        st_space("v", 1)

        show_details("""\
            The ``.stx-deploy.env`` file is searched in three locations:
            current directory, parent directory, then environment variables.
            This supports both running from the workspace root (``streamtex-dev/``)
            and from individual repos (``streamtex-docs/``).
        """)
        st_space("v", 2)

        # --- GitHub Actions integration ---
        st_write(bs.sub, "GitHub Actions integration", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The ``hetzner-deploy.yml`` workflow triggers on pushes to ``main``
            and calls the Coolify API to rebuild all services:
        """)
        st_space("v", 1)

        show_code("""\
# .github/workflows/hetzner-deploy.yml (simplified)
name: Deploy to Hetzner/Coolify
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy all services
        env:
          COOLIFY_URL: https://coolify.streamtex.org
          COOLIFY_API_TOKEN: ${{ secrets.COOLIFY_API_TOKEN }}
        run: |
          # For each application UUID, trigger a rebuild
          for UUID in uuid1 uuid2 uuid3; do
            curl -X POST "$COOLIFY_URL/api/v1/applications/$UUID/start" \\
              -H "Authorization: Bearer $COOLIFY_API_TOKEN" \\
              -H "Content-Type: application/json"
          done""", language="yaml")
        st_space("v", 1)

        show_details("""\
            The ``COOLIFY_API_TOKEN`` GitHub secret must be set from
            ``streamtex/.env`` (the non-expiring manual key), NOT from
            ``~/.render/cli.yaml`` which contains an auto-refreshing key.
            The workflow deploys all 7 services: docs, docs-intro,
            docs-advanced, docs-deploy, docs-developer, docs-ai, and docs-ce.
        """)
        st_space("v", 2)

        # --- Gotchas table ---
        st_write(bs.sub, "Hetzner/Coolify gotchas", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Gotcha")
            with g.cell(): st_write(s.bold + s.large, "Solution")
            with g.cell():
                st_write(s.large, "rebuild() vs restart()")
            with g.cell():
                st_write(s.large,
                         "rebuild = /start (full Docker build). "
                         "restart = /restart (reuse existing image). "
                         "Use rebuild after code changes, restart for env vars only.")
            with g.cell():
                st_write(s.large, "PyPI before deploy")
            with g.cell():
                st_write(s.large,
                         "Coolify installs from PyPI, not local. "
                         "ALWAYS publish to PyPI before triggering a rebuild.")
            with g.cell():
                st_write(s.large, "API token source")
            with g.cell():
                st_write(s.large,
                         "Use the non-expiring key from streamtex/.env, "
                         "never the auto-refreshing key from ~/.render/cli.yaml.")
            with g.cell():
                st_write(s.large, "ARM architecture (cax21)")
            with g.cell():
                st_write(s.large,
                         "Docker images must be ARM-compatible. "
                         "python:3.13-slim works natively on ARM.")
