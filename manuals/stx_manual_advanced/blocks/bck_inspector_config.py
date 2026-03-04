"""Inspector Configuration — InspectorConfig dataclass reference."""

from streamtex import (
    st_write, st_block, st_space, st_grid,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Inspector configuration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    """Inspector Configuration — dataclass, usage, and features."""
    st_write(bs.heading, "Inspector Configuration", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The Inspector is a development sidebar panel built into
        StreamTeX. It provides a live code editor, file browser,
        and per-block edit buttons for rapid iteration.

        InspectorConfig is a dataclass that controls the inspector
        behavior. Pass it to st_book() via the inspector= parameter.
    """)
    st_space("v", 2)

    # --- InspectorConfig dataclass ---
    st_write(bs.sub, "InspectorConfig Dataclass", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The dataclass has four fields, each with a sensible default.
        You only need to set what you want to customize.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import InspectorConfig

        InspectorConfig(
            enabled=True,           # Enable the inspector panel
            password=None,          # Optional password protection
            panel_width="35vw",     # CSS width of the sidebar panel
            backup=True,            # Create .bak files before saving
        )
    """, language="python")
    st_space("v", 2)

    # --- Usage in st_book() ---
    st_write(bs.sub, "Usage in st_book()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Pass an InspectorConfig instance to st_book() using the
        inspector= keyword argument.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import st_book, InspectorConfig

        st_book(
            [bck_intro, bck_chapter_1, bck_chapter_2],
            inspector=InspectorConfig(enabled=True),
        )
    """, language="python")
    st_space("v", 2)

    # --- Features ---
    st_write(bs.sub, "Inspector Features", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Live code editor \u2014 Edit any block file directly in the
        browser. Changes are saved to disk and the page reloads
        automatically.

        File browser \u2014 Navigate the project directory tree.
        Open any file for viewing or editing. Certain directories
        are excluded (see below).

        Per-block edit button \u2014 Each block displays a small edit
        icon. Clicking it opens that block's source file in the
        inspector editor.
    """)
    st_space("v", 2)

    # --- Panel width presets ---
    st_write(bs.sub, "Panel Width Presets", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The panel_width field accepts any valid CSS width value.
        Common presets:

        Default \u2014 "35vw" (35% of viewport width).
        Medium  \u2014 "700px" for a fixed medium-width panel.
        Large   \u2014 "900px" for wider code editing.
        XL      \u2014 "1100px" for full code visibility.
    """)
    st_space("v", 1)

    show_code("""\
        # Fixed-width panel
        InspectorConfig(enabled=True, panel_width="700px")

        # Extra-large panel for wide monitors
        InspectorConfig(enabled=True, panel_width="1100px")
    """, language="python")
    st_space("v", 2)

    # --- Password protection ---
    st_write(bs.sub, "Password Protection", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Set the password field to protect the inspector on shared
        deployments. When a password is set, users must enter it
        before the inspector panel opens.
    """)
    st_space("v", 1)

    show_code("""\
        # Password-protected inspector
        InspectorConfig(
            enabled=True,
            password="secret",
        )
    """, language="python")
    st_space("v", 2)

    # --- Excluded directories ---
    st_write(bs.sub, "Excluded Directories", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The file browser automatically excludes certain directories
        to keep the tree clean and avoid exposing sensitive files:

        .venv/     \u2014 Virtual environment.
        .git/      \u2014 Git internals.
        __pycache__/ \u2014 Python bytecode cache.
        .ruff_cache/ \u2014 Linter cache.
        node_modules/ \u2014 Node.js dependencies (if present).
    """)
    st_space("v", 2)

    show_details("""\
        The backup=True default creates a .bak copy of each file
        before the inspector overwrites it. This provides a simple
        safety net for accidental edits.

        Set backup=False to disable this behavior in environments
        where version control already provides sufficient protection.
    """)
    st_space("v", 1)
