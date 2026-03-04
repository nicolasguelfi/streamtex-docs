"""Quick Start — Installation."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Quick Start installation styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Quick Start Step 1: Install StreamTeX and set up the workspace."""
    st_space("v", 1)
    st_write(bs.heading, "Quick Start — Installation",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # --- Prerequisites ---
    st_write(bs.sub, "Step 1: Prerequisites", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX requires Python 3.10 or later, git,
        and uv as its package manager.

        Make sure all three are installed before continuing.
    """)
    st_space("v", 1)

    show_code("""\
# Check Python version (3.10+ required)
python3 --version

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Install CLI ---
    st_write(bs.sub, "Step 2: Install the StreamTeX CLI", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Install the stx command-line tool globally with uv.
        This gives you project scaffolding, workspace management,
        and Claude profile installation commands.
    """)
    st_space("v", 1)

    show_code("""\
uv tool install streamtex[cli]
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Create workspace ---
    st_write(bs.sub, "Step 3: Create a workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A workspace groups the StreamTeX library, documentation,
        Claude profiles, and your projects in one folder.

        Three commands set everything up.
    """)
    st_space("v", 1)

    show_code("""\
mkdir streamtex-dev && cd streamtex-dev
stx workspace init .
stx workspace clone     # clones streamtex, streamtex-docs, streamtex-claude
stx workspace link      # configures editable installs
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Verify ---
    st_write(bs.sub, "Step 4: Verify installation", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Check that the StreamTeX library can be imported
        from inside your workspace.
    """)
    st_space("v", 1)

    show_code("""\
uv run python -c "import streamtex; print(streamtex.__version__)"
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        Always prefix commands with uv run.
        This ensures the correct virtual environment
        and dependencies are used.

        Never call python,
        pytest, or streamlit directly.
    """)
    st_space("v", 1)
