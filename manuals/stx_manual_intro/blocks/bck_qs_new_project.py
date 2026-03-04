"""Quick Start — Create a Project."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Quick Start new project styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Quick Start Step 2: Create a project with a workspace (standard)."""
    st_space("v", 1)
    st_write(bs.heading, "Quick Start — Create a Project",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # --- Create workspace ---
    st_write(bs.sub, "Step 1: Create a workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A workspace groups documentation, Claude profiles,
        and your projects in one folder. The default standard
        preset clones streamtex-docs and streamtex-claude.
    """)
    st_space("v", 1)

    show_code("""\
mkdir streamtex-dev && cd streamtex-dev
stx workspace init .
stx workspace clone
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Create with template ---
    st_write(bs.sub, "Step 2: Create the project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Use the stx CLI to scaffold a new project.
        The --template project flag includes 9 tutorial blocks
        that demonstrate all major StreamTeX features.
    """)
    st_space("v", 1)

    show_code("""\
stx project new mon-projet --template project
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Project structure ---
    st_write(bs.sub, "Step 3: Project structure", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The CLI generates a complete project layout
        with all required files and configuration.
    """)
    st_space("v", 1)

    show_code("""\
projects/stx-mon-projet/
+-- pyproject.toml           # Dependencies + ruff config
+-- book.py                  # Entry point (orchestrates blocks)
+-- custom/
|   +-- styles.py            # Project-specific style definitions
+-- blocks/
|   +-- __init__.py          # Block registry (auto-discovery)
|   +-- helpers.py           # Project-specific helper config
|   +-- bck_01_welcome.py    # Tutorial blocks (9 total)
+-- static/
|   +-- images/              # Static assets
+-- .streamlit/
    +-- config.toml          # Static serving enabled
""", language="text", line_numbers=False)
    st_space("v", 2)

    # --- Claude profile ---
    st_write(bs.sub, "Step 4: Install a Claude profile", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Add AI-powered slash commands and agents
        to your project. This enables zero-code workflows
        with Claude Code or Cursor.
    """)
    st_space("v", 1)

    show_code("""\
cd projects/stx-mon-projet
stx claude install project .
""", language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Run ---
    st_write(bs.sub, "Step 5: Run the project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Launch the project with Streamlit.
        The template project is ready to run immediately.
    """)
    st_space("v", 1)

    show_code("""\
uv run streamlit run book.py
""", language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        The stx project new command generates pyproject.toml
        with the mandatory ruff config and .streamlit/config.toml
        with static serving enabled. No manual setup required.

        Without --template, a minimal scaffold is created
        with a single bck_hello.py starter block.

        For Claude profiles only (no docs): use --preset user.
        For full developer setup: use --preset developer
        then stx workspace link for editable installs.
    """)
    st_space("v", 1)
