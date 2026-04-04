"""Part 8 — Reference: All Commands — stx-block commands (15)."""

from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation

class BlockStyles:
    """Commands reference block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cat_title = s.project.titles.subsection_title
    cat_count = s.project.colors.ai_violet + s.bold + s.large

    cmd_card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 3px solid #8B5CF6; "
        "padding: 14px 18px; border-radius: 0 6px 6px 0;",
        "ref_cmd_card",
    )
    cmd_name = s.project.colors.ai_violet + s.bold + s.large
    cmd_desc = s.large
    cmd_profiles = s.project.colors.cyber_cyan + s.medium

bs = BlockStyles

def _render_command(name: str, description: str, profiles: str):
    """Render a single command entry inside a card."""
    with st_block(bs.cmd_card):
        st_write(bs.cmd_name, name, tag=t.div)
        st_space("v", 0.5)
        st_write(bs.cmd_desc, description)
        st_space("v", 0.5)
        st_write(bs.cmd_profiles, "Profiles: ", (s.bold, profiles))

def build():
    """Render the complete commands reference table."""
    st_space("v", 1)
    st_write(bs.heading, "Reference: All Commands", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Complete reference of all StreamTeX AI commands organized by
        category. Each entry shows the command name, its description,
        and which profiles include it.
    """)
    st_space("v", 2)

    # ── stx-block Commands (15) ──────────────────────────────────
    st_write(bs.sub, "stx-block Commands", toc_lvl="+1")
    st_write(bs.cat_count, "15 commands", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_command(
                "/stx-block:init",
                "Create a complete StreamTeX project from a natural "
                "language description. Generates styles, blocks, and book.py. "
                "Consults manual examples when available (docs-lookup).",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:update",
                "Add blocks, slides, customize theme, generate courses, "
                "upgrade boilerplate, migrate HTML, or export. "
                "Uses manual blocks as reference.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:audit [--scope slide|style|structure|all]",
                "Validate quality with configurable scope: slide layout, "
                "style consistency, structural integrity, or full project "
                "audit. Compares against manual block patterns.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:fix [--scope slide|style|structure|all]",
                "Auto-fix issues found by audit with configurable scope: "
                "slide fixes, style refactoring, structural corrections, "
                "or full project fix. Follows manual block patterns.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:tool",
                "Run utility tools. Currently available: survey-convert "
                "(convert survey screenshots into interactive StreamTeX "
                "blocks with charts and data visualization).",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:new",
                "Create a new StreamTeX block file with proper structure: "
                "BlockStyles class, build() function, and helper imports.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:slide-new",
                "Create a new slide (block file) for a StreamTeX "
                "presentation project.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:preview",
                "Preview and validate a StreamTeX block by checking "
                "its structure and dependencies.",
                "all profiles",
            )
        with g.cell():
            _render_command(
                "/stx-block:style-refactor",
                "Audit and refactor styles in a block file for "
                "consistency and best practices.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:customize",
                "Customize a StreamTeX project: palette, fonts, "
                "layout, and theme settings.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:upgrade",
                "Upgrade a StreamTeX project to match the latest "
                "template version.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:collection-new",
                "Initialize a new StreamTeX collection (multi-project "
                "hub) from the template.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:course-generate",
                "Generate book.py for a course project from its "
                "blocks.csv configuration.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:test",
                "Run the project test suite with pytest. Executes all "
                "tests in the tests/ directory with verbose output.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "/stx-block:lint",
                "Run ruff linter on the project. Checks code quality, "
                "unused imports, formatting, and style compliance.",
                "all profiles",
            )
    st_space("v", 1)
