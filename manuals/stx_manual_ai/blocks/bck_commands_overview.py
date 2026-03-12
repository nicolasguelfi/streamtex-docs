"""Commands Overview — Slash commands anatomy, categories, and file structure."""

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Commands overview styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cat_title = s.project.titles.subsection_title
    cat_count = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Render the AI Commands Overview section."""
    st_space("v", 1)
    st_write(bs.heading, "AI Commands Overview", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Introduction ───────────────────────────────────────────────
    show_explanation("""\
        StreamTeX AI commands are slash commands that you type directly
        inside Claude Code. The syntax is always the same:
        /category:command-name. Each command loads its own context,
        reads the relevant coding standards, and walks the AI through
        a structured, step-by-step workflow.
    """)
    st_space("v", 2)

    # ── Slash command syntax ───────────────────────────────────────
    st_write(bs.sub, "Slash Command Syntax", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_code("""\
        /stx-designer:init
        /stx-designer:update
        /stx-designer:audit
        /stx-designer:fix
        /stx-designer:tool
        /stx-developer:test-run""", language="bash",
        line_numbers=False)
    st_space("v", 2)

    # ── Five categories grid ───────────────────────────────────────
    st_write(bs.sub, "Command Categories", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    # Row 1: stx-designer + Developer
    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(bs.cat_title, "stx-designer", tag=t.div)
                st_write(bs.cat_count, "5 sub-commands", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(s.large, "init — create projects")
                    with l.item(): st_write(s.large, "update — add/customize/migrate content")
                    with l.item(): st_write(s.large, "audit — validate quality")
                    with l.item(): st_write(s.large, "fix — auto-fix issues")
                    with l.item(): st_write(s.large, "tool — utilities (survey-convert)")
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(bs.cat_title, "Developer", tag=t.div)
                st_write(bs.cat_count, "3 commands", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item(): st_write(s.large, "test-run")
                    with l.item(): st_write(s.large, "lint")
                    with l.item(): st_write(s.large, "deploy")
    st_space("v", 2)

    # ── Anatomy of a command file ──────────────────────────────────
    st_write(bs.sub, "Anatomy of a Command File", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    st_write(
        s.large,
        "Each command is a ",
        (s.bold, ".md file "),
        "stored in the Claude profile. It has three sections:",
    )
    st_space("v", 1)

    with st_list(list_type="ol") as l:
        with l.item():
            st_write(s.large, (s.bold, "Description"),
                     " — what the command does")
        with l.item():
            st_write(s.large, (s.bold, "Context Loading"),
                     " — files the AI must read before proceeding")
        with l.item():
            st_write(s.large, (s.bold, "Workflow"),
                     " — step-by-step instructions for the AI")
    st_space("v", 1)

    show_code("""\
        # /stx-designer:init

        ## Description
        Create a complete StreamTeX project from a natural
        language description.

        ## Context Loading
        Read the following before proceeding:
        - coding_standards.md
        - streamtex_cheatsheet_en.md
        - The target manual's book.py

        ## Workflow
        1. Ask user for a project description
        2. Generate custom/styles.py from project theme
        3. Create blocks/ directory with starter blocks
        4. Generate book.py to orchestrate all blocks
        5. Validate structure with /stx-developer:lint""", language="markdown")
    st_space("v", 2)

    # ── Summary ────────────────────────────────────────────────────
    show_details("""\
        Every command follows the same pattern: description, context
        loading, then a step-by-step workflow. The AI reads the context
        files before executing any step, ensuring that all generated
        code conforms to StreamTeX coding standards.
    """)
    st_space("v", 1)
