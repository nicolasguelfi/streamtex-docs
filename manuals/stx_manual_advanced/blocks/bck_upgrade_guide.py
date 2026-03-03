"""Upgrade Guide — v0.2 to v0.3: breaking changes, new features, migration steps."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Upgrade guide block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    """Upgrade Guide — migration from v0.2 to v0.3."""
    st_write(bs.heading, "Upgrade Guide \u2014 v0.2 to v0.3", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        This guide covers everything you need to migrate a StreamTeX
        project from version 0.2 to version 0.3. It lists breaking
        changes, highlights new features, provides step-by-step
        migration instructions, and documents deprecated APIs.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 1. Breaking Changes
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "Breaking Changes", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The following changes in v0.3 may require updates to existing
        projects. Review each item carefully before upgrading.
    """)
    st_space("v", 1)

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
                "BannerConfig replaces the banner_color parameter in st_book()",
            )
        with l.item():
            st_write(
                s.medium,
                "InspectorConfig is now a proper dataclass (previously dict)",
            )
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 2. New Features
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "New Features", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Version 0.3 introduces several major features that expand
        StreamTeX's capabilities for document authoring and data
        integration.
    """)
    st_space("v", 1)

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
    st_write(bs.sub, "Migration Steps", toc_lvl="+1")
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

    show_code(textwrap.dedent("""\
        uv add streamtex --upgrade
    """), language="bash")
    st_space("v", 2)

    # Step 2
    st_write(bs.feature, "Step 2: Replace banner_color with BannerConfig")
    st_space("v", 1)

    show_explanation("""\
        The banner_color= parameter has been replaced by the
        banner= parameter which accepts a BannerConfig instance.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Before (v0.2)
        st_book(blocks, banner_color="rgba(211, 47, 47, 0.8)")

        # After (v0.3)
        from streamtex import BannerConfig
        st_book(blocks, banner=BannerConfig.full(color="rgba(211, 47, 47, 0.8)"))
    """), language="python")
    st_space("v", 2)

    # Step 3
    st_write(bs.feature, "Step 3: Replace inspector=True with InspectorConfig")
    st_space("v", 1)

    show_explanation("""\
        The boolean inspector= parameter has been replaced by
        the InspectorConfig dataclass for finer control.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Before (v0.2)
        st_book(blocks, inspector=True)

        # After (v0.3)
        from streamtex import InspectorConfig
        st_book(blocks, inspector=InspectorConfig(enabled=True))
    """), language="python")
    st_space("v", 2)

    # Step 4
    st_write(bs.feature, "Step 4: Use export-aware widgets")
    st_space("v", 1)

    show_explanation("""\
        For HTML export compatibility, replace native st.* data
        widgets with their stx.st_* counterparts.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Before (v0.2)
        import streamlit as st
        st.dataframe(df)
        st.metric("Revenue", "$1.2M")

        # After (v0.3)
        import streamtex as stx
        stx.st_dataframe(df)
        stx.st_metric("Revenue", "$1.2M")
    """), language="python")
    st_space("v", 2)

    # Step 5
    st_write(bs.feature, "Step 5: Run linter to catch import issues")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        uv run ruff check
    """), language="bash")
    st_space("v", 2)

    # Step 6
    st_write(bs.feature, "Step 6: Run tests to verify")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        uv run pytest tests/ -v
    """), language="bash")
    st_space("v", 2)

    # ------------------------------------------------------------------ #
    # 4. Deprecated APIs
    # ------------------------------------------------------------------ #
    st_write(bs.sub, "Deprecated APIs", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The following APIs are deprecated in v0.3. They continue
        to work for backward compatibility but will be removed in
        a future release. Update your code as described above.
    """)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.medium,
                "banner_color parameter (use BannerConfig instead)",
            )
        with l.item():
            st_write(
                s.medium,
                "Direct inspector=True (use InspectorConfig instead)",
            )
    st_space("v", 1)

    show_details("""\
        Both deprecated parameters still work in v0.3 and emit
        a deprecation warning at runtime. They will be removed
        in a future release. Plan your migration accordingly.
    """)
    st_space("v", 1)
