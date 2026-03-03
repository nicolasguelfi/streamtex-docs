"""Part 2 — Prerequisites for AI-powered StreamTeX workflows."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Prerequisites block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Prerequisites — what you need before getting started."""
    st_space("v", 1)
    st_write(bs.heading, "Prerequisites", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        Before using AI-powered workflows with StreamTeX, make sure
        your environment meets these requirements. The setup takes
        only a few minutes.
    """))
    st_space("v", 2)

    # --- Python ---
    st_write(bs.sub, "Python 3.10+", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        StreamTeX requires Python 3.10 or later. Check your
        installed version before continuing.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Check your Python version
        python3 --version
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- uv ---
    st_write(bs.sub, "uv Package Manager (recommended)", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        uv is a fast Python package manager that replaces pip and venv.
        StreamTeX projects use uv for dependency management, virtual
        environment creation, and command execution.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Install uv (macOS / Linux)
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Or with Homebrew
        brew install uv

        # Verify installation
        uv --version
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Claude Code or Cursor ---
    st_write(bs.sub, "AI Tool: Claude Code or Cursor", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        StreamTeX AI profiles work with two AI coding tools.
        Choose the one that fits your workflow best.
    """))
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(s.project.titles.subsection_title, "Claude Code (CLI)")
                st_space("v", 1)
                st_write(s.large, (
                    "Terminal-based AI assistant by Anthropic. "
                    "Works in any editor. Full profile support with "
                    "commands, agents, and skills."
                ))
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(s.project.titles.subsection_title, "Cursor IDE")
                st_space("v", 1)
                st_write(s.large, (
                    "VS Code fork with built-in AI. "
                    "Uses .cursor/rules/ for project rules. "
                    "StreamTeX profiles can be adapted for Cursor."
                ))
    st_space("v", 2)

    # --- StreamTeX installation ---
    st_write(bs.sub, "Install StreamTeX", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Install the StreamTeX library from PyPI. Use uv (recommended)
        or pip as your package manager.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # With uv (recommended)
        uv add streamtex

        # Or with pip
        pip install streamtex
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Optional CLI extras ---
    st_write(bs.sub, "Optional: CLI Extras", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        For the full CLI experience (stx command), install with
        the cli extras. This adds workspace management, validation,
        and profile installation commands.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # With uv
        uv add streamtex[cli]

        # Or with pip
        pip install streamtex[cli]
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    show_details(textwrap.dedent("""\
        The streamtex[cli] extra includes the stx command-line tool
        used throughout this manual. Without it, you can still use
        StreamTeX as a Python library, but the stx commands
        (workspace, claude install, etc.) will not be available.
    """))
    st_space("v", 1)
