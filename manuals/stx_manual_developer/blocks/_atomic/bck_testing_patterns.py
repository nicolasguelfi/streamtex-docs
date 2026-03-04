"""Atomic block — Common test patterns."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Test patterns styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Common Test Patterns", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            StreamTeX tests follow recurring patterns. This section
            shows the most common ones with full code examples so you
            can replicate them in new test files.
        """)
        st_space("v", 2)

        # --- Mocking st.html ---
        st_write(bs.sub, "Mocking st.html() to capture output",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Most StreamTeX functions render content via st.html().
            In tests, we mock it to capture the HTML string and assert
            on its content without needing a running Streamlit server.
        """)
        st_space("v", 1)

        show_code("""\
            from unittest.mock import patch, MagicMock

            @patch("streamlit.html")
            def test_write_renders_text(mock_html):
                from streamtex import st_write
                from streamtex.styles import Style

                style = Style("color: red;", "test_style")
                st_write(style, "Hello")

                mock_html.assert_called_once()
                html_output = mock_html.call_args[0][0]
                assert "Hello" in html_output
                assert "color: red" in html_output\
        """, language="python")
        st_space("v", 2)

        # --- Testing style composition ---
        st_write(bs.sub, "Testing style composition", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Style objects support + (merge) and - (remove) operators.
            Test composition by asserting on the resulting .css string.
        """)
        st_space("v", 1)

        show_code("""\
            def test_style_addition():
                from streamtex.styles import Style

                a = Style("color: red;", "a")
                b = Style("font-weight: bold;", "b")
                merged = a + b

                assert "color: red" in merged.css
                assert "font-weight: bold" in merged.css

            def test_style_subtraction():
                from streamtex.styles import Style

                base = Style("color: red; font-size: 16px;", "base")
                result = base - "color: red;"

                assert "color: red" not in result.css
                assert "font-size: 16px" in result.css\
        """, language="python")
        st_space("v", 2)

        # --- Testing context managers ---
        st_write(bs.sub, "Testing context managers", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_block and st_grid are context managers that push/pop
            wrapper HTML. Test them by verifying the wrapper structure
            in the captured output.
        """)
        st_space("v", 1)

        show_code("""\
            @patch("streamlit.html")
            def test_block_wraps_content(mock_html):
                from streamtex import st_block, st_write
                from streamtex.styles import Style

                block_style = Style("padding: 10px;", "block")
                text_style = Style("color: blue;", "text")

                with st_block(block_style):
                    st_write(text_style, "Inside block")

                # Collect all HTML fragments
                calls = [c[0][0] for c in mock_html.call_args_list]
                full_html = "".join(calls)

                assert "padding: 10px" in full_html
                assert "Inside block" in full_html\
        """, language="python")
        st_space("v", 2)

        # --- Fixtures from conftest ---
        st_write(bs.sub, "Fixtures from conftest.py", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The tests/conftest.py file provides shared fixtures.
            The most important ones are mock_st_html (auto-patches
            st.html) and registry resets (clean singleton state).
        """)
        st_space("v", 1)

        show_code("""\
            # tests/conftest.py (excerpt)

            import pytest
            from unittest.mock import patch

            @pytest.fixture
            def mock_st_html():
                with patch("streamlit.html") as mock:
                    yield mock

            @pytest.fixture(autouse=True)
            def reset_registries():
                \"\"\"Reset all singleton state between tests.\"\"\"
                from streamtex import (
                    reset_toc_registry,
                    reset_bib_registry,
                    reset_export_buffer,
                )
                yield
                reset_toc_registry()
                reset_bib_registry()
                reset_export_buffer()\
        """, language="python")
        st_space("v", 2)

        # --- AST guard ---
        st_write(bs.sub, "AST guard: scanning for unsafe st.html() calls",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The AST guard test walks the source tree, parses each
            module with Python's ast module, and checks that every
            st.html() call site has a corresponding is_export_active()
            guard in the same function body.
        """)
        st_space("v", 1)

        show_code("""\
            # Simplified version of the AST guard test

            import ast
            from pathlib import Path

            def test_all_st_html_calls_are_guarded():
                src = Path("streamtex")
                for py_file in src.rglob("*.py"):
                    tree = ast.parse(py_file.read_text())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            has_html = _has_st_html_call(node)
                            has_guard = _has_export_guard(node)
                            if has_html and not has_guard:
                                raise AssertionError(
                                    f"{py_file}:{node.lineno} — "
                                    f"{node.name}() calls st.html() "
                                    f"without is_export_active() guard"
                                )\
        """, language="python")
        st_space("v", 2)

        # --- Testing export buffer ---
        st_write(bs.sub, "Testing the export buffer", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The export buffer collects HTML fragments during a page
            build. Test it by pushing a wrapper, appending content,
            popping the wrapper, and generating the final HTML.
        """)
        st_space("v", 1)

        show_code("""\
            def test_export_buffer_lifecycle():
                from streamtex import (
                    export_push_wrapper,
                    export_pop_wrapper,
                    export_append,
                    export_generate,
                    reset_export_buffer,
                    set_export_active,
                )

                reset_export_buffer()
                set_export_active(True)

                export_push_wrapper('<div class="page">')
                export_append("<p>Hello</p>")
                export_pop_wrapper("</div>")

                html = export_generate()
                assert "<p>Hello</p>" in html
                assert '<div class="page">' in html
                assert "</div>" in html

                set_export_active(False)
                reset_export_buffer()\
        """, language="python")
        st_space("v", 2)

        show_details("""\
            When writing a new test, look at the existing test file
            for the closest module first. Most patterns are already
            established and can be copied with minor adjustments.

            Always pair push_wrapper / pop_wrapper calls to avoid
            buffer stack leaks between tests.
        """)
