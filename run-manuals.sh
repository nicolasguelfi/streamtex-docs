#!/usr/bin/env bash

# StreamTeX Manuals Launcher
# Paramétrable pour lancer les manuels en parallèle
# Usage: ./run-manuals.sh [OPTIONS]
# Options:
#   --help               Affiche cette aide
#   --all                Lance les 8 manuels (défaut)
#   --collection         Lance que le hub collection (port 8501)
#   --intro              Lance que le manuel intro (port 8502)
#   --advanced           Lance que le manuel advanced (port 8503)
#   --deployment         Lance que le guide de déploiement (port 8504)
#   --developer          Lance que le manuel développeur (port 8505)
#   --ai                 Lance que le manuel AI (port 8506)
#   --ce                 Lance que le manuel CE (port 8507)
#   --patterns           Lance que le manuel patterns (port 8508)
#   --ports P1,P2,P3,P4,P5,P6,P7,P8  Ports personnalisés (défaut: 8501..8508)
#   --no-intro           Exclut le manuel intro
#   --no-advanced        Exclut le manuel advanced
#   --no-collection      Exclut la collection
#   --no-deployment      Exclut le guide de déploiement
#   --no-developer       Exclut le manuel développeur
#   --no-ai              Exclut le manuel AI
#   --no-ce              Exclut le manuel CE
#   --no-patterns        Exclut le manuel patterns
#   --kill               Tue tous les processus Streamlit lancés
#   --watch              Lance et regarde les logs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTION_PROJECT="$SCRIPT_DIR/manuals/stx_manuals_collection"
INTRO_PROJECT="$SCRIPT_DIR/manuals/stx_manual_intro"
ADVANCED_PROJECT="$SCRIPT_DIR/manuals/stx_manual_advanced"
DEPLOYMENT_PROJECT="$SCRIPT_DIR/manuals/stx_manual_deploy"
DEVELOPER_PROJECT="$SCRIPT_DIR/manuals/stx_manual_developer"
AI_PROJECT="$SCRIPT_DIR/manuals/stx_manual_ai"
CE_PROJECT="$SCRIPT_DIR/manuals/stx_manual_ce"
PATTERNS_PROJECT="$SCRIPT_DIR/manuals/stx_manual_patterns"

# Ports par défaut
COLLECTION_PORT=8501
INTRO_PORT=8502
ADVANCED_PORT=8503
DEPLOYMENT_PORT=8504
DEVELOPER_PORT=8505
AI_PORT=8506
CE_PORT=8507
PATTERNS_PORT=8508

# Flags pour les manuels à lancer
LAUNCH_COLLECTION=true
LAUNCH_INTRO=true
LAUNCH_ADVANCED=true
LAUNCH_DEPLOYMENT=true
LAUNCH_DEVELOPER=true
LAUNCH_AI=true
LAUNCH_CE=true
LAUNCH_PATTERNS=true

WATCH_MODE=false

# Parse les arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            cat << 'EOF'
StreamTeX Manuals Launcher

USAGE:
  ./run-manuals.sh [OPTIONS]

OPTIONS:
  --all              Lance les 8 manuels (défaut)
  --collection       Lance que le hub collection (port 8501)
  --intro            Lance que le manuel intro (port 8502)
  --advanced         Lance que le manuel advanced (port 8503)
  --deployment       Lance que le guide de déploiement (port 8504)
  --developer        Lance que le manuel développeur (port 8505)
  --ai               Lance que le manuel AI (port 8506)
  --ce               Lance que le manuel CE (port 8507)
  --patterns         Lance que le manuel patterns (port 8508)

  --no-intro         Exclut le manuel intro
  --no-advanced      Exclut le manuel advanced
  --no-collection    Exclut la collection
  --no-deployment    Exclut le guide de déploiement
  --no-developer     Exclut le manuel développeur
  --no-ai            Exclut le manuel AI
  --no-ce            Exclut le manuel CE
  --no-patterns      Exclut le manuel patterns

  --ports P1,P2,P3,P4,P5,P6,P7,P8  Ports personnalisés (défaut: 8501..8508)
  --kill             Tue tous les processus Streamlit lancés
  --watch            Lance et regarde les logs (Ctrl+C pour quitter)
  --help             Affiche cette aide

