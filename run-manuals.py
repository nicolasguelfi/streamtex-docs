#!/usr/bin/env python3
"""StreamTeX Manuals Launcher — Cross-platform (macOS, Linux, Windows)."""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

MANUALS = {
    "collection": {"path": "manuals/stx_manuals_collection", "port": 8501},
    "intro": {"path": "manuals/stx_manual_intro", "port": 8502},
    "advanced": {"path": "manuals/stx_manual_advanced", "port": 8503},
    "deployment": {"path": "manuals/stx_manual_deploy", "port": 8504},
    "developer": {"path": "manuals/stx_manual_developer", "port": 8505},
    "ai": {"path": "manuals/stx_manual_ai", "port": 8506},
    "ce": {"path": "manuals/stx_manual_ce", "port": 8507},
}

# Display order
DISPLAY_ORDER = ["collection", "intro", "ai", "advanced", "deployment", "developer", "ce"]

LOG_DIR = Path(tempfile.gettempdir()) / "streamtex-docs-manuals"


def check_project(name: str, info: dict) -> None:
    project_path = SCRIPT_DIR / info["path"]
    if not project_path.is_dir():
        print(f"Le manuel {name} n'existe pas: {project_path}")
        sys.exit(1)
    if not (project_path / "book.py").is_file():
        print(f"book.py introuvable dans {name}")
        sys.exit(1)


def free_port(port: int) -> None:
    """Kill processes listening on the given port."""
    if sys.platform == "win32":
        try:
            result = subprocess.run(
                ["netstat", "-ano", "-p", "TCP"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    if pid.isdigit():
                        print(f"   Port {port} occupé (PID: {pid}) — arrêt...")
                        subprocess.run(["taskkill", "/F", "/PID", pid],
                                       capture_output=True, timeout=5)
        except Exception:
            pass
    else:
        try:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}", "-sTCP:LISTEN"],
                capture_output=True, text=True, timeout=5,
            )
            pids = result.stdout.strip()
            if pids:
                print(f"   Port {port} occupé (PIDs: {pids}) — arrêt des processus...")
                for pid in pids.split():
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                    except (ProcessLookupError, ValueError):
                        pass
                time.sleep(2)
        except FileNotFoundError:
            pass


def launch_project(name: str, info: dict, log_dir: Path) -> subprocess.Popen | None:
    port = info["port"]
    project_path = SCRIPT_DIR / info["path"]
    log_file = log_dir / f"{name}.log"

    print(f"Lancement {name} (port {port})...")
    free_port(port)

    with open(log_file, "w") as lf:
        proc = subprocess.Popen(
            [
                "uv", "run", "streamlit", "run",
                str(project_path / "book.py"),
                "--server.port", str(port),
                "--server.headless", "true",
                "--logger.level=warning",
            ],
            stdout=lf,
            stderr=subprocess.STDOUT,
            cwd=str(SCRIPT_DIR),
            # On Windows, create a new process group so we can kill it later
            **({} if sys.platform != "win32" else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}),
        )

    time.sleep(2)

    if proc.poll() is None:
        print(f"   {name} lancé (PID: {proc.pid})")
        return proc
    else:
        print(f"   Erreur au lancement de {name}")
        print(f"   Logs: {log_file}")
        try:
            with open(log_file) as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    print(f"   {line.rstrip()}")
        except Exception:
            pass
        return None


