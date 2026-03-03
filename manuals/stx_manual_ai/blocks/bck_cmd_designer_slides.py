"""Designer: Slide Commands — slide-new, slide-audit, slide-fix pipeline."""

import textwrap

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Slide commands block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cmd_title = s.project.colors.ai_violet + s.bold + s.Large
    step_label = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Render the Designer Slide Commands section."""
    st_space("v", 1)
    st_write(bs.heading, "Designer: Slide Commands",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        The three slide commands form a creation-validation-fix pipeline.
        First create a slide with slide-new, then validate it with
        slide-audit, and finally auto-fix any violations with slide-fix.
    """))
    st_space("v", 2)

    # ── Command 1: slide-new ───────────────────────────────────────
    st_write(bs.sub, "/designer:slide-new", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Create a New Slide Block", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Describe the content you need. The AI selects the best ",
            (s.bold, "blueprint "),
            "(layout template), generates a fully styled block file, and ",
            "places it in your blocks/ directory.",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        /designer:slide-new

        > Create a slide comparing Python vs Java performance.
          Use a two-column layout with bullet points.
          Include a code snippet in each column."""),
        language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large, "The AI generates:")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # bck_python_vs_java.py (generated)
        \"\"\"Comparison slide — Python vs Java performance.\"\"\"

        import textwrap
        from streamtex import st_write, st_space, st_block, st_grid
        from streamtex.enums import Tags as t
        from custom.styles import Styles as s
        from blocks.helpers import show_code

        class BlockStyles:
            heading = s.project.titles.section_title + s.center_txt
            col_title = s.project.titles.subsection_title
            # ... more styles

        bs = BlockStyles

        def build():
            st_space("v", 1)
            st_write(bs.heading, "Python vs Java", tag=t.div, toc_lvl="1")
            st_space("v", 2)
            with st_grid(cols=2) as g:
                with g.cell():
                    # Python column ...
                with g.cell():
                    # Java column ..."""), language="python")
    st_space("v", 2)

    # ── Command 2: slide-audit ─────────────────────────────────────
    st_write(bs.sub, "/designer:slide-audit", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Validate Design Compliance", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Checks every block in the project against StreamTeX coding ",
            "standards. The audit reports issues in four categories:",
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
            (s.bold, "Spacing "),
            "— consistent st_space() usage between elements",
        )
        st_write(
            s.large,
            (s.bold, "Style usage "),
            "— no inline CSS, no hardcoded colors",
        )
        st_write(
            s.large,
            (s.bold, "Text density "),
            "— too much content per slide, readability",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        /designer:slide-audit

        === Slide Audit Report ===
        bck_03_what_is_ml.py ........... PASS
        bck_04_supervised.py ........... WARN: text density > 80%
        bck_05_unsupervised.py ......... FAIL: inline CSS on line 42
        bck_06_neural_nets.py .......... PASS
        ---
        Result: 2 PASS, 1 WARN, 1 FAIL"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Command 3: slide-fix ───────────────────────────────────────
    st_write(bs.sub, "/designer:slide-fix", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Auto-Fix Design Violations", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Takes the audit results and automatically applies fixes. ",
            "Inline CSS is extracted into BlockStyles, spacing is ",
            "normalized, and text density warnings are resolved by ",
            "splitting oversized blocks.",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        /designer:slide-fix

        Fixing bck_05_unsupervised.py ...
          - Extracted inline CSS to BlockStyles.highlight
          - Replaced raw style string with bs.highlight
        Fixing bck_04_supervised.py ...
          - Split block into bck_04a and bck_04b (text density)
        Done: 2 files fixed, 0 errors."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Pipeline diagram ───────────────────────────────────────────
    st_write(bs.sub, "The Audit-Fix Pipeline", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols=3) as g:
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.step_label, "1. Create", tag=t.div)
                st_space("v", 1)
                st_write(s.large, "slide-new generates the block")
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(bs.step_label, "2. Audit", tag=t.div)
                st_space("v", 1)
                st_write(s.large, "slide-audit checks compliance")
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(bs.step_label, "3. Fix", tag=t.div)
                st_space("v", 1)
                st_write(s.large, "slide-fix resolves violations")
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Tip: always run slide-audit before committing your blocks.
        Catching issues early prevents style drift across your project.
        The audit-fix cycle is designed to be run repeatedly during
        development until all blocks pass.
    """))
    st_space("v", 1)
