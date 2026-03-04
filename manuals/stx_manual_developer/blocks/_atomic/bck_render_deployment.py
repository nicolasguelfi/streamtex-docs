from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Render deployment styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Render Deployment",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Architecture ---
        st_write(bs.sub, "Architecture overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each StreamTeX manual is deployed as a **separate Render web service**,
            all sharing the **same Docker image** but with a different FOLDER env var.

            ```
            render.yaml (5 services)
              │
              ├── streamtex          FOLDER=manuals/stx_manuals_collection   :8501
              ├── streamtex-intro    FOLDER=manuals/stx_manual_intro         :8501
              ├── streamtex-advanced FOLDER=manuals/stx_manual_advanced      :8501
              ├── streamtex-deploy   FOLDER=manuals/stx_manual_deploy        :8501
              └── streamtex-developer FOLDER=manuals/stx_manual_developer    :8501
            ```

            One Dockerfile, one repo, five services. The FOLDER variable is the
            **only difference** between them.
        """)
        st_space("v", 2)

        # --- Dockerfile ---
        st_write(bs.sub, "Dockerfile", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
FROM python:3.13-slim
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Install dependencies from PyPI (not local editable)
# --no-sources ignores [tool.uv.sources] → resolves from PyPI
# sed strips the sources section so "uv run" won't re-resolve
COPY pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev && \\
    sed -i '/^\\[tool\\.uv\\.sources\\]/,/^$/d' pyproject.toml

# Copy all manuals (shared-blocks needed by LazyBlockRegistry)
COPY manuals/ ./manuals/

# FOLDER is set at runtime by Render envVars
ENV FOLDER="manuals/stx_manual_intro"

EXPOSE 8501
ENTRYPOINT ["/bin/sh", "-c", \\
  "cd /app/${FOLDER} && exec uv run streamlit run book.py \\
   --server.port=8501 --server.address=0.0.0.0"]""", language="dockerfile")
        st_space("v", 1)

        show_explanation("""\
            Key points:

            - **--no-sources** + **sed**: same problem as CI — the local editable
              path ../streamtex doesn't exist in Docker. Two-step fix: ignore during
              sync, then strip from pyproject.toml so uv run doesn't re-check.
            - **ENV FOLDER default**: if no FOLDER is set, defaults to intro.
              This is a safety net — in production, Render always sets FOLDER.
            - **All manuals are copied**: even if only one runs, shared-blocks
              must be available for LazyBlockRegistry cross-references.
        """)
        st_space("v", 2)

        # --- render.yaml ---
        st_write(bs.sub, "render.yaml", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
services:
  - type: web
    name: streamtex-developer      # Service name on Render
    runtime: docker
    repo: https://github.com/nicolasguelfi/streamtex-docs
    branch: main
    plan: free
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: FOLDER
        value: manuals/stx_manual_developer
      - key: STX_PASSWORD
        value: changeme
    healthCheckPath: /_stcore/health""", language="yaml")
        st_space("v", 1)

        show_explanation("""\
            The render.yaml is a **declarative blueprint**: it describes the desired
            state of all services. However, it does NOT create services automatically.
            You must create them via the Render Dashboard or the API (see below).
        """)
        st_space("v", 2)

        # --- Creating a service ---
        st_write(bs.sub, "Creating a new service", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            To add a new manual to Render, three steps are required:

            **Step 1** — Add the service to render.yaml (declarative config).

            **Step 2** — Create the service via the Render API.
            The Render CLI (v2) cannot create services. Use curl:
        """)
        st_space("v", 1)

        show_code("""\
# The API key is in ~/.render/cli.yaml (field: api.key)
RENDER_KEY="rnd_..."
OWNER_ID="tea-..."   # from: render services --output json

curl -X POST "https://api.render.com/v1/services" \\
  -H "Authorization: Bearer $RENDER_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "autoDeploy": "yes",
    "branch": "main",
    "name": "streamtex-NEW",
    "ownerId": "'$OWNER_ID'",
    "repo": "https://github.com/nicolasguelfi/streamtex-docs",
    "type": "web_service",
    "serviceDetails": {
      "env": "docker",
      "envSpecificDetails": {
        "dockerContext": ".",
        "dockerfilePath": "./Dockerfile"
      },
      "plan": "free",
      "region": "oregon",
      "runtime": "docker"
    }
  }'""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            **Step 3** — Set env vars separately (the create API ignores envVars
            in serviceDetails):
        """)
        st_space("v", 1)

        show_code("""\
# Get the service ID from the create response
SVC_ID="srv-..."

curl -X PUT "https://api.render.com/v1/services/$SVC_ID/env-vars" \\
  -H "Authorization: Bearer $RENDER_KEY" \\
  -H "Content-Type: application/json" \\
  -d '[
    {"key": "FOLDER", "value": "manuals/stx_manual_NEW"},
    {"key": "STX_PASSWORD", "value": "changeme"}
  ]'""", language="bash")
        st_space("v", 2)

        # --- Gotchas ---
        st_write(bs.sub, "Render gotchas", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Gotcha")
            with g.cell(): st_write(s.bold + s.large, "Solution")
            with g.cell():
                st_write(s.large, "New service shows wrong manual")
            with g.cell():
                st_write(s.large,
                         "FOLDER env var not set — must be created via "
                         "separate /env-vars API call after service creation")
            with g.cell():
                st_write(s.large, "render.yaml doesn't create services")
            with g.cell():
                st_write(s.large,
                         "It's declarative only — create via API or Dashboard, "
                         "then render.yaml keeps config in sync with git")
            with g.cell():
                st_write(s.large, "API key location")
            with g.cell():
                st_write(s.large,
                         "~/.render/cli.yaml → api.key field "
                         "(not $RENDER_API_KEY which may be empty)")
            with g.cell():
                st_write(s.large, "Free plan: service sleeps after 15 min")
            with g.cell():
                st_write(s.large,
                         "First visit takes ~30s to wake up — this is normal")
        st_space("v", 2)

        # --- Useful commands ---
        st_write(bs.sub, "Useful Render CLI commands", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# List all services
render services --output json

# Check deploy status
render deploys list --service-id srv-... --output json

# View logs
render logs --service-id srv-... --tail 50

# Trigger a redeploy (via API — CLI doesn't support this)
curl -X POST "https://api.render.com/v1/services/srv-.../deploys" \\
  -H "Authorization: Bearer $RENDER_KEY" """, language="bash")
        st_space("v", 2)

        show_details("""\
            The collection hub service also needs env vars for each manual URL
            (STX_URL_TEST_INTRO, STX_URL_TEST_ADVANCED, etc.) so that the
            navigation cards point to the correct Render URLs in production
            instead of localhost.
        """)
