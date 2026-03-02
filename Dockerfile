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
# --no-sources ignores [tool.uv.sources] so uv resolves from PyPI instead of local path
# Then strip the sources section so "uv run" won't try to re-resolve the local path
COPY pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml

# Copy all manuals (shared-blocks is needed by LazyBlockRegistry)
COPY manuals/ ./manuals/

# FOLDER is set at runtime by Render envVars (not build-time ARG)
ENV FOLDER="manuals/stx_manual_intro"

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["/bin/sh", "-c", \
            "cd /app/${FOLDER} && exec uv run streamlit run book.py --server.port=8501 --server.address=0.0.0.0"]
