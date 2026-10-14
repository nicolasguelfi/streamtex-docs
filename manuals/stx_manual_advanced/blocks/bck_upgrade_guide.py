"""Upgrade Guide — retiring a project's own slide() helper; v0.2 to v0.3 migration."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Upgrade guide block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    """Upgrade Guide — slide() helper to st_slide; migration from v0.2 to v0.3."""
    st_write(bs.heading, "Upgrade Guide", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        This guide collects the migrations a StreamTeX project may need:
        first, retiring a project's own slide() helper in favour of
        st_slide(); then the move from version 0.2 to version 0.3, with
        its breaking changes, new features and step-by-step migration
        instructions.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 0. A project's own slide() helper -> st_slide
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "Retiring a Project's Own slide() Helper", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Some projects wrote their own slide(cut, style) helper: a break
        when cut is true, then the design system's slide box, plus the
        style of that slide. st_slide() is the same construction, with
        cut and style at the same positions and the same meaning, and it
        now carries what the helper could not: the slide's marker, the
        break's settings and slides without a box. Two lines retire the
        helper — no block file changes, no visual change.
    """)
    st_space("v", 1)

    st_write(bs.feature, "Step 1: Declare the slide box once, in book.py")
    st_space("v", 1)

    show_code("""\
        import streamtex as stx
        from custom.styles import Styles as s

        # the box the helper used, before st_book(); stored per session
        stx.set_slide_container(s.project.containers.slide_center)
    """, language="python")
    st_space("v", 1)

    st_write(bs.feature, "Step 2: Make the helper an alias")
    st_space("v", 1)

    show_code("""\
        # shared/slides.py — before
        @contextmanager
        def slide(cut: bool = False, style: Style | None = None):
            if cut:
                st_slide_break()
            box = s.project.containers.slide_center
            with st_block(box + style if style is not None else box):
                yield

        # shared/slides.py — after
        from streamtex import st_slide as slide
    """, language="python")
    st_space("v", 1)

    show_details("""\
        Every existing with slide(...) renders as before: the blocks keep
        importing slide from the project. Afterwards, slide by slide, the
        marker written apart can move onto the slide it belongs to
        (st_marker("RAG") then with slide(): becomes
        with slide(marker="RAG"):), a break that needs settings takes them
        (with slide(cut=True, zoom=80):) and a scrolling slide drops the box
        (with slide(marker="Long read", box=False):). See "One slide —
        st_slide()" in the Presentation Mode chapter.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 1. Breaking Changes
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "v0.3 — Breaking Changes", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(
            s.medium,
            "The following changes in v0.3 may require updates to existing "
            "projects. Review each item carefully before upgrading.",
        )
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.medium,
                    "Style system refactored: styles/ is now a package "
                    "(core.py, text.py, container.py, visibility.py, base.py)",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Import changes: from streamtex.styles import Style still works "
                    "(backward compatible)",
                )
            with l.item():
                st_write(
                    s.medium,
                    "BannerConfig (banner=) gives full control of the banner; banner_color= "
                    "remains a shortcut for its colour only",
                )
            with l.item():
                st_write(
                    s.medium,
                    "inspector= takes an InspectorConfig (a plain True is not accepted)",
                )
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 2. New Features
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "v0.3 — New Features", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(
            s.medium,
            "Version 0.3 introduces several major features that expand "
            "StreamTeX's capabilities for document authoring and data "
            "integration.",
        )
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.medium,
                    "Bibliography system (bib.py): multi-format import, "
                    "inline citations, hover preview",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Google Sheets integration (gsheet.py): public + "
                    "authenticated sheet access",
                )
            with l.item():
                st_write(
                    s.medium,
                    "LaTeX document rendering (st_latex_doc): full LaTeX.js support",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Export-aware widgets: stx.st_dataframe, stx.st_metric, etc.",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Block helpers DI pattern (BlockHelperConfig)",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Collection system (st_collection)",
                )
            with l.item():
                st_write(
                    s.medium,
                    "Link preview scaffold",
                )
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 3. Migration Steps
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "v0.3 — Migration Steps", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Follow these steps in order to migrate your project from
        v0.2 to v0.3. Each step can be verified independently
        before moving on.
    """)
    st_space("v", 1)

    # Step 1
    st_write(bs.feature, "Step 1: Update dependency")
    st_space("v", 1)

    show_code("""\
        uv add streamtex --upgrade
    """, language="bash")
    st_space("v", 2)

    # Step 2
    st_write(bs.feature, "Step 2: Use BannerConfig for more than the colour")
    st_space("v", 1)

    show_explanation("""\
        banner= takes a BannerConfig: mode, colour and the rest of the
        banner. banner_color= stays as a shortcut that sets the colour
        only; banner= wins when both are given.
    """)
    st_space("v", 1)

    show_code("""\
        # Before (v0.2)
        st_book(blocks, banner_color="rgba(211, 47, 47, 0.8)")

        # After (v0.3)
        from streamtex import BannerConfig
        st_book(blocks, banner=BannerConfig.full(color="rgba(211, 47, 47, 0.8)"))
    """, language="python")
    st_space("v", 2)

    # Step 3
    st_write(bs.feature, "Step 3: Replace inspector=True with InspectorConfig")
    st_space("v", 1)

    show_explanation("""\
        inspector= takes an InspectorConfig. The boolean of v0.2 is no
        longer accepted: st_book(inspector=True) fails.
    """)
    st_space("v", 1)

    show_code("""\
        # Before (v0.2)
        st_book(blocks, inspector=True)

        # After (v0.3)
        from streamtex import InspectorConfig
        st_book(blocks, inspector=InspectorConfig(enabled=True))
    """, language="python")
    st_space("v", 2)

    # Step 4
    st_write(bs.feature, "Step 4: Use export-aware widgets")
    st_space("v", 1)

    show_explanation("""\
        For HTML export compatibility, replace native st.* data
        widgets with their stx.st_* counterparts.
    """)
    st_space("v", 1)

    show_code("""\
        # Before (v0.2)
        import streamlit as st
        st.dataframe(df)
        st.metric("Revenue", "$1.2M")

        # After (v0.3)
        import streamtex as stx
        stx.st_dataframe(df)
        stx.st_metric("Revenue", "$1.2M")
    """, language="python")
    st_space("v", 2)

    # Step 5
    st_write(bs.feature, "Step 5: Run linter to catch import issues")
    st_space("v", 1)

    show_code("""\
        uv run ruff check
    """, language="bash")
    st_space("v", 2)

    # Step 6
    st_write(bs.feature, "Step 6: Run tests to verify")
    st_space("v", 1)

    show_code("""\
        uv run pytest tests/ -v
    """, language="bash")
    st_space("v", 2)
