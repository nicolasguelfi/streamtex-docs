"""Markers in Paginated Mode — cross-page navigation & widget details.

Covers continuous vs paginated behaviour, cross-page navigation,
the floating widget internals, and the 3-file architecture.
"""

from streamtex import st_list, st_write, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Marker pagination styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title


bs = BlockStyles


def build():
    st_write(bs.heading, "Markers in Paginated Mode",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Continuous vs Paginated
    # ------------------------------------------------------------------
    st_write(bs.sub, "Continuous vs Paginated", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, """\
        In continuous mode (paginate=False), navigating between markers
        triggers a smooth scroll to the target element on the same page.

        In paginated mode (paginate=True), markers may span multiple
        pages. The navigation system handles page changes automatically:
    """)
    st_space("v", 1)

    show_explanation("""\
        When you press Next at the last marker of a page, the system
        switches to the next page and scrolls to its first marker.

        Similarly, pressing Prev at the first marker of a page returns
        to the previous page and scrolls to its last marker.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The floating widget
    # ------------------------------------------------------------------
    st_write(bs.sub, "The Floating Widget", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, """\
        When show_nav_ui=True (default), a floating widget appears
        with the following elements:
    """)
    st_space("v", 1)

    with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
        with l.item():
            st_write(s.large, (s.bold, "Position counter"), " showing \"current / total\" (e.g. \"3 / 12\")")
        with l.item():
            st_write(s.large, (s.bold, "Prev"), " and ", (s.bold, "Next"), " buttons")
        with l.item():
            st_write(s.large, "A ", (s.bold, "list button"), " that opens a popup with all markers")
        with l.item():
            st_write(s.large, "An optional ", (s.bold, "label"), " showing the current marker name")
    st_space("v", 1)

    st_write(s.large, """\
        The popup lists markers from all pages. In paginated mode,
        clicking a marker on a different page triggers a page change
        followed by a scroll to the target marker.
    """)
    st_space("v", 1)

    st_write(s.large, """\
        A scroll tracker updates the current marker as you scroll
        manually, keeping the counter and popup highlight in sync.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Deep links — open a deck at a given page or marker
    # ------------------------------------------------------------------
    st_write(bs.sub, "Deep Links — ?marker= and ?page=", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A paginated book opens on page 1 — unless the address says
        otherwise. Two URL parameters are honoured on the **first run of a
        session**, in the live app and, client-side, in the static HTML
        export (the static server ignores the query, so **one URL form
        works for both**):

        - `?marker=<key-or-slug>` — the `key=` given to `st_marker()`, or
          the slug of the marker label (`"Electricity"` → `electricity`);
          the book opens on the marker's page **and scrolls to it**;
        - `?page=<n>` — a 1-based page number.

        `?marker=` wins over `?page=`; an unknown value is ignored (page 1);
        no other parameter is read or modified, so a project's own `?lang=`
        travels untouched. The export also accepts `#<key>` and the
        sidebar convention `#stx-goto-<n>` (0-based).
    """)
    st_space("v", 1)

    show_code("""\
# blocks/bck_wave_electricity.py — a stable key survives a translation
st_marker(T({"en": "Electricity", "fr": "Électricité"}, lang), key="electricity")

# blocks/bck_hub.py — link to that wave, in the reader's language
from streamtex import page_url
url = page_url("https://example.org/waves?lang=fr", marker="electricity")
# → https://example.org/waves?lang=fr&marker=electricity
# page_url(base, page=12) gives ...?page=12 (1-based); marker= wins over page=""")
    st_space("v", 1)

    show_details("""\
        **Why a key?** Without `key=`, the deep link matches the slug of the
        label as rendered — `electricity` in English, `électricité` in
        French: a link built for one language misses in the other. The
        key is language-independent. Page numbers shift whenever a slide
        is added; prefer `marker=` over `page=` for anything you share.

        **Mechanism.** The page is resolved server-side from the marker
        cache (no extra render); the marker index is handed to the
        navigation JS as the initial widget position, so the intra-page
        scroll goes through the same path as cross-page navigation.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Architecture (for maintainers)
    # ------------------------------------------------------------------
    st_write(bs.sub, "Architecture Overview", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        Three files collaborate to implement the marker system:

        marker.py — MarkerConfig dataclass, MarkerRegistry singleton,
        st_marker() for manual placement, and inject_marker_navigation()
        which emits the floating widget + keyboard/scroll JavaScript.

        book.py — Lifecycle integration. Calls reset_marker_registry()
        before rendering blocks, then inject_marker_navigation() after.
        In paginated mode, passes page metadata so the JS can handle
        cross-page navigation via _stxMarkerBoundary and _stxMarkerGoToPage.

        write.py — The _handle_toc() function bridges TOC headings
        to markers. When a heading has a toc_lvl and the MarkerConfig
        is active, it calls register_marker() based on auto_marker_on_toc
        and the per-heading marker= parameter.
    """)
    st_space("v", 1)

    show_code("""\
# Lifecycle in book.py (simplified)
reset_marker_registry(marker_config)  # 1. Init registry

for block in blocks:                   # 2. Render blocks
    st_include(block)                  #    (st_write auto-registers markers)

inject_marker_navigation()             # 3. Emit widget + JS""")
