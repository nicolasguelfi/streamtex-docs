FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl git nginx-light \
        texlive-latex-base texlive-latex-extra texlive-pictures \
        texlive-fonts-recommended texlive-science \
        dvisvgm ghostscript \
    && rm -rf /var/lib/apt/lists/*
# git: needed by uv to resolve `streamtex-design @ git+https://...` declared
#   in the root pyproject.toml (streamtex-design is not yet on PyPI).
# texlive-pictures: provides the tikz/pgf packages (\usepackage{tikz}).
# texlive-latex-extra: xcolor, geometry, fancyhdr, etc. — commonly used
#   by TikZ examples in the advanced manual.
# texlive-science: math symbols / commutative diagrams used by some
#   manual examples.
# texlive-latex-base alone is insufficient — \usepackage{tikz} fails
#   with "File 'tikz.sty' not found" without texlive-pictures.

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Cache-bust: Coolify passes SOURCE_COMMIT automatically. Changing this ARG
# invalidates all subsequent layers.
ARG SOURCE_COMMIT=unknown

# Install dependencies
# .stx-version is copied first: changing the required version invalidates the cache.
# --no-sources ignores [tool.uv.sources] so uv resolves from PyPI instead of local path,
# keeping the streamtex version recorded in uv.lock — the version the CI tests.
# (No --upgrade-package: it installed the latest PyPI release, untested here.)
# Then strip the sources section so "uv run" won't try to re-resolve the local path
COPY .stx-version pyproject.toml uv.lock ./
RUN uv sync --no-sources --no-dev && \
    sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml && \
    uv pip install rich jinja2 && \
    uv run playwright install --with-deps chromium

# Fail the build unless the installed streamtex is exactly the pinned version.
# Uses importlib.metadata (package registry) — NOT streamtex.__version__
# which was historically hardcoded and could be stale.
RUN REQUIRED=$(cat .stx-version | tr -d '[:space:]') && \
    INSTALLED=$(uv run python -c "from importlib.metadata import version; print(version('streamtex'))") && \
    echo "streamtex: pinned ${REQUIRED}, installed ${INSTALLED}" && \
    [ "${INSTALLED}" = "${REQUIRED}" ] || \
    { echo "ERROR: streamtex ${INSTALLED} != ${REQUIRED} (.stx-version) — aborting build"; exit 1; }

# Copy all manuals (shared-blocks is needed by LazyBlockRegistry)
COPY manuals/ ./manuals/

# Strip `[tool.uv.sources]` from every per-manual pyproject.toml — this
# section is for local dev (path = "../../../streamtex") and breaks the
# cache-warmup + static-HTML-export passes that run `uv run` inside each
# manual directory.  Equivalent to the same sed pass applied earlier to
# the root pyproject.toml (UV_NO_SOURCES discipline).
RUN find manuals -mindepth 2 -maxdepth 2 -name pyproject.toml -exec \
        sed -i '/^\[tool\.uv\.sources\]/,/^$/d' {} \;

# Changelog (read by bck_changelog block in each manual)
COPY CHANGELOG.md ./

# FOLDER is set at runtime by Coolify/Hetzner envVars (not build-time ARG)
ENV FOLDER="manuals/stx_manual_intro"

# Nginx configuration for dual-mode (Streamlit + static HTML)
COPY nginx.conf /etc/nginx/nginx.conf

# Entrypoint script (supports dual / static-only / streamlit-only modes)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Régime d'images (2026-09-11, décision d'auteur) : plus AUCUN réchauffage de
# cache ni export HTML à la construction. L'entrypoint efface et régénère les
# deux, pour le seul module servi (FOLDER), à CHAQUE démarrage — les couches
# de construction étaient jetées avant la première visite (mesuré : 2,6 Go par
# image, 87 Go sur le serveur pour rien). Le cache reste chaud dès la première
# visite : c'est le démarrage qui le garantit, pas l'image.
RUN mkdir -p /app/static-html && \
    echo 'return 302 /html/;' > /app/static-html/.nginx-redirect.conf

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
