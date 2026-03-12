# StreamTeX Deployment -- Cheatsheet

## Quick Reference

```bash
# Pre-deployment checks
stx deploy preflight .
stx deploy preflight . --skip-tests --skip-lint

# Docker build and run
stx deploy docker .
stx deploy docker . --port 8502 --tag my-project
stx deploy docker . --build-only

# Render — generate render.yaml
stx deploy render .
stx deploy render . --name my-service --branch main --plan free
stx deploy render . --multi                    # one service per manual
stx deploy render . --env STX_PASSWORD=secret

# Render — status and env sync
stx deploy status render
stx deploy status render streamtex-intro
stx deploy env-sync --path .
stx deploy env-sync --dry-run

# HuggingFace Spaces
stx deploy huggingface . --space https://huggingface.co/spaces/user/repo
stx deploy huggingface . --space <url> --skip-push

# PyPI publishing
stx publish check .
stx publish check . --skip-tests --skip-lint
stx publish pypi .
stx publish pypi . --test                      # publish to TestPyPI

# Cache warming
stx cache warmup .
```

---

## 1. Pre-Deployment Checklist

### stx deploy preflight

Runs 9 checks on the project directory and prints a pass/warn/fail table.

```bash
stx deploy preflight .
stx deploy preflight . --skip-tests
stx deploy preflight . --skip-tests --skip-lint
```

| # | Check | Pass condition |
|---|-------|---------------|
| 1 | `book.py` | File exists in project root |
| 2 | `enableStaticServing` | `.streamlit/config.toml` contains `enableStaticServing = true` |
| 3 | `pyproject.toml` | Valid TOML with `streamtex` in `[project.dependencies]` |
| 4 | `git clean` | No uncommitted changes (warn if dirty, warn if not a git repo) |
| 5 | `sensitive files` | No `.env`, `credentials*`, `*.key`, `*.pem` files found |
| 6 | `static/` | Directory exists (warn if missing) |
| 7 | `Dockerfile` | File exists (warn if missing) |
| 8 | `tests` | `uv run pytest tests/ -q` passes (skippable with `--skip-tests`) |
| 9 | `lint` | `uv run ruff check .` passes (skippable with `--skip-lint`) |

### stx publish check — PyPI readiness

