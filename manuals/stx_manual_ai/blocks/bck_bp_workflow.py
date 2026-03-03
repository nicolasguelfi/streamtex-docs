"""Best Practices — Optimal AI workflow and when to switch to manual coding."""

import textwrap

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Optimal workflow block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step_number = s.project.colors.ai_violet + s.bold + s.large
    step_text = s.large


bs = BlockStyles


def build():
    """Render the Optimal AI Workflow best practices section."""
    st_space("v", 1)
    st_write(bs.heading, "Optimal AI Workflow", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        Following a structured order of operations maximizes AI
        effectiveness and minimizes rework. This section covers the
        recommended workflow, when to switch to manual coding, and
        how to maintain project memory.
    """))
    st_space("v", 2)

    # ── Recommended order ─────────────────────────────────────────
    st_write(bs.sub, "Recommended Order of Operations", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(
            bs.step_number, "1. Plan ",
            (bs.step_text, "— Use Project Architect or describe structure"),
        )
        st_space("v", 0.5)
        st_write(
            bs.step_number, "2. Generate ",
            (bs.step_text, "— Use project-init or slide-new"),
        )
        st_space("v", 0.5)
        st_write(
            bs.step_number, "3. Audit ",
            (bs.step_text, "— Run slide-audit and style-audit"),
        )
        st_space("v", 0.5)
        st_write(
            bs.step_number, "4. Fix ",
            (bs.step_text, "— Apply fixes with slide-fix"),
        )
        st_space("v", 0.5)
        st_write(
            bs.step_number, "5. Review ",
            (bs.step_text, "— Manual review of output"),
        )
        st_space("v", 0.5)
        st_write(
            bs.step_number, "6. Iterate ",
            (bs.step_text, "— Refine specific blocks"),
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Typical session
        /project:project-init          # 1. Plan + Generate
        /designer:slide-audit          # 3. Audit all blocks
        /designer:slide-fix            # 4. Auto-fix violations
        # 5. Review in browser
        uv run streamlit run book.py
        # 6. Iterate on individual blocks
        /designer:slide-new            # Refine or add blocks"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── When to switch to manual ──────────────────────────────────
    st_write(bs.sub, "When to Switch to Manual Coding", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        AI excels at generating standard blocks, enforcing conventions,
        and handling repetitive tasks. Some scenarios require manual
        intervention for best results.
    """))
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(
                    s.project.colors.warning_amber + s.bold + s.large,
                    "Complex Interactivity",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Blocks with st.button, st.selectbox, or other
                    Streamlit widgets that require callback logic.
                    AI generates the structure; you wire the behavior.
                """))
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(
                    s.project.colors.warning_amber + s.bold + s.large,
                    "Custom JS/HTML Integrations",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Embedded JavaScript components, custom HTML
                    widgets, or third-party library integrations
                    that go beyond StreamTeX's rendering model.
                """))
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(
                    s.project.colors.warning_amber + s.bold + s.large,
                    "Performance-Critical Rendering",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Large datasets, real-time updates, or heavily
                    optimized layouts where manual profiling and
                    tuning are essential.
                """))
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(
                    s.project.colors.warning_amber + s.bold + s.large,
                    "Highly Specific Visual Effects",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Pixel-perfect animations, advanced CSS
                    transitions, or brand-specific visual
                    requirements that need manual refinement.
                """))
    st_space("v", 2)

    # ── MEMORY.md best practices ──────────────────────────────────
    st_write(bs.sub, "MEMORY.md Best Practices", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        MEMORY.md is Claude Code's persistent memory file. It stores
        project conventions and decisions that should persist across
        conversations. A well-maintained MEMORY.md reduces context
        re-explanation and keeps AI output consistent.
    """))
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "What to store in MEMORY.md",
            tag=t.div,
        )
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(
                s.large,
                (s.bold, "Project conventions "),
                "— naming rules, block structure patterns",
            )
            st_write(
                s.large,
                (s.bold, "Color palette decisions "),
                "— chosen theme, accent colors, contrast rules",
            )
            st_write(
                s.large,
                (s.bold, "Block status tracking "),
                "— which blocks are finalized, which need rework",
            )
            st_write(
                s.large,
                (s.bold, "Recurring patterns "),
                "— common layouts, shared helpers, style shortcuts",
            )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Example MEMORY.md entries
        ## Project Conventions
        - All titles use section_title style (tech_blue)
        - Maximum 8 items per list
        - Every block ends with show_details() tip

        ## Color Palette
        - Primary: #8B5CF6 (ai_violet)
        - Accent: #06B6D4 (cyber_cyan)
        - Background callouts use 12% opacity

        ## Block Status
        - bck_01 to bck_05: FINALIZED
        - bck_06: needs spacing review
        - bck_07 to bck_10: in progress"""),
        language="text", line_numbers=False)
    st_space("v", 2)

    # ── Final tip ─────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Tip: run the Plan-Generate-Audit-Fix cycle at least twice before
        manual review. The first pass catches structural issues; the
        second pass catches style inconsistencies. After two automated
        cycles, manual review can focus on content quality rather than
        formatting.
    """))
    st_space("v", 1)
