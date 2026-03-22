#!/usr/bin/env python3
"""StreamTeX Ecosystem Dashboard — global status overview.

Usage:
    python3 stx-dashboard.py          # full dashboard
    python3 stx-dashboard.py --quick  # skip slow checks (SSH, URL probes)
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPT_DIR.parent
REPOS = {
    "streamtex": WORKSPACE / "streamtex",
    "streamtex-docs": WORKSPACE / "streamtex-docs",
    "streamtex-claude": WORKSPACE / "streamtex-claude",
}
ENV_FILE = WORKSPACE / "streamtex" / ".env"
COOLIFY_URL = "https://coolify.streamtex.org"
HETZNER_IP = "138.199.148.59"
SSH_KEY = Path.home() / ".ssh" / "hetzner_streamtex"

PROD_URLS = {
    "docs": "https://docs.streamtex.org",
    "docs-intro": "https://docs-intro.streamtex.org",
    "docs-advanced": "https://docs-advanced.streamtex.org",
    "docs-deploy": "https://docs-deploy.streamtex.org",
    "docs-developer": "https://docs-developer.streamtex.org",
    "docs-ai": "https://docs-ai.streamtex.org",
    "staging": "https://docs-staging.streamtex.org",
}

# ── Helpers ────────────────────────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"


def ok(text):
    return f"{GREEN}{text}{RESET}"


def warn(text):
    return f"{YELLOW}{text}{RESET}"


def err(text):
    return f"{RED}{text}{RESET}"


def dim(text):
    return f"{DIM}{text}{RESET}"


def bold(text):
    return f"{BOLD}{text}{RESET}"


def header(title):
    w = 60
    print(f"\n{CYAN}{'─' * w}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{'─' * w}{RESET}")


def run(cmd, cwd=None, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def load_env():
    tokens = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                tokens[k.strip()] = v.strip()
    return tokens


# ── Sections ───────────────────────────────────────────────────────────────
def section_local():
    header("LOCAL REPOSITORIES")
    for name, path in REPOS.items():
        if not path.exists():
            print(f"  {name:20s}  {err('not found')}")
            continue
        branch = run(["git", "branch", "--show-current"], cwd=path) or "?"
        dirty = run(["git", "status", "--porcelain"], cwd=path)
        dirty_flag = warn(" [modified]") if dirty else ok(" [clean]")
        ahead = run(["git", "rev-list", "--count", "HEAD...@{u}"], cwd=path) or "0"
        ahead_flag = warn(f" +{ahead} unpushed") if ahead != "0" else ""

        # Version (streamtex only)
        version = ""
        if name == "streamtex":
            init = path / "streamtex" / "__init__.py"
            if init.exists():
                for line in init.read_text().splitlines():
                    if "__version__" in line:
                        version = line.split('"')[1]
                        break
                version = f"  v{version}"

        commit = run(["git", "log", "--oneline", "-1"], cwd=path) or ""
        print(f"  {name:20s}  {BLUE}{branch}{RESET}{version}{dirty_flag}{ahead_flag}")
        print(f"  {'':20s}  {dim(commit)}")


def section_pypi():
    header("PYPI")
    try:
        req = urllib.request.Request(
            "https://pypi.org/pypi/streamtex/json",
            headers={"User-Agent": "stx-dashboard/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        version = data["info"]["version"]
        upload = data["releases"].get(version, [{}])
        upload_time = upload[0].get("upload_time_iso_8601", "?") if upload else "?"
        if upload_time != "?":
            upload_time = upload_time[:19].replace("T", " ")
        print(f"  Published version:  {ok(version)}  ({upload_time})")
    except Exception as e:
        print(f"  {err('Could not reach PyPI')}: {e}")

    # Compare with local
    local_v = None
    init = REPOS["streamtex"] / "streamtex" / "__init__.py"
    if init.exists():
        for line in init.read_text().splitlines():
            if "__version__" in line:
                local_v = line.split('"')[1]
                break
    if local_v and local_v != version:
        print(f"  Local version:      {warn(local_v)}  {warn('(not published)')}")
    elif local_v:
        print(f"  Local version:      {ok(local_v)}  (matches PyPI)")


def section_coolify(tokens):
    header("COOLIFY SERVICES")
    coolify_token = tokens.get("COOLIFY_API_TOKEN", "")
    if not coolify_token:
        print(f"  {err('COOLIFY_API_TOKEN not found in .env')}")
        return

    try:
        req = urllib.request.Request(
            f"{COOLIFY_URL}/api/v1/applications",
            headers={
                "Authorization": f"Bearer {coolify_token}",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            apps = json.loads(resp.read())
    except Exception as e:
        print(f"  {err('Coolify API unreachable')}: {e}")
        return

    for app in sorted(apps, key=lambda a: a.get("name", "")):
        name = app.get("name", "?")
        status = app.get("status", "?")
        branch = app.get("git_branch", "?")
        fqdn = app.get("fqdn", "")  # noqa: F841

        if "healthy" in status:
            st = ok(status)
        elif "running" in status:
            st = warn(status)
        else:
            st = err(status)

        print(f"  {name:30s}  {st:40s}  {dim(branch)}")


def section_server(quick=False):
    header("HETZNER SERVER")
    if quick:
        print(f"  {dim('Skipped (--quick)')}")
        return

    disk = run(
        ["ssh", "-i", str(SSH_KEY), "-o", "ConnectTimeout=8",
         "-o", "StrictHostKeyChecking=no", f"root@{HETZNER_IP}",
         "df -h / --output=size,used,avail,pcent | tail -1"],
        timeout=15,
    )
    if disk:
        parts = disk.split()
        pct = parts[3] if len(parts) >= 4 else "?"
        pct_num = int(pct.replace("%", "")) if "%" in pct else 0
        color = ok if pct_num < 70 else (warn if pct_num < 90 else err)
        print(f"  IP:    {HETZNER_IP}")
        print(f"  Disk:  {parts[1]}/{parts[0]} used  ({color(pct)})")
    else:
        print(f"  {err('SSH unreachable')} ({HETZNER_IP})")
        return

    mem = run(
        ["ssh", "-i", str(SSH_KEY), "-o", "ConnectTimeout=5",
         f"root@{HETZNER_IP}",
         "free -h | awk '/Mem:/{print $2, $3, $4}'"],
        timeout=10,
    )
    if mem:
        parts = mem.split()
        print(f"  RAM:   {parts[1]}/{parts[0]} used  ({parts[2]} free)")

    containers = run(
        ["ssh", "-i", str(SSH_KEY), "-o", "ConnectTimeout=5",
         f"root@{HETZNER_IP}",
         "docker ps -q | wc -l"],
        timeout=10,
    )
    if containers:
        print(f"  Containers: {containers} running")


def section_urls(quick=False):
    header("URL HEALTH")
    if quick:
        print(f"  {dim('Skipped (--quick)')}")
        return

    for name, url in PROD_URLS.items():
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "stx-dashboard/1.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                code = resp.getcode()
            if code == 200:
                print(f"  {name:20s}  {ok('200 OK'):30s}  {dim(url)}")
            else:
                print(f"  {name:20s}  {warn(str(code)):30s}  {dim(url)}")
        except urllib.error.HTTPError as e:
            # Cloudflare challenge returns 403 — service is up
            if e.code == 403:
                print(f"  {name:20s}  {ok('403 (CF challenge)'):30s}  {dim(url)}")
            else:
                print(f"  {name:20s}  {err(str(e.code)):30s}  {dim(url)}")
        except Exception:
            print(f"  {name:20s}  {err('unreachable'):30s}  {dim(url)}")


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    quick = "--quick" in sys.argv
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{BOLD}{CYAN}  StreamTeX Dashboard{RESET}  {dim(now)}")

    tokens = load_env()
    section_local()
    section_pypi()
    section_coolify(tokens)
    section_server(quick)
    section_urls(quick)

    print(f"\n{dim('─' * 60)}\n")


if __name__ == "__main__":
    main()
