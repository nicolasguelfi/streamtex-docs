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

    # --- Installation ---
    st_write(bs.sub, "Installation", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Install the CLI as a global tool with uv.
        This makes the stx command available everywhere.
    """)
    st_space("v", 1)

    show_code("""\
# Recommended: install as a global tool
uv tool install streamtex[cli]

# Or as a project dependency
uv add streamtex[cli]
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
""", language="bash", line_numbers=False)
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
        Workspaces support 4 presets that control which repos
        are cloned. Use --preset with stx workspace init,
        or upgrade an existing workspace.
    """)
    st_space("v", 1)

    show_code("""\
# basic — workspace only, no repos
stx workspace init . --preset basic

# user — Claude AI profiles only
stx workspace init . --preset user

# standard (default) — docs + Claude profiles
stx workspace init .

# developer — all 3 repos (library + docs + Claude)
stx workspace init . --preset developer
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        Upgrade an existing workspace to a higher preset.
        This adds the missing repos to stx.toml without
        touching existing configuration.
    """)
    st_space("v", 1)

    show_code("""\
stx workspace upgrade developer
stx workspace update   # clones + syncs newly declared repos
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
        (stx deploy, stx publish, stx workspace) are covered
        in the Deploy manual.
    """)
    st_space("v", 1)
