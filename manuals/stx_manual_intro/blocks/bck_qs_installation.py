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
    """Quick Start: Install StreamTeX and create a workspace."""
    st_space("v", 1)
    st_write(bs.heading, "Quick Start — Installation",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # --- Prerequisites ---
    st_write(bs.sub, "Step 1: Prerequisites", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.large,
        "StreamTeX requires ",
        (s.bold, "Python 3.10"),
        " or later, ",
        (s.bold, "git"),
        ", and ",
        (s.bold, "uv"),
        " as its package manager. Make sure all three are installed before continuing.",
    )
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
        A workspace groups documentation, Claude profiles,
        and your projects in one folder. The --preset option
        controls which repos are included.
    """)
    st_space("v", 1)

    show_code("""\
mkdir streamtex-dev && cd streamtex-dev
stx workspace init . --preset standard  # basic | user | standard | developer
stx workspace clone
# Shared commands (like /stx-guide) are installed globally to ~/.claude/commands/
""", language="bash", line_numbers=False)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(s.large, "The four presets offer increasing levels of functionality:")
        with st_list(li_style=s.large, list_type="ul") as l:
            with l.item():
                st_write(s.large, (s.bold, "basic"), " — empty workspace, no repos. Create standalone projects and upgrade later when needed.")
            with l.item():
                st_write(s.large, (s.bold, "user"), " — adds streamtex-claude (Claude AI profiles). Enables stx claude install for slash commands and agents.")
            with l.item():
                st_write(s.large, (s.bold, "standard"), " (default) — adds streamtex-docs + streamtex-claude. Enables rich templates (--template project) and local documentation alongside Claude profiles.")
            with l.item():
                st_write(s.large, (s.bold, "developer"), " — adds all 3 repos (library + docs + claude). Enables editable installs (stx workspace link) so library source changes are reflected immediately.")
    st_space("v", 2)

    # --- Create and run a project ---
    st_write(bs.sub, "Step 4: Create and run a project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Create a new project inside the workspace, sync
        dependencies, and launch it with Streamlit.
    """)
    st_space("v", 1)

    show_code("""\
stx project new mon-projet
cd projects/stx-mon-projet
uv sync
uv run streamlit run book.py
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        Shortcut without a workspace — create a standalone project
        directly with stx project new mon-projet then cd into it.
        You can always add a workspace later with stx workspace init.

        Manual installation without the stx CLI:
        pip install streamtex
        git clone https://github.com/nicolasguelfi/streamtex-claude.git
        mkdir my-project && cd my-project
        python ../streamtex-claude/install.py project .
        uv run streamlit run book.py
    """)
    st_space("v", 1)
