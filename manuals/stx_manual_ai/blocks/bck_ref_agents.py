"""Part 8 — Reference: All Agents — detailed cards for the four AI agents."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation


class BlockStyles:
    """Agents reference block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    agent_card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 4px solid #8B5CF6; "
        "padding: 20px 24px; border-radius: 0 8px 8px 0;",
        "ref_agent_card",
    )
    agent_name = s.project.colors.ai_violet + s.bold + s.Large
    label = s.project.colors.tech_blue + s.bold + s.large
    value = s.large


bs = BlockStyles


def build():
    """Render the complete agents reference table."""
    st_space("v", 1)
    st_write(bs.heading, "Reference: All Agents", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        StreamTeX AI profiles include four specialized agents. Each
        agent is an autonomous workflow that reads context, makes
        decisions, and orchestrates multiple commands. Below is
        the complete reference for all four agents.
    """))
    st_space("v", 2)

    # ── Row 1: Project Architect + Slide Designer ─────────────────
    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Project Architect", tag=t.div)
                st_space("v", 1)

                st_write(bs.label, "Available in: ",
                         (bs.value, "all profiles"))
                st_space("v", 0.5)

                st_write(bs.label, "Trigger: ",
                         (bs.value, "Natural language project description"))
                st_space("v", 0.5)

                st_write(bs.label, "Auto-reads:")
                with st_list(list_type="ul"):
                    st_write(s.large, "block-blueprints.md")
                    st_write(s.large, "visual-design-rules.md")
                    st_write(s.large, "coding_standards.md")
                st_space("v", 0.5)

                st_write(bs.label, "Key principles:")
                with st_list(list_type="ul"):
                    st_write(s.large, "1 block = 1 concept")
                    st_write(s.large, "Maximum 15 blocks per project")
                    st_write(s.large, "Logical progressive ordering")
                    st_write(s.large,
                             "Generates styles, blocks, and book.py")

        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Slide Designer", tag=t.div)
                st_space("v", 1)

                st_write(bs.label, "Available in: ",
                         (bs.value, "all profiles"))
                st_space("v", 0.5)

                st_write(bs.label, "Trigger: ",
                         (bs.value, "Block creation or modification request"))
                st_space("v", 0.5)

                st_write(bs.label, "Auto-reads:")
                with st_list(list_type="ul"):
                    st_write(s.large, "block-blueprints.md")
                    st_write(s.large, "visual-design-rules.md")
                    st_write(s.large, "style-conventions.md")
                st_space("v", 0.5)

                st_write(bs.label, "Key principles:")
                with st_list(list_type="ul"):
                    st_write(s.large,
                             "Enforces formatting and anti-pattern rules")
                    st_write(s.large,
                             "Uses blueprint templates for consistency")
                    st_write(s.large,
                             "Validates structure before completion")
                    st_write(s.large,
                             "Applies style composition patterns")

    st_space("v", 2)

    # ── Row 2: Slide Reviewer + Presentation Designer ─────────────
    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Slide Reviewer", tag=t.div)
                st_space("v", 1)

                st_write(bs.label, "Available in: ",
                         (bs.value, "all profiles"))
                st_space("v", 0.5)

                st_write(bs.label, "Trigger: ",
                         (bs.value, "Review request on completed slides"))
                st_space("v", 0.5)

                st_write(bs.label, "Auto-reads:")
                with st_list(list_type="ul"):
                    st_write(s.large, "visual-design-rules.md")
                    st_write(s.large, "style-conventions.md")
                    st_write(s.large, "coding_standards.md")
                st_space("v", 0.5)

                st_write(bs.label, "Key principles:")
                with st_list(list_type="ul"):
                    st_write(s.large,
                             "Returns pass/fail per compliance criterion")
                    st_write(s.large,
                             "Checks structure, visuals, and pedagogy")
                    st_write(s.large,
                             "Non-destructive: reports without modifying")
                    st_write(s.large,
                             "Suggests fixes for each failed criterion")

        with g.cell():
            with st_block(bs.agent_card):
                st_write(
                    bs.agent_name, "Presentation Designer", tag=t.div,
                )
                st_space("v", 1)

                st_write(bs.label, "Available in: ",
                         (bs.value, "presentation profile"))
                st_space("v", 0.5)

                st_write(bs.label, "Trigger: ",
                         (bs.value, "Presentation slide creation request"))
                st_space("v", 0.5)

                st_write(bs.label, "Auto-reads:")
                with st_list(list_type="ul"):
                    st_write(s.large, "visual-design-rules.md")
                    st_write(s.large, "block-blueprints.md")
                    st_write(s.large,
                             "streamtex-quick-reference.md")
                st_space("v", 0.5)

                st_write(bs.label, "Key principles:")
                with st_list(list_type="ul"):
                    st_write(s.large,
                             "Optimized for live projection (10-20m)")
                    st_write(s.large,
                             "Larger fonts, fewer items per slide")
                    st_write(s.large,
                             "High contrast for screen readability")
                    st_write(s.large,
                             "Maximum 5-7 items per visual block")

    st_space("v", 1)
