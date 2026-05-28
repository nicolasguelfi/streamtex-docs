# shellcheck shell=bash
# ============================================================================
# stx-cheatsheet.sh — mémo + helpers pour travailler avec stx
# ============================================================================
#
# DOUBLE USAGE
#   Lisez-moi comme un mémo (ouvert dans un éditeur)
#   OU sourcez-moi pour activer les fonctions :
#     source ~/path/to/streamtex-dev/stx-cheatsheet.sh
#
# CONTEXTE
#   - dev source (les 3 repos clones git) :
#       $STX_DEV_ROOT/streamtex
#       $STX_DEV_ROOT/streamtex-claude
#       $STX_DEV_ROOT/streamtex-docs
#   - dev-link global (1 fois par machine) :
#       ~/.config/streamtex/dev.json
#   - workspaces utilisateur : n'importe où, contiennent stx.toml + projects/
#
# ============================================================================

# Racine des repos source (modifiez si vous déplacez le dossier)
export STX_DEV_ROOT="/Volumes/Mac_Data/Win_data/data/backups/Dropbox-nicolas.guelfi@laposte.net/messir Dropbox/Nicolas Guelfi/users/NG/dev-dropbox/dvlpt/eclipse/git/github/streamtex-dev"


# ============================================================================
# SECTION 1 — Setup machine (à faire UNE fois)
# ============================================================================

# Enregistre les 3 sources comme dev-links globaux + installe stx en éditable.
# À relancer si vous déplacez les repos ou changez de machine.
stx-dev-setup() {
  stx dev register streamtex        "$STX_DEV_ROOT/streamtex"        || return 1
  stx dev register streamtex-claude "$STX_DEV_ROOT/streamtex-claude" || return 1
  stx dev register streamtex-docs   "$STX_DEV_ROOT/streamtex-docs"   || return 1
  uv tool install --editable --reinstall --with "streamtex[cli]" "$STX_DEV_ROOT/streamtex"
  stx dev status
}

# Réinstalle uniquement le binaire stx en éditable (après un git pull dans streamtex/).
stx-dev-reinstall() {
  uv tool install --editable --reinstall --with "streamtex[cli]" "$STX_DEV_ROOT/streamtex"
}


# ============================================================================
# SECTION 2 — Dev sur le code streamtex (la lib Python)
# ============================================================================

# Lance les tests du package streamtex.
# Usage : stx-test                       # tous
#         stx-test -k mon_test           # filtre
#         stx-test tests/test_foo.py -v  # fichier spécifique
stx-test() {
  ( cd "$STX_DEV_ROOT/streamtex" && uv run pytest "${@:-tests/}" )
}

# Lint + auto-fix sur le code streamtex.
# Usage : stx-lint           # check seul
#         stx-lint --fix     # auto-fix
stx-lint() {
  ( cd "$STX_DEV_ROOT/streamtex" && uv run ruff check streamtex/ "$@" )
}

# Ouvre un shell dans le dev source streamtex (pour git, édition, etc.)
stx-cd-lib()    { cd "$STX_DEV_ROOT/streamtex"; }
stx-cd-claude() { cd "$STX_DEV_ROOT/streamtex-claude"; }
stx-cd-docs()   { cd "$STX_DEV_ROOT/streamtex-docs"; }


# ============================================================================
# SECTION 3 — Dev sur les profils Claude / templates docs
# ============================================================================
#
# RAPPEL : `.claude/` d'un projet est une COPIE des fichiers de
# streamtex-claude. Modifier la source ne se reflète pas auto. Re-syncer
# avec les helpers ci-dessous.

# Re-sync .claude/ de TOUS les projets du workspace courant depuis la source.
# Préserve les modifications locales (sauf --force).
# Usage : stx-claude-sync            # sync, préserve modifs locales
#         stx-claude-sync --force    # overwrite (backup auto dans .claude/.backup/)
stx-claude-sync() {
  stx claude update --all "$@"
}

# Affiche le diff entre source streamtex-claude et le projet courant.
stx-claude-diff() {
  stx claude diff "${1:-.}"
}

# Vérifie l'état de sync de tous les projets du workspace.
stx-claude-check() {
  stx claude check
}


# ============================================================================
# SECTION 4 — Workflow utilisateur : créer / utiliser un workspace
# ============================================================================