Runs 11 checks specific to package publishing. See [Section 5](#5-pypi-publishing) for details.

---

## 2. Docker Deployment

### stx deploy docker — full command

```bash
stx deploy docker PATH [--port PORT] [--tag TAG] [--build-only]
```

What it does:
1. Runs preflight checks (tests and lint skipped for speed).
2. Generates a `Dockerfile` if missing.
3. Computes the image tag from the directory name (or uses `--tag`).
4. Runs `docker build -t TAG PATH`.
5. Runs `docker run -p PORT:8501 TAG` (unless `--build-only`).

### Generated Dockerfile anatomy (for single projects)

The `stx deploy docker` command generates this Dockerfile when none exists:

```dockerfile
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true UV_LINK_MODE=copy
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
ENV PORT=8501
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["uv", "run", "streamlit", "run", "book.py", \
            "--server.port=8501", "--server.address=0.0.0.0"]
```

Key points:
- **Base image**: `python:3.13-slim` (minimal footprint).
- **uv**: Copied from `ghcr.io/astral-sh/uv:latest` (no pip needed).
- **Dependency caching**: `pyproject.toml` + `uv.lock` copied first, then `uv sync --frozen --no-dev` installs dependencies in a cached layer.
- **Health check**: Streamlit's built-in `/_stcore/health` endpoint.

### Build and run locally

```bash
# With stx CLI
stx deploy docker .
stx deploy docker . --port 8502 --tag my-app --build-only

# Manual Docker commands
docker build -t my-project .
docker run -p 8501:8501 my-project
docker run -p 8502:8501 -e STX_PASSWORD=secret my-project
```

### Environment variables in Docker

Pass environment variables at runtime with `-e`:

```bash
docker run -p 8501:8501 \
  -e STX_PASSWORD=mysecret \
  -e FOLDER=manuals/stx_manual_intro \
  my-project
```

---

## 3. Render.com Deployment

### stx deploy render — generate render.yaml

```bash
stx deploy render PATH [--name NAME] [--branch BRANCH] [--plan PLAN]
                       [--env KEY=VALUE ...] [--multi]
```

**Single service mode** (default):
```bash
stx deploy render . --name my-app
```

**Multi-service mode** (one service per manual in `manuals/`):
```bash
stx deploy render . --multi
```

What it does:
1. Detects the git remote origin URL (SSH is auto-converted to HTTPS).
2. Generates a `Dockerfile` if missing.
3. Discovers `manuals/stx_manual_*` and `manuals/stx_manuals_*` directories (in `--multi` mode).
4. Derives service names: `manuals/stx_manual_intro` becomes `streamtex-intro`.
5. Writes `render.yaml` with service definitions.
6. Adds `STX_PASSWORD=changeme` if not specified via `--env`.

### Service creation via Render API

**render.yaml is declarative only** -- it does NOT create services on Render. To create a service:

```bash
# Use the Render API directly (POST /v1/services)
curl -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "web_service",
    "name": "my-service",
    "ownerId": "tea-d2adlm49c44c738ob46g",
    "repo": "https://github.com/user/repo",
    "branch": "main",
    "plan": "free",
    "runtime": "docker",
    "dockerfilePath": "./Dockerfile",
    "dockerContext": ".",
    "healthCheckPath": "/_stcore/health"
  }'
```

**Render CLI v2 cannot create services** -- you must use the API directly.

### Environment variables on Render

Env vars MUST be set separately via the API. The service creation endpoint ignores them.

```bash
# Set env vars (PUT replaces ALL env vars for the service)
curl -X PUT "https://api.render.com/v1/services/SERVICE_ID/env-vars" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '[
    {"key": "FOLDER", "value": "manuals/stx_manual_intro"},
    {"key": "STX_PASSWORD", "value": ""}
  ]'
```

### API key location

The Render API key is read from `~/.render/cli.yaml`:

```yaml
api-key: rnd_xxxxxxxxxxxxx
owner-id: tea-d2adlm49c44c738ob46g
```

The `stx deploy env-sync` command reads this file automatically. The `$RENDER_API_KEY` environment variable is used by CI workflows (GitHub secret).

### Owner ID

```
tea-d2adlm49c44c738ob46g
```

### stx deploy status — health monitoring

```bash
stx deploy status render                      # probe all services from render.yaml
stx deploy status render streamtex-intro      # probe a specific service
stx deploy status huggingface                 # probe HF Space from 'hf' git remote
stx deploy status huggingface user/repo       # probe a specific HF Space
```

Probes the service URL with HTTP HEAD. Returns one of:
- **live** -- HTTP 2xx
- **sleep** -- HTTP 502/503 or timeout (service may be waking)
- **down** -- HTTP 404 (service not found)
- **error** -- other HTTP error or network issue

For HuggingFace, uses the HF API (`/api/spaces/owner/repo`) and maps runtime stage (RUNNING, SLEEPING, PAUSED, BUILDING) to status.

### stx deploy env-sync — sync env vars to Render

```bash
stx deploy env-sync --path .                  # sync all services
stx deploy env-sync --path . --service streamtex-intro  # sync one service
stx deploy env-sync --path . --dry-run        # preview changes only
```

What it does:
1. Parses `render.yaml` to extract desired env vars per service.
2. Reads API key from `~/.render/cli.yaml`.
3. Resolves service names to Render service IDs via `GET /services`.
4. Fetches current env vars from `GET /services/{id}/env-vars`.
5. Computes a diff and displays a change table.
6. Applies changes via `PUT /services/{id}/env-vars` (unless `--dry-run`).
7. Optionally triggers a redeploy for updated services.

---

## 4. HuggingFace Spaces

### stx deploy huggingface — full command

```bash
stx deploy huggingface PATH --space SPACE_URL [--title TITLE] [--emoji EMOJI] [--skip-push]
```

What it does:
1. Runs preflight checks (tests and lint skipped).
2. Verifies `git-lfs` is installed (warns if not).
3. Verifies `huggingface-cli` is installed and authenticated (warns if not).
4. Generates a `Dockerfile` if missing.
5. Sets up `.gitattributes` with LFS patterns for binary files (images, fonts, media).
6. Generates/updates `README.md` with HF Spaces YAML front-matter.
7. Adds/updates an `hf` git remote pointing to the Space.
8. Commits and pushes to the `hf` remote (unless `--skip-push`).

### README.md format for HF Spaces

The command generates this YAML front-matter:

```yaml
---
title: My Project
emoji: <emoji>
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8501
pinned: false
---
```

### LFS patterns

These file types are automatically tracked via `.gitattributes`:

```
*.png, *.jpg, *.jpeg, *.gif, *.bmp, *.svg, *.webp
*.mp4, *.mp3, *.wav, *.ogg
*.pdf, *.zip, *.tar.gz
*.woff, *.woff2, *.ttf, *.otf
```

### Free tier limitations

- HF free tier: 16 GB RAM, 2 vCPU, limited storage.
- Spaces go to sleep after inactivity -- first load will be slow.
- Docker SDK builds are slower than Gradio/Streamlit SDK.

---

## 5. PyPI Publishing

### stx publish check — pre-publish validation

```bash
stx publish check .
stx publish check . --skip-tests
stx publish check . --skip-tests --skip-lint
```

Runs 11 checks:

| # | Check | What it verifies |
|---|-------|-----------------|
| 1 | `pyproject.toml` | Valid TOML, parseable |
| 2 | `version` | `project.version` field present |
| 3 | `README.md` | File exists |
| 4 | `LICENSE` | `LICENSE`, `LICENSE.txt`, or `LICENSE.md` exists |
| 5 | `__version__` | `streamtex/__init__.py` version matches `pyproject.toml` |
| 6 | `no dev deps` | No `pytest`, `ruff`, `rich`, `click` in `[project.dependencies]` |
| 7 | `tests` | `uv run pytest tests/ -q` passes (skippable) |
| 8 | `lint` | `uv run ruff check .` passes (skippable) |
| 9 | `build` | `uv build` succeeds |
| 10 | `dist files` | Both `.whl` and `.tar.gz` exist in `dist/` |
| 11 | `README links` | No relative links in README (they break on PyPI) |

### stx publish pypi — build and upload

```bash
stx publish pypi .
stx publish pypi . --test                     # upload to TestPyPI
stx publish pypi . --skip-tests --skip-lint
```

What it does:
1. Runs all publish checks (fails fast on any failure).
2. Cleans `dist/` directory.
3. Builds with `uv build`.
4. Loads `UV_PUBLISH_TOKEN` from `$UV_PUBLISH_TOKEN` env var, or from `.env` file (`PYPI_TOKEN=...`).
5. Uploads with `uv publish` (or `uv publish --index testpypi` for TestPyPI).

### Version management

Both files must have the same version:
- `pyproject.toml` -> `[project] version = "X.Y.Z"`
- `streamtex/__init__.py` -> `__version__ = "X.Y.Z"`

The `stx publish check` command verifies they match.

### Token configuration

Set the PyPI API token in one of two ways:

```bash
# Option 1: environment variable
export UV_PUBLISH_TOKEN=pypi-xxxxxxxxxx

# Option 2: .env file in project root
echo "PYPI_TOKEN=pypi-xxxxxxxxxx" >> .env
```

The `.env` file is only read if `UV_PUBLISH_TOKEN` is not already set.

---

## 6. Deploy Discipline (CRITICAL)

### ALWAYS publish to PyPI BEFORE deploying to Render

Render installs `streamtex` from PyPI, not from your local machine. If your docs use features from a new library version, that version MUST be published on PyPI first.

### Correct deployment sequence

```
1. Make library changes in streamtex/
2. Bump version in pyproject.toml + __init__.py
3. Run tests: uv run pytest tests/ -v
4. Publish to PyPI: stx publish pypi .
5. Wait for PyPI to process (usually < 1 minute)
6. Push docs changes to GitHub
7. Trigger Render deploy (manual or auto)
```

### What stx claude update --all does (and does NOT do)

`stx claude update --all` syncs Claude AI profiles only. It does NOT:
- Publish to PyPI
- Deploy to Render
- Trigger any CI/CD

Related profile commands:
```bash
stx claude check         # verify profiles are in sync
stx claude update --all  # sync all profiles
stx claude diff .        # show profile differences
```

---

## 7. CI/CD -- GitHub Actions

### streamtex library pipeline

File: `streamtex/.github/workflows/ci.yml`

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      lfs: true
  - uses: astral-sh/setup-uv@v4
  - run: uv sync --frozen
  - run: uv run ruff check streamtex/
  - run: uv run pytest tests/ -v
```

Key: Uses `--frozen` because the library has no `[tool.uv.sources]` overrides.

### streamtex-docs pipeline

File: `streamtex-docs/.github/workflows/ci.yml`

```yaml
env:
  UV_NO_SOURCES: "1"    # Ignores [tool.uv.sources] for ALL uv commands
steps:
  - uses: actions/checkout@v4
  - uses: astral-sh/setup-uv@v4
  - run: uv python install
  - run: uv sync           # NOT --frozen (lock file encodes local path)
```

Key: `UV_NO_SOURCES=1` is set at job level so all `uv` commands ignore the `[tool.uv.sources]` section which references `../streamtex` (a path that only exists locally).

**NEVER use `--frozen` in streamtex-docs CI** -- the lock file encodes the local editable path and will fail in CI.

### The 5 structural checks (streamtex-docs)

| # | Check | What it verifies |
|---|-------|-----------------|
| 1 | Verify streamtex import | `import streamtex` succeeds with PyPI version |
| 2 | API compatibility | All `st_*()` calls and class constructors in blocks use parameters that exist in the installed version |
| 3 | Block structure | All `blocks/**/*.py` files have valid syntax and a `build()` function |
| 4 | Composite-to-atomic links | `load_atomic_block("name")` references resolve to existing `_atomic/name.py` files |
| 5 | book.py files | All `manuals/**/book.py` files parse without syntax errors |

### Projects pipeline

All projects in `projects/` use:
```yaml
env:
  UV_NO_SOURCES: "1"
steps:
  - run: uv sync          # not --frozen
  - run: uv run ruff check .
  - run: uv run python -c "import streamtex"
```

### When to use --frozen vs not

| Context | Use `--frozen`? | Why |
|---------|----------------|-----|
| streamtex library CI | Yes | No local source overrides |
| streamtex-docs CI | No | Lock file has local path from `[tool.uv.sources]` |
| Projects CI | No | Same reason (local source overrides) |
| Docker (single project) | Yes | No `[tool.uv.sources]` in project |
| Docker (streamtex-docs) | No, use `--no-sources` | Must ignore local path references |

### Render deploy workflow

File: `streamtex-docs/.github/workflows/render-deploy.yml`

The `push` trigger is **disabled** (free tier limits). Deploys are manual only:

```bash
gh workflow run render-deploy.yml -R nicolasguelfi/streamtex-docs
```

The workflow:
1. Extracts the `{service_name: folder}` mapping from `render.yaml`.
2. Detects which files changed (if push trigger, compares `before..after`).
3. Shared file changes (Dockerfile, pyproject.toml, shared-blocks) trigger ALL services.
4. Manual folder changes trigger only the affected service.
5. `workflow_dispatch` (manual trigger) always deploys ALL services.
6. Resolves service IDs via Render API and triggers deploys via `POST /services/{id}/deploys`.

Required secret: `RENDER_API_KEY` (set in GitHub repo settings).

---

## 8. Render Services Reference

### Current services (6 total)

| Name | ID | URL | FOLDER |
|------|----|-----|--------|
| streamtex | srv-d6f23uhaae7s73c14di0 | https://streamtex.onrender.com | manuals/stx_manuals_collection |
| streamtex-intro | srv-d6f2bmhaae7s73c18qng | https://streamtex-intro.onrender.com | manuals/stx_manual_intro |
| streamtex-advanced | srv-d6f2bmhaae7s73c18qn0 | https://streamtex-advanced.onrender.com | manuals/stx_manual_advanced |
| streamtex-deploy | srv-d6f2bmhaae7s73c18qo0 | https://streamtex-deploy.onrender.com | manuals/stx_manual_deploy |
| streamtex-developer | srv-d6j8gkhdrdic73dum3u0 | https://streamtex-developer.onrender.com | manuals/stx_manual_developer |
| streamtex-ai | srv-d6mndltm5p6s73fuijt0 | https://streamtex-ai.onrender.com | manuals/stx_manual_ai |

### Collection hub env vars

The collection hub service (`streamtex`) needs `STX_URL_TEST_*` env vars pointing to the other services:

```yaml
envVars:
  - key: FOLDER
    value: manuals/stx_manuals_collection
  - key: STX_URL_TEST_INTRO
    value: https://streamtex-intro.onrender.com
  - key: STX_URL_TEST_ADVANCED
    value: https://streamtex-advanced.onrender.com
  - key: STX_URL_TEST_DEPLOY
    value: https://streamtex-deploy.onrender.com
  - key: STX_URL_TEST_DEVELOPER
    value: https://streamtex-developer.onrender.com
  - key: STX_URL_TEST_AI
    value: https://streamtex-ai.onrender.com
  - key: STX_PASSWORD
    value: ""
```

---

## 9. Claude-Assisted Deployment

### /stx-developer:deploy slash command

The deploy slash command (defined in `streamtex-claude/profiles/library/commands/stx-developer/deploy.md`) guides Claude through the deployment process.

**Arguments**: target (`docker`, `huggingface`, or `gcp`)

**Pre-deployment checks** (all targets):
1. Reads `Dockerfile`, `pyproject.toml`, `.streamlit/config.toml`.
2. Runs `uv run pytest tests/ -v` and aborts on failure.
3. Verifies `streamlit>=1.54.0` in dependencies, `enableStaticServing = true`, and image assets exist.
4. Checks git status for uncommitted changes.

**Docker target**:
```bash
docker build --build-arg FOLDER=<project_path> -t streamtex-app .
docker run -p 8501:8501 streamtex-app
```

**HuggingFace target**:
1. Verifies Dockerfile is HF-compatible (EXPOSE 8501, health check, streamlit run entrypoint).
2. Instructs: create Space (Docker SDK), add `hf` remote, push.

**GCP target**:
1. Checks for Ansible inventory (`inventory.ini`) and playbook (`deploy.yml`).
2. Verifies SSH key configuration.
3. Runs: `ansible-playbook -i inventory.ini deploy.yml`.

### Workflow: Claude runs preflight, builds Docker, deploys

Typical Claude interaction:
```
User: /stx-developer:deploy docker
Claude:
  1. Reads project configuration files
  2. Runs uv run pytest tests/ -v
  3. Verifies requirements
  4. Checks git status
  5. Builds Docker image
  6. Reports status and URL
```

---

## 10. Cache Warming

### stx cache warmup — pre-render pages

```bash
stx cache warmup .
stx cache warmup /path/to/manual
```

What it does:
1. Locates `book.py` in the project directory.
2. Monkey-patches Streamlit for headless execution (no server needed).
3. Executes `book.py` in warmup mode to build the TOC, markers, and search-index cache.
4. Saves cache to `.stx_cache/page_cache.json`.

Output on success:
```
Cache warmup for /path/to/manual
Done in 2.3s -- cache saved to .stx_cache/page_cache.json (45 KB)
```

### Using cache warmup in Dockerfile

The shared Dockerfile runs warmup for every manual during build:

```dockerfile
RUN for dir in manuals/stx_manual_*/; do \
        echo "Warming up cache for $dir ..." && \
        (cd "$dir" && uv run stx cache warmup .) || true; \
    done
```

This ensures the first visitor loads instantly (no cold-start delay for cache generation).

### When to use

- **Docker build**: Always include warmup in your Dockerfile (done automatically in the shared Dockerfile).
- **CI**: Not typically needed (CI does structural checks, not runtime).
- **Local development**: Useful after changing block structure to verify cache generation works.

### Prerequisite

The `st_book()` call in `book.py` must use `paginate=True` for the cache to be generated.

---

## 11. Shared Dockerfile Pattern

### How one Dockerfile serves all 6 manuals

The `streamtex-docs/Dockerfile` builds a single Docker image that can serve any manual. The `FOLDER` environment variable selects which manual to run at container start time.

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Install dependencies (cached layer)
# --no-sources ignores [tool.uv.sources] so uv resolves from PyPI
# Then strip the sources section so "uv run" won't try to re-resolve
COPY pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml

# Copy all manuals
COPY manuals/ ./manuals/

# Default folder (overridden by Render envVars)
ENV FOLDER="manuals/stx_manual_intro"

# Pre-warm cache for every manual
RUN for dir in manuals/stx_manual_*/; do \
        echo "Warming up cache for $dir ..." && \
        (cd "$dir" && uv run stx cache warmup .) || true; \
    done

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/bin/sh", "-c", \
            "cd /app/${FOLDER} && exec uv run streamlit run book.py --server.port=8501 --server.address=0.0.0.0"]
```

### FOLDER env var selection

Each Render service sets a different `FOLDER`:

```
streamtex         -> FOLDER=manuals/stx_manuals_collection
streamtex-intro   -> FOLDER=manuals/stx_manual_intro
streamtex-ai      -> FOLDER=manuals/stx_manual_ai
```

### UV_NO_SOURCES handling in Docker

The Dockerfile uses a two-step approach:

1. `uv sync --no-sources --no-dev` -- installs dependencies from PyPI (ignores the `[tool.uv.sources]` section that points to `../streamtex`).
2. `sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml` -- removes the `[tool.uv.sources]` section entirely so subsequent `uv run` commands do not try to resolve the local path.

This is necessary because `pyproject.toml` in `streamtex-docs` contains:

```toml
[tool.uv.sources]
streamtex = { path = "../streamtex", editable = true }
```

This path only exists in the local development environment, not inside Docker or CI.

### Single-project Dockerfile (for projects/)

Projects in `projects/` use a simpler Dockerfile without `--no-sources` or `FOLDER`:

```dockerfile
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    UV_LINK_MODE=copy
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["uv", "run", "streamlit", "run", "book.py", \
            "--server.port=8501", "--server.address=0.0.0.0"]
```

Key difference: uses `--frozen` (no local source overrides in project `pyproject.toml`).

---

## 12. Troubleshooting

### UV_NO_SOURCES errors in CI/Docker

**Symptom**: `uv sync` fails with "path '../streamtex' does not exist" or similar.

**Cause**: `pyproject.toml` has `[tool.uv.sources]` pointing to a local path that only exists on the developer's machine.

**Fix (CI)**: Set `UV_NO_SOURCES=1` as a job-level environment variable.
```yaml
jobs:
  check:
    env:
      UV_NO_SOURCES: "1"
```

**Fix (Docker)**: Use `--no-sources` flag and strip the section:
```dockerfile
RUN uv sync --no-sources --no-dev && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml
```

**Do NOT use `--frozen`** in streamtex-docs CI or Docker -- the lock file encodes the local path.

### Render service creation fails

**Symptom**: `render.yaml` is pushed but no services appear on Render.

**Cause**: `render.yaml` is declarative only. It describes services but does not create them.

**Fix**: Create services via the Render API:
```bash
curl -X POST "https://api.render.com/v1/services" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "type": "web_service", "name": "...", "ownerId": "tea-d2adlm49c44c738ob46g", ... }'
```

Render CLI v2 does not support service creation.

### Env vars not applied on Render

**Symptom**: Service is created but environment variables are missing or wrong.

**Cause**: The Render service creation API ignores `envVars` in the request body.

**Fix**: Set env vars separately after service creation:
```bash
curl -X PUT "https://api.render.com/v1/services/SERVICE_ID/env-vars" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"key": "FOLDER", "value": "manuals/stx_manual_intro"}]'
```

Or use the CLI command:
```bash
stx deploy env-sync --path .
```

### Health check failures

**Symptom**: Render shows the service as unhealthy or failing health checks.

**Possible causes**:
1. Streamlit is not running on port 8501.
2. `enableStaticServing` is not set in `.streamlit/config.toml`.
3. The `FOLDER` env var points to a directory that does not exist in the image.
4. `book.py` has an import error (missing dependency, wrong streamtex version).

**Debug**:
```bash
# Check locally
docker run -p 8501:8501 my-image
curl http://localhost:8501/_stcore/health

# Check Render status
stx deploy status render
stx deploy status render streamtex-intro
```

### PyPI version mismatch with Render

**Symptom**: Render deployment uses an old version of streamtex; new features are missing.

**Cause**: Library changes were deployed to Render before being published to PyPI.

**Fix**: Always follow the deployment sequence:
1. Publish library to PyPI first: `stx publish pypi .`
2. Wait for PyPI to process.
3. Then deploy to Render.

**Verify**:
```bash
# Check what version PyPI has
pip index versions streamtex

# Check what version Render installed (in deploy logs)
# Look for: "Installing streamtex X.Y.Z" in the Render build output
```
