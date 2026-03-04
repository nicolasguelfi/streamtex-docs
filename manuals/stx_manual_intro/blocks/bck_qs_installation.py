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
    """Quick Start Step 1: Install StreamTeX (minimal, no workspace)."""
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

    # --- Create project (no workspace) ---
    st_write(bs.sub, "Step 3: Create a project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Create a minimal project directly, without a workspace.
        This is the fastest way to start.
    """)
    st_space("v", 1)

    show_code("""\
stx project new mon-projet
cd stx-mon-projet
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Run ---
    st_write(bs.sub, "Step 4: Run the project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Sync dependencies and launch the project
        with Streamlit. The scaffold is ready to run immediately.
    """)
    st_space("v", 1)

    show_code("""\
uv sync
uv run streamlit run book.py
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        This minimal installation creates a standalone project
        without a workspace. To unlock rich templates, Claude AI
        profiles, and local documentation, see the next section
        (Create a Project with a workspace).

        Manual installation without the stx CLI:
        pip install streamtex
        git clone https://github.com/nicolasguelfi/streamtex-claude.git
        mkdir my-project && cd my-project
        python ../streamtex-claude/install.py project .
        uv run streamlit run book.py
    """)
    st_space("v", 1)
