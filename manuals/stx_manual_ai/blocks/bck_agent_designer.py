"""Part 4 — Agents: Slide Designer and Slide Reviewer."""

import textwrap
from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Slide Designer & Reviewer block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Workflow arrow box
    workflow_box = Style(
        "background: rgba(6, 182, 212, 0.08); "
        "border: 1px solid rgba(6, 182, 212, 0.25); "
        "border-radius: 8px; padding: 20px;",
        "designer_workflow",
    )
    workflow_step = s.project.colors.cyber_cyan + s.bold + s.large
    workflow_text = s.large


bs = BlockStyles


def build():
    """Render the Slide Designer and Reviewer section."""
    st_space("v", 1)
    st_write(bs.heading, "Agents: Slide Designer & Reviewer",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        The Slide Designer and Slide Reviewer are two complementary
        agents that work in tandem. The Designer creates blocks;
        the Reviewer validates them. Together they form a
        create-then-audit loop that ensures quality output.
    """))
    st_space("v", 2)

    # ── Slide Designer ─────────────────────────────────────────────
    st_write(bs.sub, "Slide Designer", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(
            s.project.titles.subsection_title,
            "Creates visually polished, pedagogically structured blocks",
        )
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(
                s.large,
                "Enforces ",
                (s.bold, "~45-character lines "),
                "for readability",
            )
            st_write(
                s.large,
                "Uses ",
                (s.bold, "32pt body text "),
                "as the standard baseline",
            )
            st_write(
                s.large,
                "Follows ",
                (s.bold, "canonical block structure: "),
                "BlockStyles, build(), helpers",
            )
            st_write(
                s.large,
                "Detects anti-patterns: string concatenation, "
                "missing examples, raw st.write",
            )
            st_write(
                s.large,
                "Reads visual design rules and style conventions "
                "before generating",
            )
    st_space("v", 2)

    # ── Slide Reviewer ─────────────────────────────────────────────
    st_write(bs.sub, "Slide Reviewer", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.subsection_title,
            "Reviews completed slides for compliance",
        )
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(
                s.large,
                (s.bold, "Structure "),
                "— BlockStyles class, build() function, imports",
            )
            st_write(
                s.large,
                (s.bold, "Visual quality "),
                "— consistent styles, proper spacing, grid usage",
            )
            st_write(
                s.large,
                (s.bold, "Pedagogical flow "),
                "— logical progression, explanations before code",
            )
            st_write(
                s.large,
                (s.bold, "Formatting "),
                "— line lengths, text sizes, no hardcoded colors",
            )
    st_space("v", 2)

    # ── Workflow ───────────────────────────────────────────────────
    st_write(bs.sub, "Design-Review Workflow", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.workflow_box):
        st_write(
            bs.workflow_step, "1. Designer creates ",
            (bs.workflow_text, "a new block from description"),
        )
        st_space("v", 0.5)
        st_write(
            bs.workflow_step, "2. Reviewer validates ",
            (bs.workflow_text, "the block against all criteria"),
        )
        st_space("v", 0.5)
        st_write(
            bs.workflow_step, "3. If issues found ",
            (bs.workflow_text, "— Designer fixes and resubmits"),
        )
        st_space("v", 0.5)
        st_write(
            bs.workflow_step, "4. Final pass ",
            (bs.workflow_text,
             "— Reviewer confirms compliance, block is ready"),
        )
    st_space("v", 2)

    # ── Example review output ──────────────────────────────────────
    st_write(bs.sub, "Example Review Output", toc_lvl="+1")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Slide Review — bck_05_prerequisites.py
        # ─────────────────────────────────────

        Structure ............. PASS
          - BlockStyles class present
          - build() function defined
          - Correct imports

        Visual quality ........ PASS
          - Consistent style usage
          - Proper st_space() spacing
          - Grid layout well-formed

        Pedagogical flow ...... PASS
          - Explanation before code
          - Logical section progression
          - Summary/details at end

        Formatting ............ FAIL
          - Line 42: line exceeds 45 chars
          - Line 67: missing st_space after code

        Result: 3/4 PASS — 1 fix required
    """), language="text", line_numbers=False)
    st_space("v", 1)

    show_details(textwrap.dedent("""\
        The Reviewer returns a structured pass/fail report for each
        criterion. When a check fails, it includes the exact line
        number and a description of the issue. The Designer can then
        target its fixes precisely, avoiding unnecessary changes to
        passing sections.
    """))
    st_space("v", 1)
