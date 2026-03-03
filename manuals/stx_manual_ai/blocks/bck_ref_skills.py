"""Part 8 — Reference: All Skills — detailed listing of all skill files."""

from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation

class BlockStyles:
    """Skills reference block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    skill_card = Style(
        "background: rgba(6, 182, 212, 0.06); "
        "border-left: 3px solid #06B6D4; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "ref_skill_card",
    )
    skill_name = s.project.colors.cyber_cyan + s.bold + s.large
    label = s.project.colors.tech_blue + s.bold + s.medium
    value = s.medium

bs = BlockStyles

def _render_skill(name: str, description: str, used_by: str,
                  profiles: str):
    """Render a single skill entry inside a styled card."""
    with st_block(bs.skill_card):
        st_write(bs.skill_name, name, tag=t.div)
        st_space("v", 0.5)
        st_write(s.large, description)
        st_space("v", 0.5)
        st_write(bs.label, "Used by: ", (bs.value, used_by))
        st_space("v", 0.3)
        st_write(bs.label, "Profiles: ", (bs.value, profiles))

def build():
    """Render the complete skills reference."""
    st_space("v", 1)
    st_write(bs.heading, "Reference: All Skills", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Skills are Markdown files that agents automatically load as
        context before performing actions. They contain domain knowledge,
        rules, and templates that guide AI behavior. Below is the
        complete reference for all skills.
    """)
    st_space("v", 2)

    # ── Designer Skills ───────────────────────────────────────────
    st_write(bs.sub, "Designer Skills", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_skill(
                "block-blueprints.md",
                "Contains 10 block templates covering common slide "
                "patterns: title, content, comparison, code demo, "
                "exercise, summary, and more.",
                "Slide Designer, Project Architect",
                "all profiles",
            )
            st_space("v", 1)
            _render_skill(
                "visual-design-rules.md",
                "Design rules for visual quality: spacing, alignment, "
                "color usage, typography hierarchy, container nesting "
                "depth, and readability constraints.",
                "Slide Designer, Slide Reviewer, Presentation Designer",
                "all profiles",
            )
        with g.cell():
            _render_skill(
                "style-conventions.md",
                "Naming conventions for Style objects, BlockStyles "
                "class organization, style composition patterns, "
                "and reuse guidelines.",
                "Slide Designer",
                "all profiles",
            )
            st_space("v", 1)
            _render_skill(
                "streamtex-quick-reference.md",
                "Compact API syntax reference for all stx functions: "
                "st_write, st_grid, st_block, st_list, st_image, "
                "and their parameters.",
                "all agents",
                "all profiles",
            )
    st_space("v", 2)

    # ── Shared Reference Skills ───────────────────────────────────
    st_write(bs.sub, "Shared Reference Skills", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_skill(
                "coding_standards.md",
                "Full coding standards for StreamTeX projects. Covers "
                "block structure, import rules, style composition, "
                "helper usage, and anti-patterns to avoid.",
                "all agents (shared reference)",
                "all profiles",
            )
        with g.cell():
            _render_skill(
                "streamtex_cheatsheet_en.md",
                "Quick cheatsheet with the most common stx function "
                "calls, Style combinations, and block patterns. "
                "Designed for fast lookup during development.",
                "all agents (shared reference)",
                "all profiles",
            )
    st_space("v", 2)

    # ── Library-Only Skills ───────────────────────────────────────
    st_write(bs.sub, "Library-Only Skills", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_skill(
                "testing-patterns.md",
                "Patterns for writing tests for StreamTeX components. "
                "Covers block validation, style assertion, rendering "
                "checks, and pytest fixtures.",
                "Developer agent",
                "library profile only",
            )
        with g.cell():
            _render_skill(
                "architecture.md",
                "Library architecture documentation: module structure, "
                "rendering pipeline, style system internals, block "
                "registry, and extension points.",
                "Developer agent",
                "library profile only",
            )
    st_space("v", 1)
