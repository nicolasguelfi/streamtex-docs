"""Atomic block — Testing gotchas."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Testing gotchas styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Testing Gotchas", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            These are the most common pitfalls developers encounter
            when writing or debugging StreamTeX tests. Each one has
            caused real CI failures.
        """)
        st_space("v", 2)

        # --- Singleton state ---
        st_write(bs.sub, "Singleton state must be reset", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX uses singleton registries for the table of
            contents, bibliography, export buffer, and more. If a test
            modifies one of these and does not reset it, subsequent
            tests see stale state and fail non-deterministically.
        """)
        st_space("v", 1)

        show_code("""\
            # Always reset in teardown or use the autouse fixture

            def test_toc_entries():
                from streamtex import reset_toc_registry, st_write
                from streamtex.styles import Style
                from streamtex.enums import Tags as t

                reset_toc_registry()  # clean slate

                style = Style("", "s")
                st_write(style, "Chapter 1", toc_lvl="1")

                # ... assertions ...

                reset_toc_registry()  # clean up after yourself\
        """, language="python")
        st_space("v", 2)

        # --- Python builtins shadowing ---
        st_write(bs.sub, "Python builtins shadowing", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The wildcard import `from streamtex import *` can shadow
            Python builtins. The most common case is list() being
            replaced by StreamTeX's list function. In test files, be
            explicit about imports or use the list_type= parameter
            instead of calling list() directly.
        """)
        st_space("v", 1)

        show_code("""\
            # PROBLEM — list() is shadowed after wildcard import
            from streamtex import *
            items = list(range(10))  # TypeError!

            # SOLUTION 1 — import explicitly
            from streamtex import st_write, st_block

            # SOLUTION 2 — save the builtin before import
            _builtin_list = list
            from streamtex import *
            items = _builtin_list(range(10))

            # SOLUTION 3 — use builtins module
            import builtins
            items = builtins.list(range(10))\
        """, language="python")
        st_space("v", 2)

        # --- st.html vs components.html ---
        st_write(bs.sub, "st.html vs components.html", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Streamlit has two different html() functions:

            - st.html() renders HTML inline without an iframe. This is
              what StreamTeX uses for all content rendering.
            - streamlit.components.v1.html() renders inside an iframe
              with a specified height. Use this only for embedded
              widgets or third-party content that needs isolation.

            In tests, mock the correct one based on what you are testing.
        """)
        st_space("v", 1)

        show_code("""\
            # For StreamTeX content rendering
            @patch("streamlit.html")
            def test_content(mock_html):
                ...

            # For iframe-based components
            @patch("streamlit.components.v1.html")
            def test_iframe_widget(mock_component_html):
                ...\
        """, language="python")
        st_space("v", 2)

        # --- Buffer stack leaks ---
        st_write(bs.sub, "Buffer stack leaks", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The export buffer uses a stack for nested wrappers. If a
            test calls export_push_wrapper() without a matching
            export_pop_wrapper(), the stack leaks into the next test.
            Always pair push/pop in a try/finally or use
            reset_export_buffer() in teardown.
        """)
        st_space("v", 1)

        show_code("""\
            def test_nested_export():
                from streamtex import (
                    export_push_wrapper,
                    export_pop_wrapper,
                    reset_export_buffer,
                    set_export_active,
                )

                reset_export_buffer()
                set_export_active(True)
                try:
                    export_push_wrapper("<div>")
                    # ... test logic ...
                    export_pop_wrapper("</div>")
                finally:
                    set_export_active(False)
                    reset_export_buffer()\
        """, language="python")
        st_space("v", 2)

        # --- Streamlit context ---
        st_write(bs.sub, "Streamlit context requirements", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Some Streamlit functions require a running app context.
            If you see "NoSessionContext" errors in tests, it means
            the function needs either a mock or a Streamlit test
            harness. Most StreamTeX tests avoid this by mocking
            st.html() and other Streamlit calls.
        """)
        st_space("v", 2)

        # --- Import order ---
        st_write(bs.sub, "Import order matters", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Always import streamtex before importing custom modules
            that depend on it. The streamtex package initialises
            internal registries on import. If a custom module tries
            to use those registries before streamtex is loaded, you
            get ImportError or AttributeError.
        """)
        st_space("v", 1)

        show_code("""\
            # CORRECT order
            import streamtex as stx
            from custom.styles import Styles as s

            # WRONG — custom module may reference stx internals
            from custom.styles import Styles as s
            import streamtex as stx\
        """, language="python")
        st_space("v", 2)

        show_details("""\
            When a test fails only in CI but passes locally, the most
            common cause is singleton state leaking between tests. The
            test execution order may differ, exposing hidden
            dependencies. Add reset calls and re-run.
        """)