EXAMPLES:
  # Lance tout (défaut)
  ./run-manuals.sh

  # Lance que le manuel intro
  ./run-manuals.sh --intro

  # Lance que le manuel développeur
  ./run-manuals.sh --developer

  # Lance que le guide de déploiement
  ./run-manuals.sh --deployment

  # Lance collection et advanced sur ports 9001, 9003
  ./run-manuals.sh --no-intro --no-deployment --no-developer --ports 9001,_,9003,_,_

  # Tue tous les Streamlit
  ./run-manuals.sh --kill

  # Lance avec watch des logs
  ./run-manuals.sh --watch

URLs:
  Collection: http://localhost:8501
  Intro:      http://localhost:8502
  Advanced:   http://localhost:8503
  Deployment: http://localhost:8504
  Developer:  http://localhost:8505
  AI:         http://localhost:8506
  CE:         http://localhost:8507
  Patterns:   http://localhost:8508
EOF
            exit 0
            ;;
        --all)
            LAUNCH_COLLECTION=true
            LAUNCH_INTRO=true
            LAUNCH_ADVANCED=true
            LAUNCH_DEPLOYMENT=true
            LAUNCH_DEVELOPER=true
            LAUNCH_AI=true
            LAUNCH_CE=true
            LAUNCH_PATTERNS=true
            shift
            ;;
        --collection)
            LAUNCH_COLLECTION=true
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --intro)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=true
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --advanced)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=true
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --deployment)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=true
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --developer)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=true
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --ai)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=true
            LAUNCH_CE=false
            LAUNCH_PATTERNS=false
            shift
            ;;
        --ce)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=true
            LAUNCH_PATTERNS=false
            shift
            ;;
        --patterns)
            LAUNCH_COLLECTION=false
            LAUNCH_INTRO=false
            LAUNCH_ADVANCED=false
            LAUNCH_DEPLOYMENT=false
            LAUNCH_DEVELOPER=false
            LAUNCH_AI=false
            LAUNCH_CE=false
            LAUNCH_PATTERNS=true
            shift
            ;;
        --no-intro)
            LAUNCH_INTRO=false
            shift
            ;;
        --no-advanced)
            LAUNCH_ADVANCED=false
            shift
            ;;
        --no-collection)
            LAUNCH_COLLECTION=false
            shift
            ;;
        --no-deployment)
            LAUNCH_DEPLOYMENT=false
            shift
            ;;
        --no-developer)
            LAUNCH_DEVELOPER=false
            shift
            ;;
        --no-ai)
            LAUNCH_AI=false
            shift
            ;;
        --no-ce)
            LAUNCH_CE=false
            shift
            ;;
        --no-patterns)
            LAUNCH_PATTERNS=false
            shift
            ;;
        --ports)
            IFS=',' read -r COLLECTION_PORT INTRO_PORT ADVANCED_PORT DEPLOYMENT_PORT DEVELOPER_PORT AI_PORT CE_PORT PATTERNS_PORT <<< "$2"
            # Remplacer '_' par le port par défaut
            [ "$COLLECTION_PORT" = "_" ] && COLLECTION_PORT=8501
            [ "$INTRO_PORT" = "_" ] && INTRO_PORT=8502
            [ "$ADVANCED_PORT" = "_" ] && ADVANCED_PORT=8503
            [ "$DEPLOYMENT_PORT" = "_" ] && DEPLOYMENT_PORT=8504
            [ "$DEVELOPER_PORT" = "_" ] && DEVELOPER_PORT=8505
            [ "$AI_PORT" = "_" ] || [ -z "$AI_PORT" ] && AI_PORT=8506
            [ "$CE_PORT" = "_" ] || [ -z "$CE_PORT" ] && CE_PORT=8507
            [ "$PATTERNS_PORT" = "_" ] || [ -z "$PATTERNS_PORT" ] && PATTERNS_PORT=8508
            shift 2
            ;;
        --kill)
            echo "Arrêt de tous les processus Streamlit..."
            pkill -f "streamlit run" || true
            sleep 1
            echo "Fait"
            exit 0
            ;;
        --watch)
            WATCH_MODE=true
            shift
            ;;
        *)
            echo "Option inconnue: $1"
            echo "Utilisez --help pour voir les options disponibles"
            exit 1
            ;;
    esac
