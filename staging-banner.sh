#!/bin/sh
# staging-banner.sh — Inject a staging banner + orange favicon into Streamlit's index.html.
# Called by Dockerfile.staging entrypoint. Zero modification to project source files.
# The patch targets Streamlit's internal static/index.html inside the installed package.

set -e

STX_BRANCH="${STX_BRANCH:-main}"

# Locate Streamlit's index.html
IDX=$(uv run python3 -c "import streamlit, pathlib; print(pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html')")

if [ ! -f "$IDX" ]; then
    echo "[staging-banner] WARNING: Streamlit index.html not found at $IDX — skipping banner injection."
    exit 0
fi

# Orange SVG favicon (STx on orange rounded square)
FAVICON='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="%23FF6600"/><text x="16" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="sans-serif">STx</text></svg>'

# Inject before </head>:
#   1. Override favicon with orange version
#   2. Fixed orange banner at top of page via CSS pseudo-element
#   3. Push page content down so banner doesn't overlap
PATCH=$(cat <<ENDPATCH
<!-- staging-banner -->
<link rel="icon" type="image/svg+xml" href="${FAVICON}">
<style>
  body::before {
    content: "STAGING — ${STX_BRANCH}";
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    z-index: 999999;
    background: #FF6600;
    color: white;
    text-align: center;
    padding: 5px 0;
    font: bold 14px/1.4 sans-serif;
    letter-spacing: 1px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }
  /* Push Streamlit content below the banner */
  .stApp { padding-top: 32px !important; }
</style>
ENDPATCH
)

# Use awk for safe multi-line injection (sed struggles with newlines)
awk -v patch="$PATCH" '{gsub(/<\/head>/, patch "\n</head>")}1' "$IDX" > "${IDX}.tmp" \
    && mv "${IDX}.tmp" "$IDX"

echo "[staging-banner] Banner injected into $IDX"
