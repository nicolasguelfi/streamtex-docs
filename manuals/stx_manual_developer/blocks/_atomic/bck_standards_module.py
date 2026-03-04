"""Atomic block — Convention for adding a new module."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Module convention styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Adding a New Module", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            Follow this checklist when adding a new module to the
            StreamTeX package. Each step ensures the module integrates
            correctly with the public API, test suite, and export
            pipeline.
        """)
        st_space("v", 2)

        # --- Step 1: Create the file ---
        st_write(bs.sub, "1. Create the module file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Create the file inside streamtex/ following snake_case naming.
            If the module is part of a subsystem (e.g. CLI), place it in
            the corresponding sub-directory.
        """)
        st_space("v", 1)

        show_code("""\
            # Example: streamtex/my_feature.py
            # or:      streamtex/cli/cmd_my_feature.py\
        """, language="text")
        st_space("v", 2)

        # --- Step 2: Define public API ---
        st_write(bs.sub, "2. Define the public API", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Define the functions and classes that users will call.
            Add type hints for all public parameters and return values.
            Prefix internal helpers with an underscore.
        """)
        st_space("v", 1)

        show_code("""\
            # streamtex/my_feature.py

            from __future__ import annotations

            def my_public_function(text: str, style: Style | None = None) -> str:
                \"\"\"One-line description of the function.\"\"\"
                return _internal_helper(text, style)

            def _internal_helper(text: str, style: Style | None) -> str:
                \"\"\"Not exported — underscore prefix.\"\"\"
                ...\
        """, language="python")
        st_space("v", 2)

        # --- Step 3: Export in __init__.py ---
        st_write(bs.sub, "3. Export in __init__.py", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Add the new public names to streamtex/__init__.py. Update
            both the import statement and the __all__ list so that
            `from streamtex import *` picks up the new symbols.
        """)
        st_space("v", 1)

        show_code("""\
            # In streamtex/__init__.py

            from streamtex.my_feature import my_public_function   # new import

            __all__ = [
                ...
                "my_public_function",    # add to __all__
            ]\
        """, language="python")
        st_space("v", 2)

        # --- Step 4: Follow existing patterns ---
        st_write(bs.sub, "4. Follow existing patterns", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX uses recurring design patterns. Match the one
            that fits your module:
        """)
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Pattern")
            with g.cell(): st_write(s.bold + s.large, "When to use")
            with g.cell(): st_write(s.large, "Singleton config")
            with g.cell():
                st_write(s.large,
                         "Module has global state (set_*/get_*/reset_*)")
            with g.cell(): st_write(s.large, "Dataclass config")
            with g.cell():
                st_write(s.large,
                         "Module accepts a configuration bundle")
            with g.cell(): st_write(s.large, "_render() + export")
            with g.cell():
                st_write(s.large,
                         "Module produces HTML output")
        st_space("v", 2)

        # --- Step 5: Implement export support ---
        st_write(bs.sub, "5. Implement export support (if applicable)",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            If the module renders HTML via st.html(), it must support
            the export pipeline. Implement the _render() pattern with
            an is_export_active() guard and export_append() call.
        """)
        st_space("v", 1)

        show_code("""\
            def _render(style, content, tag):
                html = f'<{tag} style="{style.css}">{content}</{tag}>'
                st.html(html)
                if is_export_active():
                    export_append(html)\
        """, language="python")
        st_space("v", 2)

        # --- Step 6: Write tests ---
        st_write(bs.sub, "6. Write tests", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Create a test file at tests/test_<module>.py. Mock st.html()
            to capture output. Reset all singleton state between tests.
        """)
        st_space("v", 1)

        show_code("""\
            # tests/test_my_feature.py

            import pytest
            from unittest.mock import patch
            from streamtex.my_feature import my_public_function

            def test_basic_output(mock_st_html):
                result = my_public_function("hello")
                assert "hello" in result\
        """, language="python")
        st_space("v", 2)

        # --- Step 7: Run checks ---
        st_write(bs.sub, "7. Run the full check suite", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            # Run all tests
            uv run pytest tests/ -v

            # Lint the package
            uv run ruff check streamtex/

            # Both must pass before committing\
        """, language="bash")
        st_space("v", 2)

        show_details("""\
            For modules that manage singleton state, always provide a
            reset_*() function so tests can restore a clean state.

            Example: reset_toc_registry(), reset_bib_registry(),
            reset_export_buffer().
        """)
