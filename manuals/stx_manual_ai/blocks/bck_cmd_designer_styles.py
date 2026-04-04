"""Designer: Style Commands — audit styles, fix styles, audit block via stx-block."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Style commands block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cmd_title = s.project.colors.ai_violet + s.bold + s.Large


bs = BlockStyles


def build():
    """Render the Designer Style Commands section."""
    st_space("v", 1)
    st_write(bs.heading, "Designer: Style Commands",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Style commands help you maintain consistency across your entire
        project. They detect duplicate styles, extract inline CSS into
        reusable classes, and validate the structural correctness of
        every block file.
    """)
    st_space("v", 2)

    # ── Command 1: audit --target styles ────────────────────────────
    st_write(bs.sub, "/stx-block:audit --target styles", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Check Style Consistency", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Scans every block and the project styles file to find ",
            "inconsistencies. It detects ", (s.bold, "three categories"), " of problems:",
        )
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.large,
                (s.bold, "Duplicate styles "),
                "— same CSS defined in multiple BlockStyles classes",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "Inline CSS "),
                "— raw style strings passed directly to stx functions",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "Hardcoded colors "),
                "— hex codes or rgb() used instead of project color classes",
            )
    st_space("v", 1)

    show_code("""\
        /stx-block:audit --target styles

        === Style Audit Report ===

        DUPLICATE STYLES (3 found):
          - "color: #8B5CF6; font-weight: bold" appears in:
            bck_03.py::BlockStyles.accent
            bck_07.py::BlockStyles.highlight
            bck_12.py::BlockStyles.emphasis
            -> Recommendation: use s.project.titles.feature_title

        INLINE CSS (1 found):
          - bck_09.py line 34: st_write(Style("color: red;", "x"), ...)
            -> Recommendation: define in BlockStyles or custom/styles.py

        HARDCODED COLORS (2 found):
          - bck_05.py line 18: "#FF5733"
          - bck_11.py line 22: "rgb(59, 130, 246)"
            -> Recommendation: use project color classes

        Summary: 6 issues found (3 duplicate, 1 inline, 2 hardcoded)""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Command 2: fix --target styles ─────────────────────────────
    st_write(bs.sub, "/stx-block:fix --target styles", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Refactor Repeated Styles", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Takes the audit results and performs automated refactoring. ",
            "Duplicate styles are consolidated into named classes in ",
            (s.bold, "custom/styles.py"), ", and all references are updated.",
        )
    st_space("v", 1)

    show_code("""\
        /stx-block:fix --target styles

        Refactoring 6 issues ...

        1. Consolidated 3 duplicate styles:
           Created: ColorsCustom.accent_violet
           Updated: bck_03.py, bck_07.py, bck_12.py

        2. Extracted inline CSS from bck_09.py:
           Created: BlockStyles.alert_text in bck_09.py

        3. Replaced hardcoded colors:
           bck_05.py: "#FF5733" -> s.project.colors.error_red
           bck_11.py: "rgb(...)" -> s.project.colors.tech_blue

        Done: 6 issues fixed across 5 files.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Command 3: audit --target <block> ──────────────────────────
    st_write(bs.sub, "/stx-block:audit --target <block>", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Validate Block Structure", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Validates the structural correctness of a block file ",
            "without running it. Checks that the file follows the ",
            "required StreamTeX block pattern:",
        )
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.large,
                (s.bold, "BlockStyles class "),
                "— must exist and define style attributes",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "build() function "),
                "— must be present as the entry point",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "Imports "),
                "— only stx functions, no raw st.markdown or st.write",
            )
        with l.item():
            st_write(
                s.large,
                (s.bold, "Docstring "),
                "— module-level docstring describing the block",
            )
    st_space("v", 1)

    show_code("""\
        /stx-block:audit --target bck_03_what_is_ml

        === Block Structure Check ===
        Module docstring ............. PASS
        BlockStyles class ............ PASS
        build() function ............. PASS
        Imports (stx only) ........... PASS
        bs = BlockStyles alias ....... PASS
        No raw st.* calls ............ PASS
        ---
        Result: VALID block structure""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Scope option ──────────────────────────────────────────────
    st_write(bs.sub, "Focused audits with --scope", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_explanation("""\
        The audit and fix commands support a --scope option to focus on
        a specific category of checks. This replaces the old separate
        slide-audit, style-audit, and slide-fix commands with a single,
        unified interface.
    """)
    st_space("v", 1)

    show_code("""\
        # Audit only visual design (slide layout, fonts, spacing)
        /stx-block:audit --target bck_intro --scope slide

        # Audit only style consistency (duplicates, inline CSS, colors)
        /stx-block:audit --all --scope style

        # Audit only structure (imports, BlockStyles, build(), raw HTML)
        /stx-block:audit --target bck_intro --scope structure

        # Fix only slide-related issues
        /stx-block:fix --target bck_intro --scope slide

        # Default: --scope all (checks everything)
        /stx-block:audit --all""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details("""\
        The recommended workflow is: run /stx-block:audit --target styles
        first to identify problems, then /stx-block:fix --target styles
        to fix them automatically. Use /stx-block:audit --target <block>
        to validate individual blocks during development. Use --scope to
        focus on specific categories when you know what to look for.
    """)
    st_space("v", 1)
