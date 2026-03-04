"""Part 2 — Understanding CLAUDE.md, the AI behavior configuration file."""

from streamtex import st_write, st_space, st_block
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """CLAUDE.md anatomy block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Understanding CLAUDE.md — sections, examples, and customization."""
    st_space("v", 1)
    st_write(bs.heading, "Understanding CLAUDE.md", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        CLAUDE.md is the central configuration file that tells
        Claude Code how to behave in your project. It defines
        the AI's identity, environment rules, coding standards,
        and available components.
    """)
    st_space("v", 2)

    # --- Identity ---
    st_write(bs.sub, "Identity Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The Identity section defines who the AI acts as. It sets
        the persona and specialization that shapes all responses.
    """)
    st_space("v", 1)

    show_code("""\
        ## Identity
        You are a **StreamTeX Expert** specialized in creating
        presentations and interactive documents.
        You NEVER write standard Streamlit code for content rendering.
        You ALWAYS use the `streamtex` library (`stx.*` functions).
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Environment ---
    st_write(bs.sub, "Environment Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The Environment section enforces mandatory runtime rules.
        The most important rule: always prefix Python commands
        with uv run.
    """)
    st_space("v", 1)

    show_code("""\
        ## Environment (MANDATORY)
        This project uses **uv** for dependency management. You MUST:
        - **ALWAYS** prefix Python commands with `uv run`
        - **NEVER** call `python`, `pip`, `pytest`, or `streamlit` directly
        - Use `uv add <package>` to add dependencies
        - Run `uv sync` if `uv.lock` or `pyproject.toml` changed
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Context Loading ---
    st_write(bs.sub, "Context Loading Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Context Loading tells Claude Code which files to read
        before generating any code. This ensures the AI understands
        your project's conventions.
    """)
    st_space("v", 1)

    show_code("""\
        ## Context Loading (MANDATORY before any code generation)
        Before writing any block code, you MUST read:
        1. `.claude/references/coding_standards.md`
        2. `.claude/references/streamtex_cheatsheet_en.md`
        3. The target manual's `book.py`
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Coding Standards ---
    st_write(bs.sub, "Coding Standards Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Coding Standards define the rules the AI must follow when
        writing StreamTeX code: stx functions over raw Streamlit,
        Style composition, block structure, and more.
    """)
    st_space("v", 1)

    show_code("""\
        ## Coding Standards
        - **stx for content, st for interactivity only**
        - **One st_write() with tuples for inline mixed-style text**
        - **No raw HTML/CSS** — use Style composition
        - **No hardcoded black/white** — let Streamlit handle themes
        - **Block files** need BlockStyles class + build() function
        - **After every code change**, run `uv run ruff check`
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Key Components ---
    st_write(bs.sub, "Key Components Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Key Components provides a quick API reference so the AI
        knows which StreamTeX functions are available without
        having to search the codebase.
    """)
    st_space("v", 1)

    show_code("""\
        ## Key Components
        ### Core Rendering
        - `st_write(style, text|tuple)` — Text rendering
        - `st_grid(cols, grid_style, cell_styles)` — CSS Grid layout
        - `st_block(style)`, `st_span(style)` — Containers
        - `st_list(list_type)` — List rendering

        ### Organization
        - `st_book(blocks, paginate=True)` — Book orchestration
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Customization ---
    st_write(bs.sub, "Customizing CLAUDE.md", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        You can add project-specific rules to CLAUDE.md at any
        time. Add them after the generated sections to avoid
        conflicts when updating the profile.
    """)
    st_space("v", 1)

    show_code("""\
        ## Project-Specific Rules
        - This project uses a dark theme — never override with light colors
        - All titles must use French language
        - Maximum 5 blocks per page section
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Template tip ---
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip")
        st_space("v", 1)
        st_write(s.large,
                 "CLAUDE.md is auto-generated from a profile template (",
                 (s.bold, "CLAUDE.md.j2"),
                 "). When you run ",
                 (s.bold, "stx claude install"),
                 ", the template is rendered with your project's configuration. "
                 "You can modify the generated file freely — it will not "
                 "be overwritten unless you explicitly reinstall.")
    st_space("v", 1)
