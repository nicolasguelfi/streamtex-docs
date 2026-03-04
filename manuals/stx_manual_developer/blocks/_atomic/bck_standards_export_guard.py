"""Atomic block — The export guard pattern."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Export guard styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "The Export Guard Pattern", tag=t.div,
                 toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            Every function that calls st.html() must be guarded with
            is_export_active(). This ensures that when an HTML export
            is running, all rendered content is captured into the
            export buffer. Without the guard, content is displayed in
            the browser but missing from the exported file.
        """)
        st_space("v", 2)

        # --- The pattern ---
        st_write(bs.sub, "The canonical pattern", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            def _render(style, content, tag):
                html = f'<{tag} style="{style.css}">{content}</{tag}>'
                st.html(html)
                if is_export_active():
                    export_append(html)\
        """, language="python")
        st_space("v", 1)

        show_explanation("""\
            The pattern has three parts:

            1. Build the HTML string from the style and content.
            2. Call st.html() to display it in the browser.
            3. If an export is active, append the same HTML to the
               export buffer so it appears in the generated file.

            This dual-write approach means every piece of visible
            content is also available for export.
        """)
        st_space("v", 2)

        # --- Why it matters ---
        st_write(bs.sub, "Why this matters", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX supports exporting entire books or pages to
            standalone HTML files. The export system works by collecting
            every HTML fragment rendered during a page build. If a
            module calls st.html() without also calling export_append(),
            that content silently disappears from the export.

            The AST guard test was created specifically to catch these
            omissions at CI time, before they reach users.
        """)
        st_space("v", 2)

        # --- AST test ---
        st_write(bs.sub, "The AST guard test", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            An automated AST test scans every module in streamtex/ for
            calls to st.html(). For each call site, it verifies that
            an is_export_active() check exists in the same function
            scope. If any unguarded call is found, the test fails with
            a clear message indicating the file and line number.
        """)
        st_space("v", 1)

        show_code("""\
            # Run the AST guard test specifically
            uv run pytest tests/test_export.py -v -k "ast_guard"

            # Or run it as part of the full suite
            uv run pytest tests/ -v\
        """, language="bash")
        st_space("v", 2)

        # --- Common mistakes ---
        st_write(bs.sub, "Common mistakes", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            # WRONG — missing export guard
            def render_badge(style, label):
                html = f'<span style="{style.css}">{label}</span>'
                st.html(html)
                # Export will miss this content!

            # CORRECT — guarded
            def render_badge(style, label):
                html = f'<span style="{style.css}">{label}</span>'
                st.html(html)
                if is_export_active():
                    export_append(html)

            # ALSO CORRECT — use a shared _render() helper
            def render_badge(style, label):
                _render(style, label, tag="span")\
        """, language="python")
        st_space("v", 2)

        show_details("""\
            If you see the AST test failing on CI, search for st.html()
            in the reported file and add the is_export_active() guard.

            Prefer extracting a shared _render() helper rather than
            duplicating the guard in every function. Most StreamTeX
            modules already have one.
        """)
