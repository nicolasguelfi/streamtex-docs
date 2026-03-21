#!/usr/bin/env bash
# deploy-staging.sh — Deploy a StreamTeX manual to the staging environment on Hetzner/Coolify.
#
# Usage:
#   ./deploy-staging.sh --manual intro --lib-branch fix/marker-bar --docs-branch feat/new-block
#   ./deploy-staging.sh --manual advanced                          # uses main for both
#   ./deploy-staging.sh --status                                   # show current staging status + session info
#   ./deploy-staging.sh --cleanup                                  # reset staging to main/main, clean branches
#   ./deploy-staging.sh --conclude                                 # merge branches → main, cleanup, redeploy prod
#
# Options:
#   --manual NAME        Manual to deploy: intro, advanced, deploy, developer, ai, collection (default: intro)
#   --lib-branch BRANCH  streamtex library branch to install (default: main = latest release)
#   --docs-branch BRANCH streamtex-docs branch to deploy (default: main)
#   --purpose TEXT        Description of what this staging session is testing
#   --status             Show current staging deployment status and session info
#   --cleanup            Reset staging to main/main and delete merged branches
#   --conclude           Merge branches → main, cleanup, and redeploy
#   --help               Show this help

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COOLIFY_URL="https://coolify.streamtex.org"
STATE_FILE="$SCRIPT_DIR/.stx-staging.json"
ENV_FILE="$SCRIPT_DIR/../streamtex/.env"
LIB_DIR="$SCRIPT_DIR/../streamtex"
STALE_DAYS=3

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
PURPOSE=""
ACTION="deploy"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --manual)      MANUAL="$2"; shift 2 ;;
        --lib-branch)  LIB_BRANCH="$2"; shift 2 ;;
        --docs-branch) DOCS_BRANCH="$2"; shift 2 ;;
        --purpose)     PURPOSE="$2"; shift 2 ;;
        --status)      ACTION="status"; shift ;;
        --cleanup)     ACTION="cleanup"; shift ;;
        --conclude)    ACTION="conclude"; shift ;;
        --help)
            head -18 "$0" | tail -17
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

# --- Read staging config ---
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
        curl -s -X DELETE "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs/$env_uuid" \
            -H "Authorization: Bearer $COOLIFY_API_TOKEN" > /dev/null 2>&1 || true
    fi

    curl -s -X POST "$COOLIFY_URL/api/v1/applications/$STAGING_UUID/envs" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"key\": \"$key\", \"value\": \"$value\", \"is_preview\": false}" > /dev/null
}

# --- Helper: save session to state file ---
save_session() {
    local lib_branch="$1"
    local docs_branch="$2"
    local manual="$3"
    local purpose="$4"
    local status="$5"

    python3 -c "
import json
state = json.load(open('$STATE_FILE'))
state['session'] = {
    'lib_branch': '$lib_branch',
    'docs_branch': '$docs_branch',
    'manual': '$manual',
    'purpose': '''$purpose''',
    'status': '$status',
    'deployed_at': __import__('datetime').datetime.now().isoformat(timespec='seconds')
}
json.dump(state, open('$STATE_FILE', 'w'), indent=2)
print('Session saved.')
"
}

# --- Helper: clear session from state file ---
clear_session() {
    python3 -c "
import json
state = json.load(open('$STATE_FILE'))
state.pop('session', None)
json.dump(state, open('$STATE_FILE', 'w'), indent=2)
"
}

