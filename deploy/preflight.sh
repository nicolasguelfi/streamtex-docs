#!/usr/bin/env bash
# preflight.sh — Pre-deployment verification script
# Run before deploying to Render, Docker, or any cloud platform.
#
# Usage: bash deploy/preflight.sh [manual_folder]
# Example: bash deploy/preflight.sh manuals/stx_manual_intro

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; ((WARNINGS++)); }
fail() { echo -e "${RED}✗${NC} $1"; ((ERRORS++)); }

echo "═══════════════════════════════════════════════"
echo "  StreamTeX — Pre-deployment Preflight Check"
echo "═══════════════════════════════════════════════"
echo ""

# 1. Check uv is available
if command -v uv &>/dev/null; then
    ok "uv found: $(uv --version)"
else
    fail "uv not found — install from https://docs.astral.sh/uv/"
fi

# 2. Check pyproject.toml exists
if [[ -f pyproject.toml ]]; then
    ok "pyproject.toml found"
else
    fail "pyproject.toml not found — run from project root"
fi

# 3. Check uv.lock exists and is up to date
if [[ -f uv.lock ]]; then
    ok "uv.lock found"
else
    warn "uv.lock missing — run 'uv lock' first"
fi

# 4. Check streamtex version is published on PyPI
STX_CONSTRAINT=$(grep 'streamtex>=' pyproject.toml | head -1 | sed 's/.*streamtex>=//' | sed 's/[",].*//')
if [[ -n "$STX_CONSTRAINT" ]]; then
    echo ""
    echo "Checking PyPI for streamtex>=$STX_CONSTRAINT ..."
    if uv run pip index versions streamtex 2>/dev/null | grep -q "$STX_CONSTRAINT"; then
        ok "streamtex $STX_CONSTRAINT available on PyPI"
    else
        fail "streamtex $STX_CONSTRAINT NOT found on PyPI — publish first!"
    fi
fi

# 5. Check Dockerfile exists
if [[ -f Dockerfile ]]; then
    ok "Dockerfile found"
else
    warn "Dockerfile missing"
fi

# 6. Check .streamlit/config.toml exists
FOLDER="${1:-manuals/stx_manual_intro}"
if [[ -f "$FOLDER/.streamlit/config.toml" ]]; then
    ok "Streamlit config found for $FOLDER"
else
    warn "No .streamlit/config.toml in $FOLDER"
fi

# 7. Check book.py exists in target folder
if [[ -f "$FOLDER/book.py" ]]; then
    ok "book.py found in $FOLDER"
else
    fail "No book.py in $FOLDER — cannot run this manual"
fi

# 8. Ruff lint check
echo ""
echo "Running ruff check ..."
if uv run ruff check --quiet 2>/dev/null; then
    ok "Ruff check passed"
else
    warn "Ruff check found issues — run 'uv run ruff check --fix'"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════"
if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}FAILED${NC}: $ERRORS error(s), $WARNINGS warning(s)"
    echo "Fix errors before deploying."
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}PASSED WITH WARNINGS${NC}: $WARNINGS warning(s)"
    exit 0
else
    echo -e "${GREEN}ALL CHECKS PASSED${NC} — ready to deploy!"
    exit 0
fi
