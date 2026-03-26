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
# .stx-version is copied first: changing the required version invalidates the cache.
# --no-sources ignores [tool.uv.sources] so uv resolves from PyPI instead of local path
# --upgrade-package streamtex forces latest PyPI version regardless of uv.lock
# Then strip the sources section so "uv run" won't try to re-resolve the local path
COPY .stx-version pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev --upgrade-package streamtex && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml && \
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

# Pre-warm the page cache for every manual so the first visitor loads instantly.
# Each manual gets its own .stx_cache/page_cache.json with the correct hash.
RUN for dir in manuals/stx_manual_*/; do \
        echo "Warming up cache for $dir ..." && \
        (cd "$dir" && uv run stx cache warmup .) || true; \
    done

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# On startup: clear stale caches then re-warm the target manual.
# The build-time warmup covers most cases, but env var changes (FOLDER)
# or content updates via restart (without rebuild) would serve stale data.
# Re-warming adds ~5s to startup but guarantees fresh content.
ENTRYPOINT ["/bin/sh", "-c", \
            "cd /app/${FOLDER} && rm -rf .stx_cache .streamlit/cache && uv run stx cache warmup . 2>/dev/null; exec uv run streamlit run book.py --server.port=8501 --server.address=0.0.0.0"]
