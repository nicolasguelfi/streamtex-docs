FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl nginx-light \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Cache-bust: Coolify passes SOURCE_COMMIT automatically. Changing this ARG
# invalidates all subsequent layers, ensuring uv sync fetches the latest PyPI packages.
ARG SOURCE_COMMIT=unknown

# Install dependencies
# .stx-version is copied first: changing the required version invalidates the cache.
# --no-sources ignores [tool.uv.sources] so uv resolves from PyPI instead of local path
# --upgrade-package streamtex forces latest PyPI version regardless of uv.lock
# Then strip the sources section so "uv run" won't try to re-resolve the local path
COPY .stx-version pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev --upgrade-package streamtex && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml && \
    uv pip install rich jinja2 && \
    uv run playwright install --with-deps chromium

# Fail the build if the installed streamtex version is older than required.
# Uses importlib.metadata (package registry) — NOT streamtex.__version__
# which was historically hardcoded and could be stale.
RUN REQUIRED=$(cat .stx-version | tr -d '[:space:]') && \
    INSTALLED=$(uv run python -c "from importlib.metadata import version; print(version('streamtex'))") && \
    echo "streamtex: required >= ${REQUIRED}, installed ${INSTALLED}" && \
    uv run python -c "import sys; \
r = tuple(int(x) for x in '${REQUIRED}'.split('.')); \
i = tuple(int(x) for x in '${INSTALLED}'.split('.')); \
sys.exit(1) if i < r else sys.exit(0)" || \
    { echo "ERROR: streamtex ${INSTALLED} < ${REQUIRED} — aborting build"; exit 1; }

# Copy all manuals (shared-blocks is needed by LazyBlockRegistry)
COPY manuals/ ./manuals/

# Changelog (read by bck_changelog block in each manual)
COPY CHANGELOG.md ./

# FOLDER is set at runtime by Coolify/Hetzner envVars (not build-time ARG)
ENV FOLDER="manuals/stx_manual_intro"

# Nginx configuration for dual-mode (Streamlit + static HTML)
COPY nginx.conf /etc/nginx/nginx.conf

# Entrypoint script (supports dual / static-only / streamlit-only modes)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Pre-warm the page cache for every manual so the first visitor loads instantly.
# Each manual gets its own .stx_cache/page_cache.json with the correct hash.
RUN for dir in manuals/stx_manual_*/; do \
        echo "Warming up cache for $dir ..." && \
        (cd "$dir" && uv run stx cache warmup .) || true; \
    done

# Pre-generate static HTML for every manual (served by Nginx on /html/).
# The entrypoint will clean and regenerate for the active FOLDER at runtime.
# This build-time export speeds up first cold-start.
RUN mkdir -p /app/static-html && \
    echo 'return 302 /html/;' > /app/static-html/.nginx-redirect.conf && \
    for dir in manuals/stx_manual_*/; do \
        echo "Exporting HTML for $dir ..." && \
        (cd "$dir" && uv run stx export html --output /app/static-html/ .) || true; \
    done

# STX_SERVE_MODE controls which services start (set at runtime by Coolify)
#   dual           = Nginx (:80) + Streamlit (:8501) — default
#   static-only    = Nginx (:80) only
#   streamlit-only = Streamlit (:8501) only — legacy behaviour
ENV STX_SERVE_MODE="dual"

EXPOSE 80 8501

# Health check: try Streamlit first, then Nginx static HTML
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health 2>/dev/null \
    || curl -fsL http://localhost:80/html/ -o /dev/null

# Entrypoint handles mode selection, cache refresh, and HTML re-generation
ENTRYPOINT ["/app/entrypoint.sh"]
