"""Part 5 — Skills Overview: .md knowledge bases loaded by agents."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Skills overview block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Skill card
    skill_card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 3px solid #8B5CF6; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "skill_card",
    )
    skill_name = s.project.colors.ai_violet + s.bold + s.large
    skill_desc = s.large


bs = BlockStyles


def build():
    """Render the Skills & Knowledge Bases overview section."""
    st_space("v", 1)
    st_write(bs.heading, "Skills & Knowledge Bases",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── What are skills ───────────────────────────────────────────
    show_explanation(textwrap.dedent("""\
        Skills are Markdown files that agents load as
        context before performing any action. They contain
        design rules, coding patterns, syntax references,
        and template blueprints. Each skill is a focused
        knowledge base that keeps the AI aligned with
        project conventions.
    """))
    st_space("v", 2)

    # ── Location ──────────────────────────────────────────────────
    st_write(bs.sub, "Where Skills Live", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.large,
        "Skills are stored in the ",
        (s.bold, ".claude/[role]/skills/ "),
        "directory, organized by profile role:",
    )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        .claude/
          designer/
            skills/
              block-blueprints.md
              visual-design-rules.md
              style-conventions.md
              streamtex-quick-reference.md
          references/
            coding_standards.md
            streamtex_cheatsheet_en.md
    """), language="text", line_numbers=False)
    st_space("v", 2)

    # ── Skills catalog ────────────────────────────────────────────
    st_write(bs.sub, "Skills Catalog", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "block-blueprints.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    10 template patterns for block creation.
                    Each blueprint defines a reusable layout
                    (title, content, comparison, gallery, etc.)
                """))
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "visual-design-rules.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    Styling, layout, and typography rules.
                    Covers font sizes, line lengths, spacing,
                    color usage, and grid conventions.
                """))
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "style-conventions.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    Naming conventions and style composition
                    patterns. How to create, combine, and
                    reuse Style objects across blocks.
                """))
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "streamtex-quick-reference.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    Syntax reference for all stx functions.
                    Covers st_write, st_grid, st_block,
                    st_list, st_space, and more.
                """))
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "coding_standards.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    Full coding standards document. The single
                    source of truth for all StreamTeX code.
                    Shared across every profile and agent.
                """))
        with g.cell():
            with st_block(bs.skill_card):
                st_write(
                    bs.skill_name,
                    "streamtex_cheatsheet_en.md",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.skill_desc, textwrap.dedent("""\
                    Quick syntax cheatsheet for rapid lookup.
                    Compact reference for the most common
                    stx function signatures and patterns.
                """))
    st_space("v", 2)

    # ── How agents reference skills ───────────────────────────────
    st_write(bs.sub, "How Agents Load Skills", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.large,
        "Each agent's Markdown file contains a ",
        (s.bold, "Context Loading "),
        "section that lists which skills to read "
        "before executing any step:",
    )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        ## Context Loading
        Read the following files before proceeding:
        - block-blueprints.md
        - visual-design-rules.md
        - style-conventions.md
        - coding_standards.md
    """), language="markdown", line_numbers=False)
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The agent reads every listed skill into its context
        window before generating any code. This ensures that
        all output conforms to the project's coding standards,
        visual rules, and naming conventions — without you
        having to paste rules into the conversation.
    """))
    st_space("v", 2)

    # ── Single source of truth ────────────────────────────────────
    st_write(bs.sub, "Single Source of Truth", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "coding_standards.md is the master reference",
        )
        st_space("v", 1)
        st_write(s.large, textwrap.dedent("""\
            All agents and commands ultimately defer to
            coding_standards.md for definitive rules. Other
            skills (blueprints, design rules, cheatsheet) are
            specialized extracts that help agents focus on
            specific tasks — but when in doubt, the coding
            standards document wins.
        """))
    st_space("v", 1)

    show_details(textwrap.dedent("""\
        You can add custom skills by creating new .md files
        in the skills/ directory. Each skill should focus on
        a single topic and use clear, imperative language
        that the AI can follow as instructions. Keep skills
        under 2000 lines to fit comfortably in the context
        window.
    """))
    st_space("v", 1)
