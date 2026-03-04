from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Ruff configuration styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Ruff Configuration",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Configuration location ---
        st_write(bs.sub, "Configuration in pyproject.toml", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# pyproject.toml
[tool.ruff]
target-version = "py310"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401", "I001"]
"streamtex/components/html_*.py" = ["E501"]""", language="toml")
        st_space("v", 2)

        # --- Rules explained ---
        st_write(bs.sub, "Rules", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Rule Set")
            with g.cell(): st_write(s.bold + s.large, "Description")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "E")
            with g.cell():
                st_write(s.large, "pycodestyle errors (syntax, indentation)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "F")
            with g.cell():
                st_write(s.large, "pyflakes (unused imports, undefined names)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "I")
            with g.cell():
                st_write(s.large, "isort (import sorting and grouping)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "W")
            with g.cell():
                st_write(s.large, "pycodestyle warnings")
        st_space("v", 2)

        # --- Per-file ignores ---
        st_write(bs.sub, "Per-file ignores", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Some files require specific rule exceptions:

            - __init__.py files: F401 (unused imports) and I001
              (import order) are ignored because these files
              re-export symbols for public API convenience.

            - HTML component files (html_*.py): E501 (line length)
              is ignored because embedded HTML strings often exceed
              120 characters and splitting them harms readability.
        """)
        st_space("v", 2)

        # --- Running ruff ---
        st_write(bs.sub, "Running Ruff", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Check for lint errors
uv run ruff check streamtex/

# Auto-fix safe issues
uv run ruff check --fix streamtex/

# Check a specific file
uv run ruff check streamtex/core/writer.py""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            The --fix flag automatically resolves safe issues like
            import sorting and unused import removal. Always review
            the changes after running --fix before committing.
        """)
        st_space("v", 2)

        # --- Target version ---
        st_write(bs.sub, "Target version", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            target-version = "py310" tells Ruff to flag syntax or
            patterns that are incompatible with Python 3.10. This
            ensures the codebase remains compatible with the minimum
            supported Python version.
        """)
        st_space("v", 2)

        show_details("""\
            Run uv run ruff check before every commit. CI will
            reject pull requests with lint errors. Use --fix for
            quick cleanup, but always verify the changes.
        """)
        st_space("v", 2)

        # --- Pre-commit hooks ---
        st_write(bs.sub, "Pre-commit hooks", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Every StreamTeX repo uses pre-commit to auto-run ruff
            before each commit. This catches import ordering (I001)
            and other issues before they reach CI.
        """)
        st_space("v", 1)

        show_code("""\
# .pre-commit-config.yaml (identical in every repo)
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.2
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]""", language="yaml")
        st_space("v", 1)

        show_code("""\
# Setup (once per repo)
uv sync                       # installs pre-commit
uv run pre-commit install     # activates the git hook

# Workspace-wide install
stx workspace hooks           # all repos + projects/""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            --exit-non-zero-on-fix aborts the commit when ruff
            modifies files. This lets you review changes, re-stage,
            and commit again with clean code.
        """)