done

# Vérifier que les manuels existent
check_project() {
    local project_path=$1
    local project_name=$2
    if [ ! -d "$project_path" ]; then
        echo "Le manuel $project_name n'existe pas: $project_path"
        exit 1
    fi
    if [ ! -f "$project_path/book.py" ]; then
        echo "book.py introuvable dans $project_name"
        exit 1
    fi
}

[ "$LAUNCH_COLLECTION" = true ] && check_project "$COLLECTION_PROJECT" "collection"
[ "$LAUNCH_INTRO" = true ] && check_project "$INTRO_PROJECT" "intro"
[ "$LAUNCH_ADVANCED" = true ] && check_project "$ADVANCED_PROJECT" "advanced"
[ "$LAUNCH_DEPLOYMENT" = true ] && check_project "$DEPLOYMENT_PROJECT" "deployment"
[ "$LAUNCH_DEVELOPER" = true ] && check_project "$DEVELOPER_PROJECT" "developer"
[ "$LAUNCH_AI" = true ] && check_project "$AI_PROJECT" "ai"
[ "$LAUNCH_CE" = true ] && check_project "$CE_PROJECT" "ce"
[ "$LAUNCH_PATTERNS" = true ] && check_project "$PATTERNS_PROJECT" "patterns"

# Logs
LOG_DIR="/tmp/streamtex-manuals"
mkdir -p "$LOG_DIR"
COLLECTION_LOG="$LOG_DIR/collection.log"
INTRO_LOG="$LOG_DIR/intro.log"
ADVANCED_LOG="$LOG_DIR/advanced.log"
DEPLOYMENT_LOG="$LOG_DIR/deployment.log"
DEVELOPER_LOG="$LOG_DIR/developer.log"
AI_LOG="$LOG_DIR/ai.log"
CE_LOG="$LOG_DIR/ce.log"
PATTERNS_LOG="$LOG_DIR/patterns.log"

# Fonction pour afficher les PID
print_pids() {
    echo ""
    echo "==========================================================="
    echo "StreamTeX Manuals Running"
    echo "==========================================================="
    [ "$LAUNCH_COLLECTION" = true ] && echo "  Collection:  http://localhost:$COLLECTION_PORT (PID: $(pgrep -f "stx_manuals_collection" | head -1 || echo '—'))"
    [ "$LAUNCH_INTRO" = true ] && echo "  Intro:       http://localhost:$INTRO_PORT (PID: $(pgrep -f "stx_manual_intro" | head -1 || echo '—'))"
    [ "$LAUNCH_AI" = true ] && echo "  AI:          http://localhost:$AI_PORT (PID: $(pgrep -f "stx_manual_ai" | head -1 || echo '—'))"
    [ "$LAUNCH_ADVANCED" = true ] && echo "  Advanced:    http://localhost:$ADVANCED_PORT (PID: $(pgrep -f "stx_manual_advanced" | head -1 || echo '—'))"
    [ "$LAUNCH_DEPLOYMENT" = true ] && echo "  Deployment:  http://localhost:$DEPLOYMENT_PORT (PID: $(pgrep -f "stx_manual_deploy" | head -1 || echo '—'))"
    [ "$LAUNCH_DEVELOPER" = true ] && echo "  Developer:   http://localhost:$DEVELOPER_PORT (PID: $(pgrep -f "stx_manual_developer" | head -1 || echo '—'))"
    [ "$LAUNCH_CE" = true ] && echo "  CE:          http://localhost:$CE_PORT (PID: $(pgrep -f "stx_manual_ce" | head -1 || echo '—'))"
    [ "$LAUNCH_PATTERNS" = true ] && echo "  Patterns:    http://localhost:$PATTERNS_PORT (PID: $(pgrep -f "stx_manual_patterns" | head -1 || echo '—'))"
    echo ""
    echo "Logs: $LOG_DIR"
    [ "$WATCH_MODE" = false ] && echo "Utilisez --kill pour arrêter tous les processus"
    echo "==========================================================="
    echo ""
}

