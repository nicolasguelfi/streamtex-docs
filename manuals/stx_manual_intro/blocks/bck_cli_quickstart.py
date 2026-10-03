"""CLI Quick Start — stx command-line tool."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """CLI quick start styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """CLI Quick Start — introduce the stx command-line tool."""
    st_space("v", 1)
    st_write(bs.heading, "CLI Quick Start \u2014 stx",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(
        s.large,
        "StreamTeX provides a CLI tool called ",
        (s.bold, "stx"),
        " for project management. It helps you ",
        (s.bold, "create"),
        ", ",
        (s.bold, "validate"),
        ", ",
        (s.bold, "test"),
        ", and ",
        (s.bold, "lint"),
        " your StreamTeX projects from the command line.",
    )
    st_space("v", 2)

    # --- Prerequisites ---
    st_write(bs.sub, "Prerequisites", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The stx CLI requires Python 3.11+, git, and uv (recommended).
        If uv is not installed, run one of these commands first.
    """)
    st_space("v", 1)

    show_code("""\
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS with Homebrew
brew install uv

# Any platform (with pip)
pip install uv
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Installation ---
    st_write(bs.sub, "Installation", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Install the CLI as a global tool with uv (recommended)
        or pip. This makes the stx command available everywhere.
    """)
    st_space("v", 1)

    show_code("""\
# With uv (recommended)
uv tool install streamtex[cli]

# With pip (alternative)
pip install streamtex[cli]
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx project new ---
    st_write(bs.sub, "Create a new project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Scaffold a new StreamTeX project from the built-in
        template. This creates the full directory structure
        with book.py, blocks/, custom/, and static/ folders.
    """)
    st_space("v", 1)

    show_code("""\
# Minimal scaffold
stx project new myproject

# Rich template with 9 tutorial blocks
stx project new myproject --template project

# Available templates: project (default), slides, collection
stx project new myslides --template slides
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx run ---
    st_write(bs.sub, "Run a project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        stx run starts the project in the current directory (a shortcut
        for uv run streamlit run book.py) and opens it in the browser.
    """)
    st_space("v", 1)

    show_code("""\
stx run                       # book.py of the current directory
stx run path/to/book.py       # another book
stx run --port 8502           # a fixed port
stx run --force               # free the port first
stx run --headless            # no browser
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx run --set (0.7.39) ---
    st_write(bs.sub, "Run several documents together", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A project made of several documents (decks, modules, a hub)
        declares them once in its stx.toml, one `[[run.documents]]`
        table each: an id, the book, a fixed port. stx run --set then
        starts all of them in the background. Every document receives
        one environment variable per document, `STX_URL_<ID>` (the id in
        upper case, - becomes _), holding that document's address — the
        links between documents need no hard-coded port.
    """)
    st_space("v", 1)

    show_code("""\
# stx.toml (at the root of the project)
[[run.documents]]
id = "opening"                               # $STX_URL_OPENING
book = "modules/opening/book.py"
port = 8731

[[run.documents]]
id = "survey"                                # $STX_URL_SURVEY
book = "modules/survey/book.py"
port = 8732
""", language="toml", line_numbers=False)
    st_space("v", 1)

    show_code("""\
stx run --set                    # start every declared document
stx run --set --doc survey       # only this one
stx run --list                   # documents, ports, state
stx run --kill                   # stop them (--doc to target one)
stx run --set --fresh            # stop, clear the page cache, start again
stx run --set --lang fr          # the URLs carry ?lang=fr
stx run --set --ports-offset 100 # 8831, 8832: a second set side by side
stx run --set --open             # open the documents in the browser
stx run --set --open --chrome-profile ~/.stx-projection-chrome
""", language="bash", line_numbers=False)
    st_space("v", 1)

    show_details("""\
        State and logs live in `.stx_run/` next to stx.toml (one
        `<id>.json` and `<id>.log` per document). The project's .venv is
        used when present. --chrome-profile opens a dedicated Chrome
        profile allowed to autoplay media, for projection. stx run
        without these options behaves as before.
    """)
    st_space("v", 2)

    # --- stx project validate ---
    st_write(bs.sub, "Validate project structure", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Check that your project has the required files and
        directories. Reports missing or misplaced elements.
    """)
    st_space("v", 1)

    show_code("""\
stx project validate
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx test ---
    st_write(bs.sub, "Run the test suite", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Execute the project test suite using pytest under
        the hood. Discovers and runs all tests in the tests/
        directory.
    """)
    st_space("v", 1)

    show_code("""\
stx test
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx lint ---
    st_write(bs.sub, "Run the linter", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Run ruff against your project to catch style issues,
        unused imports, and potential errors.
    """)
    st_space("v", 1)

    show_code("""\
stx lint
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Workspace presets ---
    st_write(bs.sub, "Workspace presets", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Workspaces support 5 presets that control which repos
        are cloned. Use --preset with stx install,
        or upgrade an existing workspace.
    """)
    st_space("v", 1)

    show_code("""\
# basic — workspace only, no repos
stx install --preset basic

# user — Claude AI profiles only
stx install --preset user

# standard (default) — docs + Claude profiles
stx install

# power — docs + Claude profiles + all extras (pdf, ai, inspector)
stx install --preset power

# developer — all 3 repos (library + docs + Claude)
stx install --preset developer
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        Upgrade an existing workspace to a higher preset.
        This adds the missing repos to stx.toml without
        touching existing configuration.
    """)
    st_space("v", 1)

    show_code("""\
stx install --preset developer
stx update   # clones + syncs newly declared repos
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx status ---
    st_write(bs.sub, "Check workspace status", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Display a summary of the current workspace: preset,
        installed repos, sync state, and project list.
    """)
    st_space("v", 1)

    show_code("""\
stx status
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx project upgrade ---
    st_write(bs.sub, "Upgrade an existing project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Upgrade an existing project to the latest StreamTeX
        scaffolding and configuration. Use --check to preview
        changes, or --dry-run to simulate without writing files.
    """)
    st_space("v", 1)

    show_code("""\
# Preview what would change
stx project upgrade --check

# Simulate the upgrade without writing files
stx project upgrade --dry-run

# Apply the upgrade
stx project upgrade
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Ruff configuration ---
    st_write(bs.sub, "Ruff configuration", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX projects require specific ruff ignore rules
        in pyproject.toml. The stx project new command generates
        this configuration automatically.
    """)
    st_space("v", 1)

    show_code("""\
# pyproject.toml — mandatory for all StreamTeX projects
[tool.ruff.lint]
ignore = ["F403", "F405", "E701", "E741"]
""", language="toml", line_numbers=False)
    st_space("v", 2)

    # --- CI configuration ---
    st_write(bs.sub, "CI configuration", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        If your project uses [tool.uv.sources] for editable
        installs (e.g. pointing to a local streamtex checkout),
        set UV_NO_SOURCES=1 in CI so uv resolves from PyPI.
    """)
    st_space("v", 1)

    show_code("""\
# GitHub Actions example
env:
  UV_NO_SOURCES: 1
""", language="yaml", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        These are the essential day-to-day commands.
        Advanced CLI commands for deployment and publishing
        (stx deploy, stx publish, stx install/update/status) are covered
        in the Deploy manual.
    """)
    st_space("v", 1)
