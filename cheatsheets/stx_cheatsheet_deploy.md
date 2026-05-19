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

# Hetzner / Coolify (production target)
stx deploy hetzner .
stx deploy hetzner . --subdomain my-app
stx deploy hetzner . --serve-mode dual         # Streamlit + Nginx static fallback
stx deploy update [TARGET]                     # rebuild service + replicas
stx deploy update [TARGET] --quick             # restart only
stx deploy scale TARGET --replicas 3           # load-balanced
stx deploy status coolify                      # health of all services
stx deploy status coolify docs-intro           # specific service

# Hetzner / Coolify (server bootstrap, one-off)
stx deploy setup                               # create+secure server, install Coolify
stx deploy provision                           # create server only
stx deploy secure                              # SSH-key + UFW + fail2ban
stx deploy install-coolify

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

## 3. Hetzner / Coolify Deployment (production target)

### stx deploy hetzner — deploy via Coolify API

```bash
stx deploy hetzner PATH [--subdomain NAME] [--uuid UUID]
                        [--serve-mode streamlit|dual|static-only]
                        [--yes]
```

**Default**:
```bash
stx deploy hetzner .
```

**With a chosen subdomain on `streamtex.org`**:
```bash
stx deploy hetzner . --subdomain my-app
# → deploys to https://my-app.streamtex.org
```

**With dual serve-mode (Streamlit + Nginx static fallback)**:
```bash
stx deploy hetzner . --serve-mode dual
```

What it does:
1. Runs `stx deploy preflight` first (book.py, Dockerfile, git, tests, lint).
2. Discovers or creates a Coolify application UUID (state in `.stx-deploy.json`).
3. Pushes git, triggers a Coolify deploy via API, waits for the rebuild.
4. For multi-replica projects, deploys all replicas (batched ≤ 4 to avoid server hang).
5. Updates `.stx-deploy.json` with the new state.

### stx deploy update — rebuild or restart service

```bash
stx deploy update                              # rebuild ALL services + replicas
stx deploy update docs-intro                   # rebuild one service
stx deploy update docs-intro --quick           # restart only (no rebuild)
stx deploy update docs-intro --serve-mode static-only
```

### stx deploy scale — horizontal scaling

```bash
stx deploy scale docs-intro --replicas 3       # 3 load-balanced containers
```

### Coolify state file (`.stx-deploy.json`)

Stored at the workspace root. Tracks service UUIDs, hostnames,
serve modes. Versioned with the repo (no secrets).

### API tokens

In `streamtex/.env` (gitignored):

```bash
COOLIFY_API_TOKEN=...    # Coolify management API
HETZNER_API_TOKEN=...    # Hetzner Cloud (server lifecycle)
```

For GitHub Actions auto-deploy: secret `COOLIFY_API_TOKEN` configured
in the repo settings.

### stx deploy status — health monitoring

```bash
stx deploy status coolify                      # probe all Coolify services
stx deploy status coolify docs-intro           # probe a specific service
stx deploy status huggingface                  # probe HF Space from 'hf' git remote
stx deploy status huggingface user/repo        # probe a specific HF Space
```

Probes the service URL with HTTP HEAD. Returns one of:
- **live** -- HTTP 2xx
- **sleep** -- HTTP 502/503 or timeout (service may be waking)
- **down** -- HTTP 404 (service not found)
- **error** -- other HTTP error or network issue

For HuggingFace, uses the HF API (`/api/spaces/owner/repo`) and maps runtime stage (RUNNING, SLEEPING, PAUSED, BUILDING) to status.

### Coolify env vars

