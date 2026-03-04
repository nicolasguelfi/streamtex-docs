"""Shared best practices block for training courses."""

from streamtex import *
import streamtex as stx


class BlockStyles:
    """Best practices block styles."""
    pass


def build():
    """Share best practices and patterns."""
    st_write(
        stx.StxStyles.large + stx.StxStyles.text.colors.reset,
        "Best Practices",
        toc_lvl="2"
    )
    st_space("v", 1)

    st_write(
        stx.StxStyles.large,
        "Follow these patterns for clean, maintainable code:"
    )
    st_space("v", 1)

    with st_list(list_type="ol") as l:
        with l.item():
            st_write(
                stx.StxStyles.medium,
                (stx.StxStyles.bold, "stx.* functions"), " for ALL content (st.* only for interactivity)"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Define one ", (stx.StxStyles.bold, "generic style"), ", reuse everywhere"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Use a single ", (stx.StxStyles.bold, "st_write()"), " with tuples for inline mixed-style text"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Never ", (stx.StxStyles.bold, "hardcode colors"), " — let Streamlit handle dark/light mode"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Use ", (stx.StxStyles.bold, "st_block()"), " and ", (stx.StxStyles.bold, "st_span()"), " for layout, not raw HTML"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Keep blocks ", (stx.StxStyles.bold, "atomic"), " and ", (stx.StxStyles.bold, "composable")
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Use ", (stx.StxStyles.bold, "export-aware widgets"), " (stx.st_dataframe, not st.dataframe) for HTML export"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Use ", (stx.StxStyles.bold, "Style composition"), " (+ / -) instead of raw CSS strings"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                "Run ", (stx.StxStyles.bold, "uv run ruff check"), " after every change"
            )

    st_space("v", 2)

    st_write(
        stx.StxStyles.large + stx.StxStyles.text.colors.reset,
        "Known Gotchas",
        toc_lvl="2"
    )
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                stx.StxStyles.medium,
                (stx.StxStyles.bold, "from streamtex import *"), " shadows Python builtins (list, type) — use list_type= parameter"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                (stx.StxStyles.bold, "Singleton registries"), " (TOC, bib, marker) persist across reruns — call ", (stx.StxStyles.bold, "reset_*()"), " in tests"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                (stx.StxStyles.bold, "st_html()"), " height=0 uses st.html(), height>0 uses components.html() iframe"
            )
        with l.item():
            st_write(
                stx.StxStyles.medium,
                (stx.StxStyles.bold, "Export buffer push/pop"), " must always be paired to avoid stack leaks"
            )

    st_space("v", 2)
