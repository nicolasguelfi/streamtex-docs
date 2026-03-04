"""Atomic block — Source modules breakdown by category."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Source modules section styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    category_label = s.large + s.text.weights.bold_weight + s.project.colors.dev_cyan

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Source Modules", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            The `streamtex/` package contains 38 modules organised into functional
            categories. Each module has a single responsibility and exports its
            public API through `__init__.py`.
        """)
        st_space("v", 2)

        # --- Core Rendering ---
        st_write(bs.sub, "Core Rendering", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            write.py        # st_write() — main text rendering engine
            markdown.py     # st_markdown() — Streamlit-native markdown
            code.py         # st_code() — syntax-highlighted code blocks
            image.py        # st_image() — image handling with base64
            container.py    # st_block(), st_span() — styled containers
            space.py        # st_space(), st_br() — vertical/horizontal spacing
            overlay.py      # st_overlay() — positioned overlay panels\
        """, language="text")
        st_space("v", 2)

        # --- Layout & Styling ---
        st_write(bs.sub, "Layout & Styling", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            grid.py         # st_grid() — CSS Grid layout system
            list.py         # st_list() — ordered/unordered/custom lists
            styles/         # Style class, StxStyles, composition engine
            zoom.py         # st_zoom() — responsive zoom control
            constants.py    # Shared constants and defaults\
        """, language="text")
        st_space("v", 2)

        # --- Book Orchestration ---
        st_write(bs.sub, "Book Orchestration", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            book.py         # st_book() — page orchestration (paginated/continuous)
            banner.py       # st_banner() — top banner rendering
            toc.py          # st_toc() — table of contents generation
            marker.py       # st_marker() — navigation markers
            collection.py   # st_collection() — multi-project hub\
        """, language="text")
        st_space("v", 2)

        # --- Content Processing ---
        st_write(bs.sub, "Content Processing", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            blocks.py       # Block loading, registry, lazy imports
            block_helpers.py # show_code(), show_explanation(), show_details()
            search.py       # Full-text search across blocks
            inspector.py    # Runtime block inspection tools\
        """, language="text")
        st_space("v", 2)

        # --- Diagrams & Visualisation ---
        st_write(bs.sub, "Diagrams & Visualisation", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            mermaid.py      # st_mermaid() — Mermaid diagram rendering
            plantuml.py     # st_plantuml() — PlantUML diagram rendering
            tikz.py         # st_tikz() — TikZ diagrams via LaTeX pipeline
            latex.py        # st_latex() — LaTeX math rendering\
        """, language="text")
        st_space("v", 2)

        # --- Document Processing ---
        st_write(bs.sub, "Document Processing", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            latex_utils.py      # LaTeX compilation utilities
            export.py           # HTML/PDF export pipeline
            export_widgets.py   # Export UI widgets (buttons, progress)
            bib_preview.py      # Bibliography preview rendering\
        """, language="text")
        st_space("v", 2)

        # --- Data Integration ---
        st_write(bs.sub, "Data Integration", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            bib.py          # BibTeX parsing and citation management
            gsheet.py       # Google Sheets data import
            auth.py         # Authentication helpers (GCP service accounts)
            link_config.py  # Link configuration and URL management\
        """, language="text")
        st_space("v", 2)

        # --- Link Features ---
        st_write(bs.sub, "Link Features", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            link_preview.py # Rich link preview cards
            utils.py        # Shared utility functions\
        """, language="text")
        st_space("v", 2)

        # --- CLI ---
        st_write(bs.sub, "CLI (cli/)", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            cli/
            ├── main.py         # Entry point, click group registration
            ├── commands.py     # Top-level command definitions
            ├── project_cmd.py  # stx project init/info/validate
            ├── workspace_cmd.py# stx workspace management
            ├── deploy_cmd.py   # stx deploy (Docker, cloud)
            ├── publish_cmd.py  # stx publish (PyPI release)
            ├── claude_cmd.py   # stx claude (profile management)
            ├── bib_cmd.py      # stx bib (bibliography tools)
            ├── shortcuts.py    # stx run, stx export shortcuts
            └── console.py      # Rich console output helpers\
        """, language="text")
        st_space("v", 2)

        show_details("""\
            All public symbols are re-exported through `streamtex/__init__.py`.
            Users should never import from internal modules directly.

            The `cli/` sub-package uses click groups; each file registers its
            commands with the top-level `stx` group defined in `main.py`.
        """)