# Libère un port en tuant les processus serveur qui l'occupent
free_port() {
    local port=$1
    local pids
    pids=$(lsof -ti :"$port" -sTCP:LISTEN 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo "   Port $port occupé (PIDs: $pids) — arrêt des processus..."
        echo "$pids" | xargs kill 2>/dev/null || true
        sleep 2
    fi
}

# Lance un manuel
launch_project() {
    local project_path=$1
    local project_name=$2
    local port=$3
    local log_file=$4

    echo "Lancement $project_name (port $port)..."
    free_port "$port"

    cd "$SCRIPT_DIR"
    nohup uv run streamlit run "$project_path/book.py" \
        --server.port "$port" \
        --server.headless true \
        --logger.level=warning \
        > "$log_file" 2>&1 &

    local pid=$!
    sleep 2

    if ps -p $pid > /dev/null 2>&1; then
        echo "   $project_name lancé (PID: $pid)"
    else
        echo "   Erreur au lancement de $project_name"
        echo "   Logs: $log_file"
        tail -20 "$log_file"
        return 1
    fi
}

# Tue tous les processus liés
cleanup() {
    echo ""
    echo "Arrêt des manuels..."
    pkill -f "stx_manuals_collection\|stx_manual_intro\|stx_manual_advanced\|stx_manual_deploy\|stx_manual_developer\|stx_manual_ai\|stx_manual_ce\|stx_manual_patterns" || true
    pkill -f "streamlit run.*stx_manuals_collection\|streamlit run.*stx_manual_intro\|streamlit run.*stx_manual_advanced\|streamlit run.*stx_manual_deploy\|streamlit run.*stx_manual_developer\|streamlit run.*stx_manual_ai\|streamlit run.*stx_manual_ce\|streamlit run.*stx_manual_patterns" || true
    sleep 1
    echo "Tous les manuels ont été arrêtés"
}

# Configuration de cleanup au CTRL+C
trap cleanup INT

# Lance les manuels
echo "StreamTeX Manuals Launcher"
echo "=================================="
echo ""

if [ "$LAUNCH_COLLECTION" = true ]; then
    launch_project "$COLLECTION_PROJECT" "Collection" "$COLLECTION_PORT" "$COLLECTION_LOG"
fi

if [ "$LAUNCH_INTRO" = true ]; then
    launch_project "$INTRO_PROJECT" "Intro" "$INTRO_PORT" "$INTRO_LOG"
fi

if [ "$LAUNCH_AI" = true ]; then
    launch_project "$AI_PROJECT" "AI" "$AI_PORT" "$AI_LOG"
fi

if [ "$LAUNCH_ADVANCED" = true ]; then
    launch_project "$ADVANCED_PROJECT" "Advanced" "$ADVANCED_PORT" "$ADVANCED_LOG"
fi

if [ "$LAUNCH_DEPLOYMENT" = true ]; then
    launch_project "$DEPLOYMENT_PROJECT" "Deployment" "$DEPLOYMENT_PORT" "$DEPLOYMENT_LOG"
fi

if [ "$LAUNCH_DEVELOPER" = true ]; then
    launch_project "$DEVELOPER_PROJECT" "Developer" "$DEVELOPER_PORT" "$DEVELOPER_LOG"
fi

if [ "$LAUNCH_CE" = true ]; then
    launch_project "$CE_PROJECT" "CE" "$CE_PORT" "$CE_LOG"
fi

if [ "$LAUNCH_PATTERNS" = true ]; then
    launch_project "$PATTERNS_PROJECT" "Patterns" "$PATTERNS_PORT" "$PATTERNS_LOG"
fi

print_pids

# Attendre si en watch mode
if [ "$WATCH_MODE" = true ]; then
    echo "Mode watch activé. Appuyez sur Ctrl+C pour quitter."
    echo ""

    while true; do
        sleep 5
        # Vérifier que les processus tournent toujours
        if [ "$LAUNCH_COLLECTION" = true ] && ! pgrep -f "streamlit run.*stx_manuals_collection" > /dev/null 2>&1; then
            echo "Collection est arrêté. Redémarrage..."
            launch_project "$COLLECTION_PROJECT" "Collection" "$COLLECTION_PORT" "$COLLECTION_LOG"
        fi
        if [ "$LAUNCH_INTRO" = true ] && ! pgrep -f "streamlit run.*stx_manual_intro" > /dev/null 2>&1; then
            echo "Intro est arrêté. Redémarrage..."
            launch_project "$INTRO_PROJECT" "Intro" "$INTRO_PORT" "$INTRO_LOG"
        fi
        if [ "$LAUNCH_AI" = true ] && ! pgrep -f "streamlit run.*stx_manual_ai" > /dev/null 2>&1; then
            echo "AI est arrêté. Redémarrage..."
            launch_project "$AI_PROJECT" "AI" "$AI_PORT" "$AI_LOG"
        fi
        if [ "$LAUNCH_ADVANCED" = true ] && ! pgrep -f "streamlit run.*stx_manual_advanced" > /dev/null 2>&1; then
            echo "Advanced est arrêté. Redémarrage..."
            launch_project "$ADVANCED_PROJECT" "Advanced" "$ADVANCED_PORT" "$ADVANCED_LOG"
        fi
        if [ "$LAUNCH_DEPLOYMENT" = true ] && ! pgrep -f "streamlit run.*stx_manual_deploy" > /dev/null 2>&1; then
            echo "Deployment est arrêté. Redémarrage..."
            launch_project "$DEPLOYMENT_PROJECT" "Deployment" "$DEPLOYMENT_PORT" "$DEPLOYMENT_LOG"
        fi
        if [ "$LAUNCH_DEVELOPER" = true ] && ! pgrep -f "streamlit run.*stx_manual_developer" > /dev/null 2>&1; then
            echo "Developer est arrêté. Redémarrage..."
            launch_project "$DEVELOPER_PROJECT" "Developer" "$DEVELOPER_PORT" "$DEVELOPER_LOG"
        fi
        if [ "$LAUNCH_CE" = true ] && ! pgrep -f "streamlit run.*stx_manual_ce" > /dev/null 2>&1; then
            echo "CE est arrêté. Redémarrage..."
            launch_project "$CE_PROJECT" "CE" "$CE_PORT" "$CE_LOG"
        fi
        if [ "$LAUNCH_PATTERNS" = true ] && ! pgrep -f "streamlit run.*stx_manual_patterns" > /dev/null 2>&1; then
            echo "Patterns est arrêté. Redémarrage..."
            launch_project "$PATTERNS_PROJECT" "Patterns" "$PATTERNS_PORT" "$PATTERNS_LOG"
        fi
    done
else
    # Attendre un peu puis ouvrir dans Chrome
    sleep 2
    echo "Tous les manuels sont lancés!"
    echo ""
    echo "Ouverture dans Chrome:"
    [ "$LAUNCH_COLLECTION" = true ] && echo "  Collection:  http://localhost:$COLLECTION_PORT" && open -a "Google Chrome" "http://localhost:$COLLECTION_PORT" && sleep 0.5
    [ "$LAUNCH_INTRO" = true ] && echo "  Intro:       http://localhost:$INTRO_PORT" && open -a "Google Chrome" "http://localhost:$INTRO_PORT" && sleep 0.5
    [ "$LAUNCH_AI" = true ] && echo "  AI:          http://localhost:$AI_PORT" && open -a "Google Chrome" "http://localhost:$AI_PORT" && sleep 0.5
    [ "$LAUNCH_ADVANCED" = true ] && echo "  Advanced:    http://localhost:$ADVANCED_PORT" && open -a "Google Chrome" "http://localhost:$ADVANCED_PORT" && sleep 0.5
    [ "$LAUNCH_DEPLOYMENT" = true ] && echo "  Deployment:  http://localhost:$DEPLOYMENT_PORT" && open -a "Google Chrome" "http://localhost:$DEPLOYMENT_PORT" && sleep 0.5
    [ "$LAUNCH_DEVELOPER" = true ] && echo "  Developer:   http://localhost:$DEVELOPER_PORT" && open -a "Google Chrome" "http://localhost:$DEVELOPER_PORT" && sleep 0.5
    [ "$LAUNCH_CE" = true ] && echo "  CE:          http://localhost:$CE_PORT" && open -a "Google Chrome" "http://localhost:$CE_PORT" && sleep 0.5
    [ "$LAUNCH_PATTERNS" = true ] && echo "  Patterns:    http://localhost:$PATTERNS_PORT" && open -a "Google Chrome" "http://localhost:$PATTERNS_PORT"
    echo ""
    echo "Utilisez './run-manuals.sh --kill' pour arrêter tous les manuels"
    echo ""
fi
