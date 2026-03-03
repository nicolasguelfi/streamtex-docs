#!/bin/bash
# claude-sync.sh — Synchronise les fichiers Claude Code entre machines via le cloud
#
# Usage:
#   ./claude-sync.sh              # Verifie et corrige les liens (mode normal)
#   ./claude-sync.sh --status     # Affiche l'etat sans rien modifier
#   ./claude-sync.sh --init       # Premiere installation (copie local -> cloud)
#   ./claude-sync.sh --help       # Aide
#
# Principe : tout reste local par defaut. Seuls les elements explicitement
# lies sont synchronises. Aucun fichier dangereux (locks, transcripts, debug)
# ne quitte la machine.
#
# Idempotent : peut etre execute autant de fois que necessaire.

set -euo pipefail

# ============================================
# Configuration
# ============================================
CLOUD_DIR="${CLAUDE_SYNC_CLOUD_DIR:-$HOME/Dropbox/config/claude}"
CLAUDE_DIR="$HOME/.claude"

# Elements racine a synchroniser (safe, petits, rarement ecrits)
ROOT_ITEMS=("commands" "plugins" "plans" "settings.json")

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Compteurs
LINKS_OK=0
LINKS_CREATED=0
LINKS_BROKEN=0
WARNINGS=0

# ============================================
# Fonctions
# ============================================

usage() {
    cat << 'EOF'
claude-sync.sh — Synchronise les fichiers Claude Code entre machines

USAGE:
  ./claude-sync.sh              Mode normal : verifie et cree les liens manquants
  ./claude-sync.sh --status     Affiche l'etat sans rien modifier
  ./claude-sync.sh --init       Premiere installation (copie local -> cloud + liens)
  ./claude-sync.sh --help       Affiche cette aide

CONFIGURATION:
  Par defaut le cloud est dans ~/Dropbox/config/claude.
  Pour changer : export CLAUDE_SYNC_CLOUD_DIR="$HOME/iCloud/config/claude"

CE QUI EST SYNCHRONISE:
  commands/                   Custom skills (ex: stx-guide.md)
  plugins/                    Plugins installes
  plans/                      Plans de session
  settings.json               Preferences utilisateur
  projects/*/memory/          Memoires persistantes de chaque projet

CE QUI RESTE LOCAL (jamais synchronise):
  ide/, tasks/                Lock files (PID machine-specific)
  debug/, telemetry/          Logs (volumineux, jetable)
  file-history/               Historique editions (ecrit constamment)
  projects/*/*.jsonl          Transcripts (355M+, conflits garantis)
  session-env/, shell-snapshots/, paste-cache/, cache/, todos/, backups/
EOF
    exit 0
}

log_ok()   { echo -e "  ${GREEN}OK${NC}     $1"; LINKS_OK=$((LINKS_OK + 1)); }
log_new()  { echo -e "  ${BLUE}NEW${NC}    $1"; LINKS_CREATED=$((LINKS_CREATED + 1)); }
log_warn() { echo -e "  ${YELLOW}WARN${NC}   $1"; WARNINGS=$((WARNINGS + 1)); }
log_err()  { echo -e "  ${RED}ERROR${NC}  $1"; LINKS_BROKEN=$((LINKS_BROKEN + 1)); }

# Verifie ou cree un lien pour un item
check_item() {
    local item="$1"
    local mode="$2"  # "status" ou "fix" ou "init"
    local source="$CLAUDE_DIR/$item"
    local target="$CLOUD_DIR/$item"

    # Cas 1 : deja un lien symbolique correct
    if [ -L "$source" ]; then
        local actual_target
        actual_target=$(readlink "$source")
        if [ "$actual_target" = "$target" ]; then
            log_ok "$item"
            return
        else
            log_warn "$item -> $actual_target (attendu: $target)"
            return
        fi
    fi

    # Cas 2 : le lien n'existe pas ou c'est un vrai dossier/fichier
    if [ "$mode" = "status" ]; then
        if [ -e "$source" ] && [ -e "$target" ]; then
            log_warn "$item — existe localement ET dans le cloud (merge necessaire)"
        elif [ -e "$source" ]; then
            log_warn "$item — local seulement (pas de lien, pas dans le cloud)"
        elif [ -e "$target" ]; then
            log_warn "$item — dans le cloud mais pas lie localement"
        else
            log_warn "$item — n'existe nulle part"
        fi
        return
    fi

    # Mode fix ou init : creer le lien
    if [ -e "$source" ] && [ ! -e "$target" ]; then
        # Le contenu existe localement mais pas dans le cloud -> copier
        mkdir -p "$(dirname "$target")"
        cp -a "$source" "$target"
        mv "$source" "${source}.bak"
        ln -s "$target" "$source"
        log_new "$item (copie vers cloud + lien cree, backup: .bak)"
    elif [ ! -e "$source" ] && [ -e "$target" ]; then
        # Le contenu existe dans le cloud mais pas localement -> lier
        mkdir -p "$(dirname "$source")"
        ln -s "$target" "$source"
        log_new "$item (lien cree depuis cloud)"
    elif [ -e "$source" ] && [ -e "$target" ]; then
        # Les deux existent -> signaler le conflit, ne pas toucher
        log_warn "$item — CONFLIT: existe localement ET dans le cloud"
        log_warn "  Local: $source"
        log_warn "  Cloud: $target"
        log_warn "  Action: comparer manuellement, supprimer le local, puis relancer"
    else
        # Rien n'existe -> rien a faire
        if [ "$mode" = "init" ]; then
            log_ok "$item (n'existe pas encore — sera lie a la creation)"
        fi
    fi
}

