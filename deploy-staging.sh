#!/usr/bin/env bash
# deploy-staging.sh — Deploy a StreamTeX manual to the staging environment on Hetzner/Coolify.
#
# Usage:
#   ./deploy-staging.sh --manual intro --lib-branch fix/marker-bar --docs-branch feat/new-block
#   ./deploy-staging.sh --manual advanced                          # uses main for both
#   ./deploy-staging.sh --status                                   # show current staging status
#
# Options:
#   --manual NAME        Manual to deploy: intro, advanced, deploy, developer, ai, collection (default: intro)
#   --lib-branch BRANCH  streamtex library branch to install (default: main = latest release)
#   --docs-branch BRANCH streamtex-docs branch to deploy (default: main)
#   --status             Show current staging deployment status
#   --help               Show this help

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COOLIFY_URL="https://coolify.streamtex.org"
STATE_FILE="$SCRIPT_DIR/.stx-staging.json"
ENV_FILE="$SCRIPT_DIR/../streamtex/.env"

# --- Load API token ---
if [ -z "${COOLIFY_API_TOKEN:-}" ]; then
    if [ -f "$ENV_FILE" ]; then
        COOLIFY_API_TOKEN=$(grep '^COOLIFY_API_TOKEN' "$ENV_FILE" | sed 's/^[^=]*=\s*//' | tr -d ' ')
    fi
fi
if [ -z "${COOLIFY_API_TOKEN:-}" ]; then
    echo "Error: COOLIFY_API_TOKEN not found. Set it in environment or in $ENV_FILE"
    exit 1
fi

# --- Parse arguments ---
MANUAL="intro"
LIB_BRANCH="main"
DOCS_BRANCH="main"
SHOW_STATUS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --manual)      MANUAL="$2"; shift 2 ;;
        --lib-branch)  LIB_BRANCH="$2"; shift 2 ;;
        --docs-branch) DOCS_BRANCH="$2"; shift 2 ;;
        --status)      SHOW_STATUS=true; shift ;;
        --help)
            head -15 "$0" | tail -14
            exit 0 ;;
        *)
            echo "Unknown option: $1. Use --help for usage."
            exit 1 ;;
    esac
done

# Map manual short name to folder
case "$MANUAL" in
    intro)      FOLDER="manuals/stx_manual_intro" ;;
    advanced)   FOLDER="manuals/stx_manual_advanced" ;;
    deploy)     FOLDER="manuals/stx_manual_deploy" ;;
    developer)  FOLDER="manuals/stx_manual_developer" ;;
    ai)         FOLDER="manuals/stx_manual_ai" ;;
    collection) FOLDER="manuals/stx_manuals_collection" ;;
    *)
        echo "Error: Unknown manual '$MANUAL'. Use: intro, advanced, deploy, developer, ai, collection"
        exit 1 ;;
esac

# --- Read staging service UUID ---
STAGING_UUID=""
if [ -f "$STATE_FILE" ]; then
    STAGING_UUID=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('uuid',''))" 2>/dev/null || echo "")
fi

if [ -z "$STAGING_UUID" ]; then
    echo "Error: No staging service found. Create it first in Coolify UI or via API."
    echo "Then save its UUID: echo '{\"uuid\": \"YOUR_UUID\"}' > $STATE_FILE"
    exit 1
fi

# --- Helper: update or create an env var ---
update_env() {
    local key="$1"
    local value="$2"

    # Find existing env var UUID for this key
    local env_uuid
    env_uuid=$(curl -s "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" | \
        python3 -c "
import json,sys
for ev in json.load(sys.stdin):
    if ev.get('key') == '$key' and not ev.get('is_preview', False):
        print(ev['uuid']); break
" 2>/dev/null || echo "")

    if [ -n "$env_uuid" ]; then
        # Delete existing, then recreate (Coolify API doesn't support PATCH on envs)
        curl -s -X DELETE "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs/$env_uuid" \
            -H "Authorization: Bearer $COOLIFY_API_TOKEN" > /dev/null 2>&1 || true
    fi

    # Create new env var
    curl -s -X POST "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"key\": \"$key\", \"value\": \"$value\", \"is_preview\": false}" > /dev/null
}

# --- Status ---
if [ "$SHOW_STATUS" = true ]; then
    echo "=== StreamTeX Staging Status ==="
    result=$(curl -s "$COOLIFY_URL/api/v1/applications/$STAGING_UUID" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN")
    echo "$result" | python3 -c "
import json,sys
app = json.load(sys.stdin)
print(f\"Service:     {app.get('name','?')}\")
print(f\"UUID:        {app.get('uuid','?')}\")
print(f\"Status:      {app.get('status','?')}\")
print(f\"Docs branch: {app.get('git_branch','?')}\")
print(f\"Dockerfile:  {app.get('dockerfile_location','?')}\")
print(f\"FQDN:        {app.get('fqdn','?')}\")
"
    echo ""
    echo "Environment variables:"
    curl -s "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" | python3 -c "
import json,sys
for ev in json.load(sys.stdin):
    if not ev.get('is_preview', False):
        print(f\"  {ev.get('key','?'):15s} = {ev.get('value','?')}\")
"
    exit 0
fi

# --- Deploy ---
echo "=== StreamTeX Staging Deploy ==="
echo "Manual:      $MANUAL ($FOLDER)"
echo "Docs branch: $DOCS_BRANCH"
echo "Lib branch:  $LIB_BRANCH"
echo "Service:     $STAGING_UUID"
echo ""

# Step 1: Update the docs branch
echo "[1/4] Setting docs branch to '$DOCS_BRANCH'..."
curl -s -X PATCH "$COOLIFY_URL/api/v1/applications/$STAGING_UUID" \
    -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"git_branch\": \"$DOCS_BRANCH\"}" > /dev/null

# Step 2: Update FOLDER
echo "[2/4] Setting FOLDER=$FOLDER..."
update_env "FOLDER" "$FOLDER"

# Step 3: Update STX_BRANCH (lib branch, read at container startup)
echo "[3/4] Setting STX_BRANCH=$LIB_BRANCH..."
update_env "STX_BRANCH" "$LIB_BRANCH"

# Step 4: Trigger deploy
echo "[4/4] Triggering deploy..."
result=$(curl -s "$COOLIFY_URL/api/v1/deploy?uuid=$STAGING_UUID&force=true" \
    -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
    -H "Accept: application/json")

if echo "$result" | grep -q "deployment queued"; then
    echo ""
    echo "Deploy triggered successfully!"
    echo "Watch progress: $COOLIFY_URL"
    echo "URL: https://docs-staging.streamtex.org"
else
    echo "Deploy failed: $result"
    exit 1
fi