Env vars are managed in the Coolify dashboard per application
(see https://coolify.streamtex.org). The runtime variable `FOLDER`
selects which manual the shared Dockerfile serves.

Example for `docs-intro.streamtex.org`:

```
FOLDER=manuals/stx_manual_intro
SOURCE_COMMIT=<sha>       # cache-bust ARG, set by deploy
```

### Server bootstrap (one-off, when starting from scratch)

```bash
stx deploy setup            # provision + secure + install Coolify (all-in-one)
stx deploy provision        # create Hetzner Cloud server only
stx deploy secure           # SSH-key login + UFW + fail2ban
stx deploy install-coolify  # install Coolify on the provisioned server
```

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

### ALWAYS publish to PyPI BEFORE deploying to Hetzner

The Docker build on Hetzner/Coolify installs `streamtex` from PyPI,
not from your local machine. If your docs use features from a new
library version, that version MUST be published on PyPI first.

### Correct deployment sequence

```
1. Make library changes in streamtex/
2. Bump version in pyproject.toml + __init__.py
3. Run tests: uv run pytest tests/ -v
4. Publish to PyPI: stx publish pypi .
5. Wait for PyPI to process (usually < 1 minute)
6. Bump streamtex-docs/.stx-version (used by deploy guard)
7. Push docs changes to GitHub
8. Trigger Hetzner deploy (`stx deploy update` or auto via GitHub Action)
```

### What stx claude update --all does (and does NOT do)

`stx claude update --all` syncs Claude AI profiles only. It does NOT:
- Publish to PyPI
- Deploy to Hetzner/Coolify
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

### Hetzner deploy workflow

File: `streamtex-docs/.github/workflows/hetzner-deploy.yml`

Auto-deploys on push to `main` (configured per service via Coolify
webhooks). Manual trigger:

```bash
gh workflow run hetzner-deploy.yml -R nicolasguelfi/streamtex-docs
```

The workflow:
1. Reads service UUIDs from `.stx-deploy.json`.
2. Detects which files changed (compares `before..after`).
3. Shared file changes (Dockerfile, pyproject.toml, shared-blocks) trigger ALL services.
4. Manual folder changes trigger only the affected service.
5. `workflow_dispatch` (manual trigger) always deploys ALL services.
6. Hits the Coolify API to rebuild each affected application.

Required secret: `COOLIFY_API_TOKEN` (set in GitHub repo settings).

Critical: batch size capped at **4 services** per run — server
hangs above that (memory rule `feedback_deploy_batch_size`).

---

## 8. Hetzner Services Reference

### Current services (Coolify applications on `streamtex.org`)

See `.stx-deploy.json` at the workspace root for the authoritative
state (UUIDs, hostnames, serve modes). Live snapshot:

| Service | URL | FOLDER |
|---|---|---|
| docs | https://docs.streamtex.org | manuals/stx_manuals_collection |
| docs-intro | https://docs-intro.streamtex.org | manuals/stx_manual_intro |
| docs-advanced | https://docs-advanced.streamtex.org | manuals/stx_manual_advanced |
| docs-deploy | https://docs-deploy.streamtex.org | manuals/stx_manual_deploy |
| docs-developer | https://docs-developer.streamtex.org | manuals/stx_manual_developer |
| docs-ai | https://docs-ai.streamtex.org | manuals/stx_manual_ai |
| docs-ce | https://docs-ce.streamtex.org | manuals/stx_manual_ce |

### Collection hub env vars

The collection hub service (`streamtex`) needs `STX_URL_TEST_*` env vars pointing to the other services:

```yaml
envVars:
  - key: FOLDER
    value: manuals/stx_manuals_collection
  - key: STX_URL_TEST_INTRO
    value: https://docs-intro.streamtex.org
  - key: STX_URL_TEST_ADVANCED
    value: https://docs-advanced.streamtex.org
  - key: STX_URL_TEST_DEPLOY
    value: https://docs-deploy.streamtex.org
  - key: STX_URL_TEST_DEVELOPER
    value: https://docs-developer.streamtex.org
  - key: STX_URL_TEST_AI
    value: https://docs-ai.streamtex.org
  - key: STX_PASSWORD
    value: ""
```

---

## 9. Claude-Assisted Deployment

### /stx-deploy:* slash commands

The `stx-deploy/` command group (defined in `streamtex-claude/shared/commands/stx-deploy/`) drives the full Hetzner/Coolify deployment pipeline through Claude. The legacy `/stx-developer:deploy` command was unified into this group on 2026-03-10.

**Subcommands** (run `/stx-deploy:<name>`):
- `preflight` — verify prerequisites (Dockerfile, pyproject.toml, tests pass, git clean).
- `provision` — create a Hetzner cax21 ARM server.
- `setup` / `setup-loadbalancer` — local environment / multi-server setup.
- `secure`, `install-coolify`, `configure-domain` — server hardening + Coolify install + DNS/SSL.
- `deploy` / `deploy-batch` / `update` — deploy one project, batch up to 4, or update existing services.
- `scale`, `status`, `go` — scaling, status dashboard, full zero-to-live in one command.

**Pre-deployment checks** (`/stx-deploy:preflight`):
1. Reads `Dockerfile`, `pyproject.toml`, `.streamlit/config.toml`.
2. Runs `uv run pytest tests/ -v` and aborts on failure.
3. Verifies `streamlit>=1.54.0` in dependencies, `enableStaticServing = true`, and image assets exist.
4. Checks git status for uncommitted changes.

**Local Docker check** (`/stx-deploy:deploy --target docker`):
```bash
docker build --build-arg FOLDER=<project_path> -t streamtex-app .
docker run -p 8501:8501 streamtex-app
```

### Workflow: Claude runs preflight, builds Docker, deploys

Typical Claude interaction:
```
User: /stx-deploy:deploy
Claude:
  1. Reads project configuration files
  2. Runs uv run pytest tests/ -v
  3. Verifies requirements
  4. Checks git status
  5. Builds Docker image (or triggers Coolify deploy via API)
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

# Default folder (overridden by Coolify env vars per application)
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

Each Coolify application sets a different `FOLDER`:

```
docs           -> FOLDER=manuals/stx_manuals_collection
docs-intro     -> FOLDER=manuals/stx_manual_intro
docs-ai        -> FOLDER=manuals/stx_manual_ai
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

### Coolify deploy fails — application not found

**Symptom**: `stx deploy hetzner` reports a missing application UUID.

**Cause**: The application was not yet registered in `.stx-deploy.json`,
or the UUID was rotated in the Coolify dashboard.

**Fix**: re-register via `stx deploy hetzner . --subdomain <name>` —
the command creates the Coolify application on first run and stores
the UUID in `.stx-deploy.json`.

### Env vars not applied on Coolify

**Symptom**: Service is rebuilt but env vars (`FOLDER`, `STX_PASSWORD`, etc.)
are missing or wrong.

**Cause**: Env vars are managed per application in the Coolify dashboard,
not in any committed file.

**Fix**: open the Coolify dashboard
(https://coolify.streamtex.org), select the application, edit env
vars manually. The deploy command does NOT push them — that is by
design (avoids leaking secrets through git).

### Health check failures

**Symptom**: Coolify shows the service as unhealthy or failing
health checks.

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

# Check Coolify status
stx deploy status coolify
stx deploy status coolify docs-intro
```

### PyPI version mismatch with Hetzner

**Symptom**: Hetzner deployment uses an old version of streamtex;
new features are missing.

**Cause**: Library changes were deployed before being published to PyPI.

**Fix**: Always follow the deployment sequence:
1. Publish library to PyPI first: `stx publish pypi .`
2. Wait for PyPI to process.
3. Bump `streamtex-docs/.stx-version`.
4. Then `stx deploy update`.

**Verify**:
```bash
# Check what version PyPI has (use the JSON API — never `pip index versions`)
curl -s https://pypi.org/pypi/streamtex/json | jq -r '.info.version'

# Check what version Coolify installed (in build logs)
# Look for: "Installing streamtex X.Y.Z" in the Coolify build output
```