def kill_all() -> None:
    """Kill all streamlit processes related to StreamTeX manuals."""
    print("Arrêt de tous les processus Streamlit...")
    if sys.platform == "win32":
        try:
            result = subprocess.run(
                ["wmic", "process", "where",
                 "commandline like '%streamlit run%'",
                 "get", "processid"],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.splitlines():
                pid = line.strip()
                if pid.isdigit():
                    subprocess.run(["taskkill", "/F", "/PID", pid],
                                   capture_output=True, timeout=5)
        except Exception:
            # Fallback: try taskkill with image name
            subprocess.run(["taskkill", "/F", "/IM", "streamlit.exe"],
                           capture_output=True, timeout=5)
    else:
        try:
            subprocess.run(["pkill", "-f", "streamlit run"],
                           capture_output=True, timeout=5)
        except FileNotFoundError:
            # pkill not available, try manual approach
            pass

    time.sleep(1)
    print("Fait")


def terminate_processes(processes: list[subprocess.Popen]) -> None:
    """Gracefully terminate all managed processes."""
    print("\nArrêt des manuels...")
    for proc in processes:
        try:
            proc.terminate()
        except Exception:
            pass
    # Wait a bit then force kill survivors
    time.sleep(2)
    for proc in processes:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass
    print("Tous les manuels ont été arrêtés")


def print_status(active: dict[str, dict], log_dir: Path, watch: bool,
                 processes: dict[str, subprocess.Popen]) -> None:
    print()
    print("===========================================================")
    print("StreamTeX Manuals Running")
    print("===========================================================")
    labels = {
        "collection": "Collection:",
        "intro": "Intro:     ",
        "ai": "AI:        ",
        "advanced": "Advanced:  ",
        "deployment": "Deployment:",
        "developer": "Developer: ",
        "ce": "CE:        ",
    }
    for name in DISPLAY_ORDER:
        if name in active:
            pid = processes[name].pid if name in processes else "—"
            port = active[name]["port"]
            print(f"  {labels[name]}  http://localhost:{port} (PID: {pid})")
    print()
    print(f"Logs: {log_dir}")
    if not watch:
        print("Utilisez 'python run-manuals.py --kill' pour arrêter tous les manuels")
    print("===========================================================")
    print()


def open_in_browser(url: str) -> None:
    """Open URL in Chrome (cross-platform, fallback to default browser)."""
    if sys.platform == "darwin":
        subprocess.Popen(["open", "-a", "Google Chrome", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif sys.platform == "win32":
        # Try Chrome, fall back to default
        chrome_path = os.path.expandvars(
            r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
        )
        if os.path.isfile(chrome_path):
            subprocess.Popen([chrome_path, url],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            webbrowser.open(url)
    else:
        # Linux: try google-chrome, chromium-browser, then default
        for cmd in ("google-chrome", "chromium-browser", "chromium"):
            if shutil.which(cmd):
                subprocess.Popen([cmd, url],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="StreamTeX Manuals Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
EXAMPLES:
  # Lance tout (défaut)
  python run-manuals.py

  # Lance que le manuel intro
  python run-manuals.py --intro

  # Lance que le manuel développeur
  python run-manuals.py --developer

  # Lance collection et advanced sur ports personnalisés
  python run-manuals.py --no-intro --no-deployment --no-developer --no-ai --no-ce --ports 9001,_,9003,_,_,_,_

  # Tue tous les Streamlit
  python run-manuals.py --kill

  # Lance avec watch des logs
  python run-manuals.py --watch

URLs:
  Collection: http://localhost:8501
  Intro:      http://localhost:8502
  Advanced:   http://localhost:8503
  Deployment: http://localhost:8504
  Developer:  http://localhost:8505
  AI:         http://localhost:8506
  CE:         http://localhost:8507
""",
    )

    # Select single manual
    for name in MANUALS:
        parser.add_argument(f"--{name}", action="store_true",
                            help=f"Lance que le manuel {name}")

    # Exclude flags
    for name in MANUALS:
        parser.add_argument(f"--no-{name}", action="store_true",
                            help=f"Exclut le manuel {name}")

    parser.add_argument("--all", action="store_true",
                        help="Lance les 7 manuels (défaut)")
    parser.add_argument("--ports",
                        help="Ports personnalisés: P1,P2,P3,P4,P5,P6,P7 "
                             "(ordre: collection,intro,advanced,deployment,developer,ai,ce). "
                             "Utilisez _ pour le port par défaut.")
    parser.add_argument("--kill", action="store_true",
                        help="Tue tous les processus Streamlit lancés")
    parser.add_argument("--watch", action="store_true",
                        help="Lance et regarde les logs (Ctrl+C pour quitter)")

    args = parser.parse_args()

    # --kill
    if args.kill:
        kill_all()
        return

    # Determine which manuals to launch
    # Check if any single-manual flag was given
    single_flags = {name: getattr(args, name) for name in MANUALS}
    any_single = any(single_flags.values())

    active: dict[str, dict] = {}
    if any_single and not args.all:
        for name in MANUALS:
            if single_flags[name]:
                active[name] = dict(MANUALS[name])
    else:
        # Default: all
        for name in MANUALS:
            active[name] = dict(MANUALS[name])

    # Apply --no-* exclusions
    for name in MANUALS:
        if getattr(args, f"no_{name}"):
            active.pop(name, None)

    # Apply custom ports
    if args.ports:
        port_names = ["collection", "intro", "advanced", "deployment", "developer", "ai", "ce"]
        parts = args.ports.split(",")
        for i, part in enumerate(parts):
            if i < len(port_names):
                name = port_names[i]
                part = part.strip()
                if part and part != "_" and name in active:
                    active[name]["port"] = int(part)

    if not active:
        print("Aucun manuel sélectionné.")
        return

    # Check projects exist
    for name, info in active.items():
        check_project(name, info)

    # Prepare log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    print("StreamTeX Manuals Launcher")
    print("==================================")
    print()

    # Launch
    processes: dict[str, subprocess.Popen] = {}
    for name in DISPLAY_ORDER:
        if name in active:
            proc = launch_project(name, active[name], LOG_DIR)
            if proc:
                processes[name] = proc

    print_status(active, LOG_DIR, args.watch, processes)

    if args.watch:
        print("Mode watch activé. Appuyez sur Ctrl+C pour quitter.")
        print()

        def on_signal(*_: object) -> None:
            terminate_processes(list(processes.values()))
            sys.exit(0)

        signal.signal(signal.SIGINT, on_signal)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, on_signal)

        try:
            while True:
                time.sleep(5)
                for name in DISPLAY_ORDER:
                    if name in active and name in processes:
                        if processes[name].poll() is not None:
                            print(f"{name} est arrêté. Redémarrage...")
                            proc = launch_project(name, active[name], LOG_DIR)
                            if proc:
                                processes[name] = proc
        except KeyboardInterrupt:
            terminate_processes(list(processes.values()))
    else:
        time.sleep(2)
        print("Tous les manuels sont lancés!")
        print()
        print("Ouverture dans le navigateur:")
        labels = {
            "collection": "Collection:",
            "intro": "Intro:     ",
            "ai": "AI:        ",
            "advanced": "Advanced:  ",
            "deployment": "Deployment:",
            "developer": "Developer: ",
            "ce": "CE:        ",
        }
        for name in DISPLAY_ORDER:
            if name in active:
                url = f"http://localhost:{active[name]['port']}"
                print(f"  {labels[name]}  {url}")
                open_in_browser(url)
                time.sleep(0.5)
        print()
        print("Utilisez 'python run-manuals.py --kill' pour arrêter tous les manuels")
        print()


if __name__ == "__main__":
    main()
