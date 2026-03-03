import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Adding CLI commands styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Adding a New CLI Command",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Step 1: Create command file ---
        st_write(bs.sub, "Step 1: Create the command file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Create a new file in streamtex/cli/ following the naming
            convention: mycommand_cmd.py. This file will contain
            your Click group or command definition.
        """)
        st_space("v", 1)

        show_code("""\
# streamtex/cli/mycommand_cmd.py
import click
from streamtex.cli.console import console

@click.group()
def mycommand():
    \"\"\"My new command group.\"\"\"
    pass

@mycommand.command()
@click.argument("name")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def run(name, verbose):
    \"\"\"Run mycommand with the given name.\"\"\"
    console.print(f"Running mycommand for [bold]{name}[/bold]")
    if verbose:
        console.print("Verbose mode enabled")

@mycommand.command()
def status():
    \"\"\"Show mycommand status.\"\"\"
    console.print("Status: [green]OK[/green]")""", language="python")
        st_space("v", 2)

        # --- Step 2: Define Click group ---
        st_write(bs.sub, "Step 2: Define Click group or command", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use @click.group() for commands that have subcommands
            (e.g. stx mycommand run, stx mycommand status).
            Use @click.command() for standalone commands that do not
            need subcommands. Add docstrings — Click uses them as
            help text automatically.
        """)
        st_space("v", 2)

        # --- Step 3: Register in commands.py ---
        st_write(bs.sub, "Step 3: Register in commands.py", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# streamtex/cli/commands.py
from streamtex.cli.mycommand_cmd import mycommand

def register_commands(cli):
    # ... existing registrations ...
    cli.add_command(mycommand)""", language="python")
        st_space("v", 1)

        show_explanation("""\
            The commands.py module is the single place where all
            command groups are registered. Import your command group
            and add it with cli.add_command(). The command name
            defaults to the function name (mycommand), but you can
            override it: cli.add_command(mycommand, "my-cmd").
        """)
        st_space("v", 2)

        # --- Step 4: Add tests ---
        st_write(bs.sub, "Step 4: Add tests", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# tests/test_cli_mycommand.py
from click.testing import CliRunner
from streamtex.cli.main import app

def test_mycommand_run():
    runner = CliRunner()
    result = runner.invoke(app, ["mycommand", "run", "example"])
    assert result.exit_code == 0
    assert "Running mycommand for example" in result.output

def test_mycommand_status():
    runner = CliRunner()
    result = runner.invoke(app, ["mycommand", "status"])
    assert result.exit_code == 0""", language="python")
        st_space("v", 1)

        show_explanation("""\
            Use Click's CliRunner for testing. It invokes the CLI
            in-process without spawning a subprocess, making tests
            fast and reliable. Always test both the happy path and
            error cases.
        """)
        st_space("v", 2)

        # --- Step 5: Export ---
        st_write(bs.sub, "Step 5: Export in __init__.py if needed", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            If your command module exposes utilities that other parts
            of the codebase need, add the relevant imports to
            streamtex/cli/__init__.py. For most CLI commands, this
            step is not needed — the registration in commands.py
            is sufficient.
        """)
        st_space("v", 2)

        # --- Summary ---
        st_write(bs.sub, "Summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Step")
            with g.cell(): st_write(s.bold + s.large, "Action")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "1")
            with g.cell():
                st_write(s.large, "Create streamtex/cli/mycommand_cmd.py")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "2")
            with g.cell():
                st_write(s.large, "Define Click group or command with docstrings")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "3")
            with g.cell():
                st_write(s.large, "Register in commands.py via cli.add_command()")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "4")
            with g.cell():
                st_write(s.large, "Add tests in tests/test_cli_mycommand.py")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "5")
            with g.cell():
                st_write(s.large, "Export in __init__.py if needed")
        st_space("v", 2)

        show_details("""\
            Keep CLI commands thin. They should parse arguments,
            validate input, and delegate to library functions.
            Business logic belongs in the streamtex package,
            not in the CLI layer.
        """)