# --- Helper: show session info with staleness warning ---
show_session() {
    python3 -c "
import json, sys
from datetime import datetime

state = json.load(open('$STATE_FILE'))
session = state.get('session')
if not session:
    print('No active staging session.')
    print('Staging is on main/main (idle).')
    sys.exit(0)

print('Active session:')
print(f\"  Lib branch:  {session.get('lib_branch', '?')}\")
print(f\"  Docs branch: {session.get('docs_branch', '?')}\")
print(f\"  Manual:      {session.get('manual', '?')}\")
print(f\"  Purpose:     {session.get('purpose', '-')}\")
print(f\"  Status:      {session.get('status', '?')}\")
print(f\"  Deployed at: {session.get('deployed_at', '?')}\")

deployed = session.get('deployed_at', '')
if deployed:
    try:
        dt = datetime.fromisoformat(deployed)
        age = datetime.now() - dt
        days = age.days
        hours = age.seconds // 3600
        if days >= $STALE_DAYS:
            print(f\"\")
            print(f\"  ⚠️  STALE SESSION — {days}d {hours}h old (threshold: ${STALE_DAYS}d)\")
            print(f\"  Action needed: --conclude (merge & deploy) or --cleanup (discard)\")
        elif days >= 1:
            print(f\"  Age: {days}d {hours}h\")
        else:
            print(f\"  Age: {hours}h\")
    except Exception:
        pass
"
}

# --- Helper: trigger deploy ---
trigger_deploy() {
    echo "Triggering deploy..."
    result=$(curl -s "$COOLIFY_URL/api/v1/deploy?uuid=$STAGING_UUID&force=true" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
        -H "Accept: application/json")

    if echo "$result" | grep -q "deployment queued"; then
        echo "Deploy triggered successfully!"
        echo "Watch progress: $COOLIFY_URL"
        echo "URL: https://docs-staging.streamtex.org"
    else
        echo "Deploy failed: $result"
        exit 1
    fi
}

# --- Helper: reset staging to main/main ---
reset_to_main() {
    echo "[1/5] Setting docs branch to 'main'..."
    curl -s -X PATCH "$COOLIFY_URL/api/v1/applications/$STAGING_UUID" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"git_branch": "main"}' > /dev/null

    echo "[2/5] Setting STX_BRANCH=main..."
    update_env "STX_BRANCH" "main"

    echo "[3/5] Setting STX_DOCS_BRANCH=main..."
    update_env "STX_DOCS_BRANCH" "main"

    echo "[4/5] Setting STX_DOCS_COMMIT..."
    local main_commit
    main_commit=$(cd "$SCRIPT_DIR" && git rev-parse --short origin/main 2>/dev/null || echo "?")
    update_env "STX_DOCS_COMMIT" "$main_commit"

    echo "[5/5] Triggering deploy on main/main..."
    trigger_deploy
    clear_session
}

# ============================================================
# ACTION: status
# ============================================================
if [ "$ACTION" = "status" ]; then
    echo "=== StreamTeX Staging Status ==="
    result=$(curl -s "$COOLIFY_URL/api/v1/applications/$STAGING_UUID" \
        -H "Authorization: Bearer $COOLIFY_API_TOKEN")
    echo "$result" | python3 -c "
import json,sys
app = json.load(sys.stdin)
print(f\"Service:     {app.get('name','?')}\")
print(f\"Status:      {app.get('status','?')}\")
print(f\"FQDN:        {app.get('fqdn','?')}\")
"
    echo ""
    show_session
    exit 0
fi

# ============================================================
# ACTION: cleanup — reset to main, optionally delete branches
# ============================================================
if [ "$ACTION" = "cleanup" ]; then
    echo "=== StreamTeX Staging Cleanup ==="
    show_session
    echo ""

    # Read current session branches before clearing
    SESSION_LIB=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('lib_branch','main'))" 2>/dev/null)
    SESSION_DOCS=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('docs_branch','main'))" 2>/dev/null)

    read -p "Reset staging to main/main? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi

    reset_to_main

    # Offer to delete branches
    if [ "$SESSION_LIB" != "main" ]; then
        echo ""
        read -p "Delete lib branch '$SESSION_LIB' from remote? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            (cd "$LIB_DIR" && git push origin --delete "$SESSION_LIB" 2>/dev/null && echo "  Deleted origin/$SESSION_LIB (lib)") || echo "  Could not delete origin/$SESSION_LIB (may already be deleted)"
        fi
    fi

    if [ "$SESSION_DOCS" != "main" ]; then
        read -p "Delete docs branch '$SESSION_DOCS' from remote? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            (cd "$SCRIPT_DIR" && git push origin --delete "$SESSION_DOCS" 2>/dev/null && echo "  Deleted origin/$SESSION_DOCS (docs)") || echo "  Could not delete origin/$SESSION_DOCS (may already be deleted)"
        fi
    fi

    echo ""
    echo "Cleanup complete. Staging is back on main/main."
    exit 0
fi

# ============================================================
# ACTION: conclude — merge branches to main, cleanup, redeploy
# ============================================================
if [ "$ACTION" = "conclude" ]; then
    echo "=== StreamTeX Staging Conclude ==="
    show_session
    echo ""

    SESSION_LIB=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('lib_branch','main'))" 2>/dev/null)
    SESSION_DOCS=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('docs_branch','main'))" 2>/dev/null)

    if [ "$SESSION_LIB" = "main" ] && [ "$SESSION_DOCS" = "main" ]; then
        echo "No branches to merge — staging is already on main/main."
        exit 0
    fi

    # Merge lib branch
    if [ "$SESSION_LIB" != "main" ]; then
        echo ""
        read -p "Merge lib branch '$SESSION_LIB' into main? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "  Merging $SESSION_LIB → main (lib)..."
            (cd "$LIB_DIR" && git checkout main && git pull && git merge "$SESSION_LIB" && git push) || {
                echo "  ERROR: Merge failed. Resolve manually, then re-run --conclude."
                exit 1
            }
            echo "  Deleting branch $SESSION_LIB..."
            (cd "$LIB_DIR" && git branch -d "$SESSION_LIB" 2>/dev/null; git push origin --delete "$SESSION_LIB" 2>/dev/null) || true
        fi
    fi

    # Merge docs branch
    if [ "$SESSION_DOCS" != "main" ]; then
        echo ""
        read -p "Merge docs branch '$SESSION_DOCS' into main? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "  Merging $SESSION_DOCS → main (docs)..."
            (cd "$SCRIPT_DIR" && git checkout main && git pull && git merge "$SESSION_DOCS" && git push) || {
                echo "  ERROR: Merge failed. Resolve manually, then re-run --conclude."
                exit 1
            }
            echo "  Deleting branch $SESSION_DOCS..."
            (cd "$SCRIPT_DIR" && git branch -d "$SESSION_DOCS" 2>/dev/null; git push origin --delete "$SESSION_DOCS" 2>/dev/null) || true
        fi
    fi

    # Reset staging to main
    echo ""
    echo "Resetting staging to main/main..."
    reset_to_main

    echo ""
    echo "Conclude complete. Branches merged, staging reset to main."
    echo "Note: if lib changes were merged, remember to publish to PyPI before prod deploy."
    exit 0
fi

# ============================================================
# ACTION: deploy
# ============================================================
echo "=== StreamTeX Staging Deploy ==="
echo "Manual:      $MANUAL ($FOLDER)"
echo "Docs branch: $DOCS_BRANCH"
echo "Lib branch:  $LIB_BRANCH"
echo "Service:     $STAGING_UUID"
echo ""

# Warn if overwriting an existing session with different branches
EXISTING_LIB=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('lib_branch',''))" 2>/dev/null)
EXISTING_DOCS=$(python3 -c "import json; s=json.load(open('$STATE_FILE')).get('session',{}); print(s.get('docs_branch',''))" 2>/dev/null)

if [ -n "$EXISTING_LIB" ] && [ "$EXISTING_LIB" != "main" ] && [ "$EXISTING_LIB" != "$LIB_BRANCH" ]; then
    echo "⚠️  Warning: overwriting existing session (lib: $EXISTING_LIB → $LIB_BRANCH)"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] || exit 0
fi

if [ -n "$EXISTING_DOCS" ] && [ "$EXISTING_DOCS" != "main" ] && [ "$EXISTING_DOCS" != "$DOCS_BRANCH" ]; then
    echo "⚠️  Warning: overwriting existing session (docs: $EXISTING_DOCS → $DOCS_BRANCH)"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] || exit 0
fi

# Prompt for purpose if deploying non-main branches without one
if [ -z "$PURPOSE" ] && { [ "$LIB_BRANCH" != "main" ] || [ "$DOCS_BRANCH" != "main" ]; }; then
    read -p "Purpose of this staging session (optional): " PURPOSE
fi

# Resolve docs commit hash locally
DOCS_COMMIT=$(cd "$SCRIPT_DIR" && git rev-parse --short "origin/$DOCS_BRANCH" 2>/dev/null || echo "?")

# Step 1: Update the docs branch
echo "[1/6] Setting docs branch to '$DOCS_BRANCH'..."
curl -s -X PATCH "$COOLIFY_URL/api/v1/applications/$STAGING_UUID" \
    -H "Authorization: Bearer $COOLIFY_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"git_branch\": \"$DOCS_BRANCH\"}" > /dev/null

# Step 2: Update FOLDER
echo "[2/6] Setting FOLDER=$FOLDER..."
update_env "FOLDER" "$FOLDER"

# Step 3: Update STX_BRANCH (lib branch, read at container startup)
echo "[3/6] Setting STX_BRANCH=$LIB_BRANCH..."
update_env "STX_BRANCH" "$LIB_BRANCH"

# Step 4: Update STX_DOCS_BRANCH and STX_DOCS_COMMIT (for banner display)
echo "[4/6] Setting STX_DOCS_BRANCH=$DOCS_BRANCH..."
update_env "STX_DOCS_BRANCH" "$DOCS_BRANCH"

echo "[5/6] Setting STX_DOCS_COMMIT=$DOCS_COMMIT..."
update_env "STX_DOCS_COMMIT" "$DOCS_COMMIT"

# Step 6: Trigger deploy
echo "[6/6] Triggering deploy..."
trigger_deploy

# Save session
save_session "$LIB_BRANCH" "$DOCS_BRANCH" "$MANUAL" "$PURPOSE" "testing"
