"""Part 8 — Reference: All Commands — complete table of 23 commands by category."""

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

    # ── Project Commands (5) ──────────────────────────────────────
    st_write(bs.sub, "Project Commands", toc_lvl="+1")
    st_write(bs.cat_count, "5 commands", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_command(
                "project-init",
                "Create a complete StreamTeX project from a natural "
                "language description. Generates styles, blocks, and book.py.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "project-customize",
                "Modify theme colors, fonts, and visual identity of "
                "an existing project without changing content.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "course-generate",
                "Generate a complete book.py from a CSV file listing "
                "block names and titles.",
                "all profiles",
            )
        with g.cell():
            _render_command(
                "collection-new",
                "Create a collection hub that aggregates multiple "
                "StreamTeX projects into a unified portal.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "project-upgrade",
                "Update project boilerplate (helpers, styles base, "
                "book.py patterns) to the latest StreamTeX version.",
                "all profiles",
            )
    st_space("v", 2)

    # ── Designer Commands (7) ─────────────────────────────────────
    st_write(bs.sub, "Designer Commands", toc_lvl="+1")
    st_write(bs.cat_count, "7 commands", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_command(
                "block-new",
                "Create a new block file with the standard structure: "
                "docstring, imports, BlockStyles, build().",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "slide-new",
                "Create a visually polished slide using a blueprint "
                "template. Enforces formatting and design rules.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "slide-audit",
                "Validate an existing slide against design rules. "
                "Returns pass/fail for each compliance criterion.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "slide-fix",
                "Auto-fix design rule violations detected by "
                "slide-audit. Applies corrections in place.",
                "all profiles",
            )
        with g.cell():
            _render_command(
                "style-audit",
                "Check style consistency across all blocks. Detects "
                "duplicated styles, unused definitions, naming issues.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "style-refactor",
                "Extract repeated style patterns into reusable "
                "definitions in the project Styles class.",
                "all profiles",
            )
            st_space("v", 1)
            _render_command(
                "block-preview",
                "Validate block structure without rendering. Checks "
                "imports, build() signature, and BlockStyles.",
                "all profiles",
            )
    st_space("v", 2)

    # ── Migration Commands (5) ────────────────────────────────────
    st_write(bs.sub, "Migration Commands", toc_lvl="+1")
    st_write(bs.cat_count, "5 commands", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_command(
                "html-migrate",
                "Convert a single HTML file into a native StreamTeX "
                "block with proper Style objects and stx functions.",
                "project, documentation",
            )
            st_space("v", 1)
            _render_command(
                "html-convert-batch",
                "Batch convert an entire directory of HTML files. "
                "Each file becomes one block in blocks/.",
                "project, documentation",
            )
            st_space("v", 1)
            _render_command(
                "html-convert-block",
                "Convert a previously saved HTML block (from a "
                "StreamTeX export) back into native Python code.",
                "project, documentation",
            )
        with g.cell():
            _render_command(
                "html-export",
                "Configure HTML export settings for a project. "
                "Sets output format, paths, and rendering options.",
                "project, documentation",
            )
            st_space("v", 1)
            _render_command(
                "conversion-audit",
                "Verify quality of converted blocks. Checks for "
                "leftover HTML, missing styles, and structural issues.",
                "project, documentation",
            )
    st_space("v", 2)

    # ── Developer Commands (3) ────────────────────────────────────
    st_write(bs.sub, "Developer Commands", toc_lvl="+1")
    st_write(bs.cat_count, "3 commands", tag=t.div)
    st_space("v", 1)

    _render_command(
        "test-run",
        "Run the project test suite with pytest. Executes all tests "
        "in the tests/ directory with verbose output.",
        "all profiles",
    )
    st_space("v", 1)
    _render_command(
        "lint",
        "Run ruff linter on the project. Checks code quality, "
        "unused imports, formatting, and style compliance.",
        "all profiles",
    )
    st_space("v", 1)
    _render_command(
        "deploy",
        "Deploy the project to a hosting platform. Configures "
        "Dockerfile, render.yaml, and environment variables.",
        "library only",
    )
    st_space("v", 2)

    # ── Presentation Commands (3) ─────────────────────────────────
    st_write(bs.sub, "Presentation Commands", toc_lvl="+1")
    st_write(bs.cat_count, "3 commands", tag=t.div)
    st_space("v", 1)

    _render_command(
        "presentation-audit",
        "Check slides for projection compliance: font sizes, "
        "contrast ratios, item counts, readability at distance.",
        "presentation only",
    )
    st_space("v", 1)
    _render_command(
        "presentation-fix",
        "Auto-fix projection violations. Enlarges fonts, reduces "
        "content density, improves contrast automatically.",
        "presentation only",
    )
    st_space("v", 1)
    _render_command(
        "survey-convert",
        "Convert survey screenshots into interactive StreamTeX "
        "blocks with charts and data visualization.",
        "presentation only",
    )
    st_space("v", 1)
