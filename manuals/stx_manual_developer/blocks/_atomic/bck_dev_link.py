from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Dev link styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Development Links — stx dev",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Problem ---
        st_write(bs.sub, "The problem", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When developing the StreamTeX library, you may be tempted
            to modify files directly in your project's .venv. These
            changes are **lost** on the next `uv sync` or `stx update`.

            `stx dev` provides a safe workflow: register your source
            repos once, then link any project to them with a single command.
        """)
        st_space("v", 2)

        # --- 2. Register repos (once per machine) ---
        st_write(bs.sub, "Register source repos (once per machine)", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Register the absolute path to each official repo.
            The paths are stored in `~/.config/streamtex/dev.json`
            and shared across all your projects.
        """)
        st_space("v", 1)

        show_code("""\
# Register the 3 official repos
stx dev register streamtex /path/to/streamtex-dev/streamtex
stx dev register streamtex-claude /path/to/streamtex-dev/streamtex-claude
stx dev register streamtex-docs /path/to/streamtex-dev/streamtex-docs

# Verify registrations
stx dev status""", language="bash")
        st_space("v", 2)

        # --- 3. Link a project ---
        st_write(bs.sub, "Link a project to dev source", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            From any StreamTeX project directory, link to one or all
            registered repos. For `streamtex`, this adds `[tool.uv.sources]`
            to your `pyproject.toml` and runs `uv sync` to create an
            editable install. Changes to the source are reflected immediately.
        """)
        st_space("v", 1)

        show_code("""\
cd my-project

# Link a single repo
stx dev link streamtex

# Or link all registered repos at once
stx dev link all

# Check the result
stx dev status""", language="bash")
        st_space("v", 2)

        # --- 4. Unlink ---
        st_write(bs.sub, "Unlink and revert to PyPI", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Revert a single repo to PyPI version
stx dev unlink streamtex

# Or revert all
stx dev unlink all""", language="bash")
        st_space("v", 2)

        # --- 5. Safety ---
        st_write(bs.sub, "Safety rules", toc_lvl="+1")
        st_space("v", 1)

        show_details("""\
            **NEVER modify files inside `.venv/site-packages/streamtex/`.**
            These files are overwritten by `uv sync`.

            `stx dev register` validates that the path is a real repo
            (not inside a `.venv`) and contains the expected markers
            (`pyproject.toml` for streamtex, `install.py` for claude,
            `manuals/` for docs).

            `.stx-dev.json` is automatically added to `.gitignore`
            so dev links are never committed to the shared repo.

            In CI, set `UV_NO_SOURCES=1` to ignore `[tool.uv.sources]`
            and resolve from PyPI instead.
        """)