# Crée un nouveau workspace + projet avec template, depuis zéro.
# Usage : stx-new <nom-workspace> [nom-projet] [template]
#   nom-projet : défaut = nom-workspace
#   template   : project (défaut) | collection | slides
# Exemple : stx-new mon-cours hello-world project
stx-new() {
  local ws="${1:?usage: stx-new <workspace> [project] [template]}"
  local proj="${2:-$ws}"
  local tpl="${3:-project}"
  mkdir -p "$ws" && cd "$ws" || return 1
  stx install --preset power --project "$proj" --template "$tpl"
}

# Variante dev : pareil que stx-new mais auto-link streamtex dev source
# dans le projet (via --dev). Requiert: stx dev register streamtex <path> au préalable.
# Usage : stx-new-dev <nom-workspace> [nom-projet] [template]
stx-new-dev() {
  local ws="${1:?usage: stx-new-dev <workspace> [project] [template]}"
  local proj="${2:-$ws}"
  local tpl="${3:-project}"
  mkdir -p "$ws" && cd "$ws" || return 1
  stx install --preset power --project "$proj" --template "$tpl" --dev
}

# Ajoute un projet à un workspace existant (à lancer depuis la racine du workspace).
# Usage : stx-add-project <nom-projet> [template]
#         stx-add-project <nom-projet> [template] --dev    # avec auto-link streamtex
stx-add-project() {
  local proj="${1:?usage: stx-add-project <name> [template] [--dev]}"
  local tpl="${2:-project}"
  shift; [[ $# -gt 0 ]] && shift   # consume project + template, keep extra flags (e.g. --dev)
  stx install --project "$proj" --template "$tpl" "$@"
}

# Lance le serveur Streamlit du projet courant (équivalent stx run).
# Usage : stx-up                    # depuis un dossier projet
stx-up() {
  stx run "$@"
}


# ============================================================================
# SECTION 4bis — Reuse architecture (packs / components / kits / DS)
# ============================================================================
#
# IMPORTANT : ces commandes INTROSPECTENT le venv du projet (elles lisent les
# entry points Python installés). Elles passent donc TOUTES par `uv run stx`
# pour s'exécuter dans le venv du projet, pas dans celui du binaire global.
# (Le `stx` global ne verrait pas les packs installés dans ./.venv — il
# afficherait un avertissement de divergence, cf. SECTION 5.)
# À lancer depuis un dossier PROJET (là où vivent stx.toml + ./.venv).

# Ajoute un pack au projet courant puis l'installe.
# Usage : stx-pack-add git:https://github.com/nicolasguelfi/streamtex-packs#subdirectory=streamtex-pack-design
#         stx-pack-add local:../mon-pack
#         stx-pack-add pypi:streamtex-pack-x@'>=0.1,<0.2'
stx-pack-add() { uv run stx pack add "$@" && uv run stx pack sync && uv sync; }

# Re-synchronise les packs déclarés dans stx.toml + applique via uv.
stx-pack-sync() { uv run stx pack sync && uv sync; }

# Liste les packs actifs (+ état lifecycle avec --trace).
stx-pack-ls() { uv run stx pack list "$@"; }

# Liste / inspecte les composants disponibles.
# Usage : stx-comp-ls                 # tous
#         stx-comp-ls --pack <nom>    # filtré
#         stx-comp-show callout       # docstring §4.1 (INVARIANTS/PARAMS/INTERDITS)
stx-comp-ls()   { uv run stx component list "$@"; }
stx-comp-show() { uv run stx component show "$@"; }

# Design systems disponibles.
stx-ds-ls() { uv run stx ds list; }

# Kits : liste + installation (DS + composants curés).
# Usage : stx-kit-ls
#         stx-kit-install streamtex-pack-design:course-default
stx-kit-ls()      { uv run stx kit list; }
stx-kit-install() { uv run stx kit install "$@" && uv sync; }

# Validation agrégée de la reuse architecture (errors/warnings).
stx-pack-validate() { uv run stx validate "$@"; }


# ============================================================================
# SECTION 5 — Diagnostics
# ============================================================================
#
# NOTE — Avertissement de divergence de version :
#   Si tu lances une commande d'introspection (`stx pack/component/kit/ds
#   list|validate`) avec le `stx` GLOBAL alors que le venv du projet a une
#   version de streamtex différente, stx affiche un avertissement + un prompt
#   [y]es/[n]o/ne[v]er. Deux résolutions :
#     - utilise `uv run stx ...` (helpers SECTION 4bis) → bon venv, pas de warning
#     - `stx dev link streamtex` → aligne le projet sur la source dev du tool
#   `stx-which` ci-dessous diagnostique le cas voisin "binaire figé vs éditable".

# Vue d'ensemble : workspace + repos + dev-links + version + santé.
stx-info() {
  echo "=== stx dev status ==="
  stx dev status
  echo
  echo "=== stx status ==="
  stx status
}

# Vérifie où est le binaire stx et quelle copie du package il charge.
# Sert à diagnostiquer "mon fix n'apparaît pas" → install figée vs éditable.
stx-which() {
  local bin py pkg
  bin=$(which stx)
  echo "binary : $bin"
  py=$(head -1 "$bin" | sed 's|^#!||')
  echo "python : $py"
  pkg=$("$py" -c "import streamtex; print(streamtex.__file__)" 2>/dev/null)
  echo "package: $pkg"
  if [[ "$pkg" == "$STX_DEV_ROOT"/* ]]; then
    echo "→ EDITABLE (pointe vers la source dev) ✓"
  else
    echo "→ FIGÉ (re-run stx-dev-reinstall pour passer en éditable)"
  fi
}


# ============================================================================
# SECTION 6 — Cycle de release lib (avancé)
# ============================================================================

# Vérifie que le package est prêt pour publication PyPI.
stx-publish-check() {
  ( cd "$STX_DEV_ROOT/streamtex" && stx publish check "$@" )
}

# Publish vers TestPyPI d'abord, puis PyPI.
# Usage : stx-publish-test           # TestPyPI
#         stx-publish-prod           # PyPI réel
stx-publish-test() {
  ( cd "$STX_DEV_ROOT/streamtex" && stx publish pypi --test "$@" )
}
stx-publish-prod() {
  ( cd "$STX_DEV_ROOT/streamtex" && stx publish pypi "$@" )
}


# ============================================================================
# AIDE
# ============================================================================

# Liste toutes les fonctions stx-* disponibles.
stx-help() {
  cat <<'EOF'
Fonctions disponibles (source stx-cheatsheet.sh d'abord) :

  Setup machine
    stx-dev-setup                   Register dev-links + install stx editable (1x)
    stx-dev-reinstall               Réinstall stx éditable (après git pull)

  Dev streamtex
    stx-test [args]                 pytest sur la lib
    stx-lint [--fix]                ruff check
    stx-cd-lib / -claude / -docs    cd dans les dev sources

  Dev profils Claude
    stx-claude-sync [--force]       Re-sync .claude/ de tous les projets du WS
    stx-claude-diff [path]          Diff source vs projet
    stx-claude-check                Statut de sync

  Workflow utilisateur
    stx-new <ws> [proj] [tpl]       Crée workspace + projet
    stx-new-dev <ws> [proj] [tpl]   Idem, + auto-link streamtex dev source (--dev)
    stx-add-project <name> [tpl]    Ajoute projet à workspace existant
                                    (passer --dev en dernier pour auto-link)
    stx-up                          Lance streamlit (depuis un projet)

  Reuse architecture (depuis un projet ; via `uv run stx`)
    stx-pack-add <ref>              Ajoute + installe un pack (git/local/pypi)
    stx-pack-sync                   Re-sync les packs + uv sync
    stx-pack-ls [--trace]           Liste les packs actifs
    stx-comp-ls [--pack <nom>]      Liste les composants
    stx-comp-show <nom>             Docstring §4.1 d'un composant
    stx-ds-ls                       Liste les design systems
    stx-kit-ls                      Liste les kits
    stx-kit-install <pack>:<kit>    Installe un kit + uv sync
    stx-pack-validate [--strict]    Validation agrégée

  Diagnostics
    stx-info                        Vue d'ensemble (dev status + status)
    stx-which                       Vérifie quelle copie de stx tourne
                                    (voir aussi : note divergence en SECTION 5)

  Release (avancé)
    stx-publish-check               Pre-flight publication
    stx-publish-test                Publish TestPyPI
    stx-publish-prod                Publish PyPI

EOF
}
