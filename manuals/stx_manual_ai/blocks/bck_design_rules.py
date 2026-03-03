"""Part 5 — Visual Design Rules: 9 rules with WRONG/CORRECT examples."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Design rules block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    rule_label = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Render the Visual Design Rules section."""
    st_space("v", 1)
    st_write(bs.heading, "Visual Design Rules",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The visual-design-rules.md skill defines 9 rules
        that every block must follow. These rules ensure
        consistent, readable, and maintainable output
        across all projects. Below are the rules with
        WRONG and CORRECT examples.
    """)
    st_space("v", 2)

    # ── Rule 1: Style composition ────────────────────────────────
    st_write(bs.sub, "The 9 Design Rules", toc_lvl="+1")
    st_space("v", 1)

    st_write(bs.rule_label, "Rule 1 — Use Style composition, "
             "not raw CSS", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(
                    s.project.colors.error_red + s.bold,
                    "WRONG",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_write(
                        Style("color: red; "
                              "font-weight: bold; "
                              "font-size: 24px;",
                              "my_style"),
                        "Important text",
                    )
                """), language="python", line_numbers=False)
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(
                    s.project.titles.subsection_title,
                    "CORRECT",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_write(
                        s.project.colors.error_red
                        + s.bold + s.Large,
                        "Important text",
                    )
                """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 2: One st_write with tuples ─────────────────────────
    st_write(bs.rule_label, "Rule 2 — One st_write with tuples "
             "for mixed styles", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(
                    s.project.colors.error_red + s.bold,
                    "WRONG",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_write(s.bold, "Name: ")
                    st_write(s.large, "Alice")
                    # Two calls = two vertical lines
                """), language="python", line_numbers=False)
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(
                    s.project.titles.subsection_title,
                    "CORRECT",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_write(
                        s.large,
                        (s.bold, "Name: "),
                        "Alice",
                    )
                    # One call = one inline line
                """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 3: No hardcoded colors ──────────────────────────────
    st_write(bs.rule_label, "Rule 3 — No hardcoded colors",
             tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(
                    s.project.colors.error_red + s.bold,
                    "WRONG",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    title = Style(
                        "color: #8B5CF6;",
                        "title",
                    )
                """), language="python", line_numbers=False)
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(
                    s.project.titles.subsection_title,
                    "CORRECT",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    title = (
                        s.project.colors.ai_violet
                        + s.bold
                    )
                """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 4: BlockStyles class ────────────────────────────────
    st_write(
        bs.rule_label,
        "Rule 4 — BlockStyles class required",
        tag=t.div,
    )
    st_space("v", 1)

    show_explanation("""\
        Every block file must define a BlockStyles class
        at the top. This class groups all style definitions
        for the block, keeping them organized and reusable.
        Always alias it as "bs" for concise usage.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        class BlockStyles:
            heading = s.project.titles.section_title
            sub = s.project.titles.section_subtitle

        bs = BlockStyles
    """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 5: build() function ─────────────────────────────────
    st_write(
        bs.rule_label,
        "Rule 5 — build() function as entry point",
        tag=t.div,
    )
    st_space("v", 1)

    show_explanation("""\
        Every block must expose a build() function with no
        required parameters. This is the entry point called
        by the book orchestrator. All rendering logic goes
        inside build().
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        def build():
            st_space("v", 1)
            st_write(bs.heading, "Title",
                     tag=t.div, toc_lvl="1")
            st_space("v", 2)
            # ... content ...
    """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 6: st_space for spacing ─────────────────────────────
    st_write(bs.rule_label, "Rule 6 — st_space for vertical "
             "spacing", tag=t.div)
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(
                    s.project.colors.error_red + s.bold,
                    "WRONG",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_write(s.large, "")
                    st_write(s.large, "")
                    # Empty writes for spacing
                """), language="python", line_numbers=False)
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(
                    s.project.titles.subsection_title,
                    "CORRECT",
                    tag=t.div,
                )
                st_space("v", 0.5)
                show_code(textwrap.dedent("""\
                    st_space("v", 2)
                    # Semantic spacing function
                """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Rule 7: ~45-char lines ───────────────────────────────────
    st_write(
        bs.rule_label,
        "Rule 7 — ~45-character lines for readability",
        tag=t.div,
    )
    st_space("v", 1)

    show_explanation("""\
        Keep text content to approximately 45 characters
        per line. This ensures comfortable reading on
        slides and prevents text from overflowing grid
        cells. Use textwrap.dedent for multi-line strings.
    """)
    st_space("v", 2)

    # ── Rule 8: 32pt minimum ─────────────────────────────────────
    st_write(
        bs.rule_label,
        "Rule 8 — 32pt minimum body text",
        tag=t.div,
    )
    st_space("v", 1)

    show_explanation("""\
        Body text must use s.large (32pt) or larger. Never
        use default size or s.small for content that readers
        need to see clearly. Titles use s.Large (40pt) or
        s.LARGE (48pt).
    """)
    st_space("v", 2)

    # ── Rule 9: Consistent imports ───────────────────────────────
    st_write(
        bs.rule_label,
        "Rule 9 — Consistent import patterns",
        tag=t.div,
    )
    st_space("v", 1)

    show_explanation("""\
        Every block follows the same import structure.
        Only import what you actually use. The canonical
        import order is: streamtex functions, enums,
        styles, then helpers.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        import textwrap
        from streamtex import (
            st_write, st_space, st_block, st_grid,
        )
        from streamtex.enums import Tags as t
        from custom.styles import Styles as s
        from blocks.helpers import (
            show_code, show_explanation,
        )
    """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Summary ──────────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "Why these rules matter",
        )
        st_space("v", 1)
        st_write(s.large, textwrap.dedent("""\
            These 9 rules are enforced by the Slide Reviewer
            agent. Every block is checked against them before
            being accepted. Following the rules from the start
            means fewer review iterations and faster delivery.
        """))
    st_space("v", 1)

    show_details("""\
        The visual-design-rules.md skill contains the full
        specification with additional examples and edge
        cases. Agents read this skill automatically before
        generating or reviewing blocks. You can also read
        it yourself to understand exactly what the AI
        checks for during a slide audit.
    """)
    st_space("v", 1)
