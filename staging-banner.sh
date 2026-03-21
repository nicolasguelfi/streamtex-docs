#!/bin/sh
# staging-banner.sh — Inject a rich staging banner + orange favicon into Streamlit's index.html.
# Called by Dockerfile.staging entrypoint. Zero modification to project source files.
# The patch targets Streamlit's internal static/index.html inside the installed package.
#
# Expected env vars (set by ENTRYPOINT before calling this script):
#   STX_BRANCH       — lib branch name (e.g. fix/mobile-banner)
#   STX_VERSION      — lib version (e.g. 0.5.4)
#   STX_LIB_COMMIT   — lib git commit short hash (e.g. 778e24f)
#   STX_DOCS_BRANCH  — docs branch name (e.g. fix/staging-infra)
#   STX_DOCS_COMMIT  — docs git commit short hash (e.g. 59239a5)
#   STX_DEPLOY_TIME  — deploy timestamp (e.g. 2026-03-21 22:54)
#   FOLDER           — manual folder (e.g. manuals/stx_manual_intro)

set -e

STX_BRANCH="${STX_BRANCH:-main}"
STX_VERSION="${STX_VERSION:-?}"
STX_LIB_COMMIT="${STX_LIB_COMMIT:-?}"
STX_DOCS_BRANCH="${STX_DOCS_BRANCH:-main}"
STX_DOCS_COMMIT="${STX_DOCS_COMMIT:-?}"
STX_DEPLOY_TIME="${STX_DEPLOY_TIME:-?}"
FOLDER="${FOLDER:-?}"

# Extract manual short name from folder path (e.g. manuals/stx_manual_intro → intro)
MANUAL_NAME=$(echo "$FOLDER" | sed 's|.*/stx_manual_||; s|.*/stx_manuals_||')

# Locate Streamlit's index.html (use venv python directly)
IDX=$(/app/.venv/bin/python -c "import streamlit, pathlib; print(pathlib.Path(streamlit.__file__).parent / 'static' / 'index.html')")

if [ ! -f "$IDX" ]; then
    echo "[staging-banner] WARNING: Streamlit index.html not found at $IDX — skipping banner injection."
    exit 0
fi

# Orange SVG favicon (STx on orange rounded square)
FAVICON='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="%23FF6600"/><text x="16" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="sans-serif">STx</text></svg>'

# Build banner content lines
LINE1="STAGING"
LINE2="lib: ${STX_BRANCH} @ ${STX_LIB_COMMIT} (v${STX_VERSION}) | docs: ${STX_DOCS_BRANCH} @ ${STX_DOCS_COMMIT} | ${MANUAL_NAME} | ${STX_DEPLOY_TIME}"

# Inject before </head>:
#   1. Override favicon with orange version
#   2. Fixed orange banner (real <div>) with two lines of deployment info
#   3. Push Streamlit content below the banner
PATCH=$(cat <<ENDPATCH
<!-- staging-banner -->
<link rel="icon" type="image/svg+xml" href="${FAVICON}">
<style>
  #stx-staging-banner {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    z-index: 999999;
    background: #FF6600;
    color: white;
    text-align: center;
    padding: 4px 8px;
    font-family: sans-serif;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    line-height: 1.3;
  }
  #stx-staging-banner .stx-sb-title {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 2px;
  }
  #stx-staging-banner .stx-sb-details {
    font-size: 11px;
    font-family: monospace;
    opacity: 0.9;
  }
  .stApp { padding-top: 46px !important; }
</style>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('stx-staging-banner')) return;
    var b = document.createElement('div');
    b.id = 'stx-staging-banner';
    b.innerHTML = '<div class="stx-sb-title">${LINE1}</div><div class="stx-sb-details">${LINE2}</div>';
    document.body.insertBefore(b, document.body.firstChild);
  });
</script>
ENDPATCH
)

# Use awk for safe multi-line injection (sed struggles with newlines)
awk -v patch="$PATCH" '{gsub(/<\/head>/, patch "\n</head>")}1' "$IDX" > "${IDX}.tmp" \
    && mv "${IDX}.tmp" "$IDX"

echo "[staging-banner] Banner injected: $LINE1 | $LINE2"
