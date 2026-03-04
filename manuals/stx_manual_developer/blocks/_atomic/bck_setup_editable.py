from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Editable install styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Editable Install for streamtex-docs",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Why editable install ---
        st_write(bs.sub, "Why editable install?", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When developing the StreamTeX library alongside the docs,
            you need changes to the library to be reflected immediately
            without reinstalling. An editable install creates a live
            link between the source code and the installed package.
        """)
        st_space("v", 2)

        # --- 2. How uv handles editable installs ---
        st_write(bs.sub, "How uv handles editable installs", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            uv reads the pyproject.toml to determine how to install
            the package. When a local path dependency is declared,
            uv installs it in editable mode automatically.
        """)
        st_space("v", 1)

        show_code("""\
# In streamtex-docs/pyproject.toml
[project]
dependencies = [
    "streamtex",       # from PyPI (release)
]

# For development, override with a local path:
[tool.uv.sources]
streamtex = { path = "../streamtex", editable = true }""", language="toml")
        st_space("v", 2)

        # --- 3. Development workflow ---
        st_write(bs.sub, "Development workflow", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The typical dev loop is: edit the library source,
            then run a manual to see the effect immediately.
            No reinstall step is needed because the editable
            install points directly at the source tree.
        """)
        st_space("v", 1)

        show_code("""\
# 1. Edit the library source
#    e.g. streamtex/streamtex/core.py

# 2. Run a manual to test the change
uv run streamlit run manuals/stx_manual_intro/book.py

# 3. The change is reflected immediately
#    because the editable install points at the source""", language="bash")
        st_space("v", 2)

        # --- 4. Verify the editable install ---
        st_write(bs.sub, "Verify the editable install", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Confirm that the editable install is active by checking
            the installed package location. It should point to your
            local source directory, not to a site-packages copy.
        """)
        st_space("v", 1)

        show_code("""\
# Check where streamtex is installed from
uv run python -c "import streamtex; print(streamtex.__file__)"
# Should print a path inside your local streamtex/ directory

# Run a manual to confirm everything works end-to-end
uv run streamlit run manuals/stx_manual_intro/book.py""", language="bash")
        st_space("v", 2)

        # --- 5. Workflow diagram ---
        st_write(bs.sub, "Edit-test cycle", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
Edit streamtex/streamtex/*.py
    |
    v
uv run streamlit run manuals/<manual>/book.py
    |
    v
See changes live (no reinstall needed)
    |
    v
uv run pytest tests/ -v   (verify nothing broke)
    |
    v
uv run ruff check streamtex/   (verify code style)""", language="text")
        st_space("v", 2)

        show_details("""\
            The editable install only affects the local environment.

            When deploying, the docs project pulls the release
            version of streamtex from PyPI.

            Always run tests after editing the library to catch
            regressions before committing.
        """)