# Detecte les nouveaux projets avec memory/ non lies
scan_projects() {
    local mode="$1"

    # Projets locaux avec memory/
    for proj_dir in "$CLAUDE_DIR"/projects/*/; do
        [ -d "$proj_dir" ] || continue
        proj_name=$(basename "$proj_dir")
        mem_dir="$proj_dir/memory"

        if [ -d "$mem_dir" ] || [ -L "$mem_dir" ]; then
            check_item "projects/$proj_name/memory" "$mode"
        fi
    done

    # Projets dans le cloud qui n'existent pas localement
    if [ -d "$CLOUD_DIR/projects" ]; then
        for cloud_mem in "$CLOUD_DIR"/projects/*/memory/; do
            [ -d "$cloud_mem" ] || continue
            proj_name=$(basename "$(dirname "$cloud_mem")")
            local_proj="$CLAUDE_DIR/projects/$proj_name"

            if [ ! -d "$local_proj" ]; then
                mkdir -p "$local_proj"
                check_item "projects/$proj_name/memory" "$mode"
            fi
        done
    fi
}

# ============================================
# Main
# ============================================

MODE="fix"
case "${1:-}" in
    --status) MODE="status" ;;
    --init)   MODE="init" ;;
    --help)   usage ;;
    "")       MODE="fix" ;;
    *)        echo "Option inconnue: $1"; usage ;;
esac

echo ""
echo "========================================"
echo "  Claude Code Sync"
echo "========================================"
echo "  Cloud:  $CLOUD_DIR"
echo "  Local:  $CLAUDE_DIR"
echo "  Mode:   $MODE"
echo "========================================"
echo ""

# Verifier les prerequis
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "ERREUR: $CLAUDE_DIR n'existe pas. Claude Code n'est pas installe."
    exit 1
fi

if [ "$MODE" != "status" ] && [ ! -d "$(dirname "$CLOUD_DIR")" ]; then
    echo "ERREUR: Le dossier parent de $CLOUD_DIR n'existe pas."
    echo "Verifier que Dropbox est installe et synchronise."
    exit 1
fi

if [ "$MODE" != "status" ]; then
    mkdir -p "$CLOUD_DIR/projects"
fi

# Verifier les elements racine
echo "--- Elements racine ---"
for item in "${ROOT_ITEMS[@]}"; do
    check_item "$item" "$MODE"
done

# Verifier les memoires projets
echo ""
echo "--- Memoires projets ---"
scan_projects "$MODE"

# Resume
echo ""
echo "========================================"
echo "  Resume"
echo "========================================"
echo -e "  ${GREEN}OK${NC}      : $LINKS_OK"
echo -e "  ${BLUE}Crees${NC}   : $LINKS_CREATED"
echo -e "  ${YELLOW}Warnings${NC}: $WARNINGS"
echo -e "  ${RED}Erreurs${NC} : $LINKS_BROKEN"
echo ""

if [ $WARNINGS -gt 0 ] && [ "$MODE" = "status" ]; then
    echo "  Conseil: relancer sans --status pour creer les liens manquants"
    echo "  Les conflits doivent etre resolus manuellement."
    echo ""
fi

if [ $LINKS_CREATED -gt 0 ]; then
    echo "  Backups locaux (.bak) crees. Apres verification, supprimer avec:"
    echo "  find $CLAUDE_DIR -maxdepth 4 -name '*.bak' -exec rm -rf {} +"
    echo ""
fi

# Verifier s'il reste des .bak a nettoyer
bak_count=$(find "$CLAUDE_DIR" -maxdepth 4 -name "*.bak" 2>/dev/null | wc -l | tr -d ' ')
if [ "$bak_count" -gt 0 ]; then
    echo "  Note: $bak_count backup(s) .bak en attente de nettoyage"
    find "$CLAUDE_DIR" -maxdepth 4 -name "*.bak" -exec echo "    {}" \;
    echo ""
fi

exit $LINKS_BROKEN
