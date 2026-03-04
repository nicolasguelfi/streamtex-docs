"""Atomic block — Running tests."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Running tests styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Running Tests", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            StreamTeX uses pytest as its test runner. All tests live
            in the tests/ directory and follow the test_<module>.py
            naming convention. Always run tests through uv run so the
            managed virtual environment is used.
        """)
        st_space("v", 2)

        # --- Full suite ---
        st_write(bs.sub, "Full test suite", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
            # Run every test with verbose output
            uv run pytest tests/ -v\
        """, language="bash")
        st_space("v", 2)

        # --- Single file ---
        st_write(bs.sub, "Single test file", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Target a specific module's tests by passing the file path.
        """)
        st_space("v", 1)

        show_code("""\
            # Run only the st_write tests
            uv run pytest tests/test_write.py -v\
        """, language="bash")
        st_space("v", 2)

        # --- By keyword ---
        st_write(bs.sub, "Filter by keyword", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use the -k flag to run tests matching a keyword expression.
            This is useful when working on a specific feature.
        """)
        st_space("v", 1)

        show_code("""\
            # Run all tests with "style" in their name
            uv run pytest tests/ -k "test_style" -v\
        """, language="bash")
        st_space("v", 2)

        # --- CLI shortcut ---
        st_write(bs.sub, "CLI shortcut", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX provides a CLI command that wraps the test
            runner with sensible defaults.
        """)
        st_space("v", 1)

        show_code("""\
            # Equivalent to uv run pytest tests/ -v
            stx test\
        """, language="bash")
        st_space("v", 2)

        # --- Coverage ---
        st_write(bs.sub, "Test coverage", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Generate a coverage report to see which lines are
            exercised by the test suite.
        """)
        st_space("v", 1)

        show_code("""\
            # Run tests with coverage measurement
            uv run pytest --cov=streamtex tests/

            # Generate an HTML coverage report
            uv run pytest --cov=streamtex --cov-report=html tests/\
        """, language="bash")
        st_space("v", 2)

        # --- Command summary ---
        st_write(bs.sub, "Command summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Command")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv run pytest tests/ -v")
            with g.cell(): st_write(s.large, "Full test suite")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv run pytest tests/test_write.py -v")
            with g.cell(): st_write(s.large, "Single file")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         'uv run pytest tests/ -k "style" -v')
            with g.cell(): st_write(s.large, "Filter by keyword")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx test")
            with g.cell(): st_write(s.large, "CLI shortcut")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "uv run pytest --cov=streamtex tests/")
            with g.cell(): st_write(s.large, "Coverage report")
        st_space("v", 2)

        show_details("""\
            If tests fail after a git pull, run uv sync first to ensure
            dependencies are up to date.

            Use the --tb=short flag for condensed tracebacks, or
            --tb=long for full stack traces when debugging failures.
        """)
