import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """CLI architecture styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "CLI Architecture",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Entry point ---
        st_write(bs.sub, "Entry point", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The stx command is the main entry point for the StreamTeX CLI.
            It is defined in pyproject.toml under [project.scripts] and
            points to streamtex.cli.main:app.
        """))
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[project.scripts]
stx = "streamtex.cli.main:app\"""", language="toml")
        st_space("v", 2)

        # --- Main module ---
        st_write(bs.sub, "Main module", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# streamtex/cli/main.py
# Entry: app() function using Click
# Registers all command groups from commands.py""", language="python")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The main.py module creates the root Click group and
            imports all subcommands from commands.py. Each subcommand
            group lives in its own file for maintainability.
        """))
        st_space("v", 2)

        # --- Command hierarchy ---
        st_write(bs.sub, "Command hierarchy", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
stx                          # Root CLI group
 |-- test                    # shortcuts.py — run pytest
 |-- lint                    # shortcuts.py — run ruff
 |
 |-- workspace               # workspace_cmd.py
 |    |-- init               #   Initialize a new workspace
 |    |-- clone              #   Clone a project into workspace
 |    |-- link               #   Link an existing project
 |    |-- status             #   Show workspace status
 |    +-- sync               #   Sync all workspace projects
 |
 |-- claude                  # claude_cmd.py
 |    |-- install            #   Install Claude profiles
 |    |-- list               #   List available profiles
 |    |-- update             #   Update to latest profiles
 |    +-- diff               #   Diff local vs template
 |
 |-- bib                     # bib_cmd.py
 |    +-- generate-stubs     #   Generate bibliography stubs
 |
 |-- project                 # project_cmd.py
 |    |-- new                #   Create a new project from template
 |    +-- validate           #   Validate project structure
 |
 |-- deploy                  # deploy_cmd.py
 |    |-- preflight          #   Pre-deployment checks
 |    |-- docker             #   Build Docker image
 |    |-- render             #   Deploy to Render
 |    |-- huggingface        #   Deploy to HuggingFace
 |    +-- status             #   Check deployment status
 |
 +-- publish                 # publish_cmd.py
      |-- check              #   Verify version and changelog
      +-- pypi               #   Build and publish to PyPI""", language="text")
        st_space("v", 2)

        # --- Console helpers ---
        st_write(bs.sub, "Console helpers", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            The console.py module provides Rich-based formatting
            utilities used by all CLI commands for consistent output:

            - Colored status messages (success, warning, error).
            - Tables for structured output.
            - Progress indicators for long-running operations.
        """))
        st_space("v", 2)

        # --- File layout ---
        st_write(bs.sub, "File layout", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
streamtex/cli/
 |-- __init__.py
 |-- main.py              # Root app() + CLI entry point
 |-- commands.py           # Registers all command groups
 |-- console.py            # Rich-based formatting helpers
 |-- shortcuts.py          # Top-level shortcuts (test, lint)
 |-- workspace_cmd.py      # stx workspace *
 |-- claude_cmd.py         # stx claude *
 |-- bib_cmd.py            # stx bib *
 |-- project_cmd.py        # stx project *
 |-- deploy_cmd.py         # stx deploy *
 +-- publish_cmd.py        # stx publish *""", language="text")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            Each command file is self-contained: it defines its Click
            group or command, handles arguments, and calls into the
            core streamtex library for actual logic. The CLI layer
            is intentionally thin — business logic lives in the
            library, not in the CLI commands.
        """))
