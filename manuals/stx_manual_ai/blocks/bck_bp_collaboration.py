"""Best Practices — Multi-user collaboration and cross-manual reuse."""

import textwrap

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Collaboration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Render the Multi-User Collaboration best practices section."""
    st_space("v", 1)
    st_write(bs.heading, "Multi-User Collaboration",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        StreamTeX projects are designed for team collaboration. Shared
        blocks, consistent profiles, and AI-assisted review enable
        multiple authors to work on the same project while maintaining
        visual and structural coherence.
    """))
    st_space("v", 2)

    # ── Shared blocks ─────────────────────────────────────────────
    st_write(bs.sub, "Using shared-blocks/ for Cross-Manual Reuse",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The shared-blocks/ directory contains blocks that can be reused
        across multiple manuals. Instead of duplicating code, you place
        common blocks there and import them via LazyBlockRegistry.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        streamtex-docs/
        └── manuals/
            ├── shared-blocks/           # Shared block library
            │   ├── bck_header.py        # Common header
            │   ├── bck_footer.py        # Common footer
            │   └── bck_disclaimer.py    # Legal disclaimer
            ├── stx_manual_intro/
            │   └── blocks/              # Manual-specific blocks
            └── stx_manual_advanced/
                └── blocks/              # Manual-specific blocks"""),
        language="bash", line_numbers=False)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # In book.py — importing shared blocks
        from streamtex import LazyBlockRegistry

        registry = LazyBlockRegistry(
            local_path="blocks",
            shared_path="../shared-blocks",
        )

        # Shared blocks are resolved automatically
        blocks = [
            "bck_header",        # Found in shared-blocks/
            "bck_01_intro",      # Found in local blocks/
            "bck_02_content",    # Found in local blocks/
            "bck_footer",        # Found in shared-blocks/
        ]"""), language="python")
    st_space("v", 2)

    # ── Code review with AI ───────────────────────────────────────
    st_write(bs.sub, "Code Review with AI", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        AI-assisted review complements human review. Use automated
        audits for structural compliance and agent-based review for
        comprehensive quality assessment.
    """))
    st_space("v", 1)

    with st_grid(cols=3, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Automated Audit",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Use slide-audit for fast, rule-based
                    checking of structure, spacing, style
                    usage, and text density.
                """))
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Agent Review",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Use the Slide Reviewer agent for
                    comprehensive review: pedagogy,
                    visual quality, and compliance.
                """))
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(
                    s.project.colors.tech_blue + s.bold + s.large,
                    "Human Review",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Combine AI review with human judgment
                    for content accuracy, tone, and
                    audience appropriateness.
                """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Review pipeline
        /designer:slide-audit          # Step 1: automated checks
        /designer:slide-fix            # Step 2: auto-fix violations
        # Step 3: agent-based comprehensive review
        # (invoke the Slide Reviewer agent)
        # Step 4: human review in browser
        uv run streamlit run book.py"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Team workflows ────────────────────────────────────────────
    st_write(bs.sub, "Team Workflows", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        In a team setting, clear role separation and shared conventions
        prevent style drift and conflicting changes. Here is a proven
        workflow for multi-author projects.
    """))
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "Recommended Team Roles",
            tag=t.div,
        )
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(
                s.large,
                (s.bold, "One architect plans "),
                "— designs the block structure and color palette using "
                "Project Architect, then shares the plan with the team",
            )
            st_write(
                s.large,
                (s.bold, "Multiple designers implement "),
                "— each team member generates and refines their assigned "
                "blocks using slide-new and slide-fix",
            )
            st_write(
                s.large,
                (s.bold, "Use a consistent profile "),
                "— all team members install the same .claude/ profile "
                "so that the AI follows identical conventions everywhere",
            )
            st_write(
                s.large,
                (s.bold, "Share custom styles "),
                "— the custom/styles.py file is the single source of "
                "truth for colors, fonts, and containers across the team",
            )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Team setup — every team member runs:
        stx claude install designer

        # The profile installs:
        # .claude/CLAUDE.md          — shared AI rules
        # .claude/settings.json      — shared permissions
        # .claude/designer/          — commands, agents, skills
        # custom/styles.py           — shared style definitions"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Version control tip ───────────────────────────────────────
    with st_block(s.project.containers.note_callout):
        st_write(
            s.project.titles.warning_label,
            "Version Control Your .claude/ Directory",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(s.large, (
            "Commands, agents, and skills are project-specific files "
            "stored in .claude/. Commit them to your repository so "
            "that every team member and CI environment uses the exact "
            "same AI configuration. This ensures consistent output "
            "regardless of who runs the commands."
        ))
    st_space("v", 2)

    # ── Final tip ─────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Tip: establish a review checklist early in the project. Define
        which aspects are checked by AI (structure, spacing, style
        compliance) and which require human review (content accuracy,
        tone, branding). This avoids duplicate effort and accelerates
        the review cycle.
    """))
    st_space("v", 1)
