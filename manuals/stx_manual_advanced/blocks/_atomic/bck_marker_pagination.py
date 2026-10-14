"""Markers in Paginated Mode — numbers, cross-page navigation, deep links.

Covers continuous vs paginated behaviour, the slide number every surface
shows, the floating widget, deep links (?marker= > ?slide= > ?page=,
page_url) and the files that implement the system.
"""

from streamtex import page_url, st_list, st_write, st_space
from streamtex.enums import Tags as t
from streamtex.marker import annotate_marker_numbers, marker_row_text
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Marker pagination styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    code = s.text.fonts.font_monospace + s.large


bs = BlockStyles

#: A small module, as the marker registry records it (module order):
#: a listed section, two break stops, a second section, one more stop.
_SAMPLE = [
    {"index": 0, "label": "Section A", "stop": True, "listed": True},
    {"index": 1, "label": "Marker 2", "stop": True, "listed": False, "auto": True},
    {"index": 2, "label": "Marker 3", "stop": True, "listed": False, "auto": True},
    {"index": 3, "label": "Section B", "stop": True, "listed": True},
    {"index": 4, "label": "Part B.1", "stop": False, "listed": True},
    {"index": 5, "label": "Marker 6", "stop": True, "listed": False, "auto": True},
]


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
        In continuous mode (paginate=False), going to a stop scrolls
        smoothly to it on the same page.
    """, breaks=False)
    st_space("v", 1)
    st_write(s.large, """\
        In paginated mode (paginate=True), the stops span several pages
        and the navigation changes page by itself. Each page knows its
        first and last stop:
    """, breaks=False)
    st_space("v", 1)

    show_explanation("""\
        Next at the last stop of a page opens the page of the next stop
        (its first stop) and scrolls to it; pages without a stop are
        skipped.

        Prev at the first stop of a page opens the page of the previous
        stop (its last stop).

        A page that has markers but no stop keeps the widget in sync with
        the nearest marker instead of jumping to the first one.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # One number per marker: its slide number
    # ------------------------------------------------------------------
    st_write(bs.sub, "One Number per Marker — Its Slide Number", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Stops are the slides of the book, numbered 1…N in module order.
        Every other marker takes the number of the slide it sits in (the
        last stop before it). The counter n / N, the presentation footer
        "Slide n / N", the ☰ popup, the sidebar Markers tab, the paginated
        page titles and ?slide=n all show that number, in paginated mode,
        continuous mode and the HTML export alike.
    """)
    st_space("v", 1)

    st_write(s.large, """\
        Each listed marker is a row of the marker list, and the row shows
        the range of slides it covers: from its own number to the last
        stop before the next listed marker. For a small module — Section A
        (listed stop), two break stops, Section B (listed stop), Part B.1
        (listed, no stop), one more break stop — the library numbers the
        rows like this (computed while this page renders):
    """, breaks=False)
    st_space("v", 1)

    entries = annotate_marker_numbers([dict(e) for e in _SAMPLE])
    with st_list(list_type="ul", l_style=bs.code, li_style=bs.code) as l:
        for e in entries:
            if e.get("listed"):
                with l.item():
                    st_write(bs.code, marker_row_text(e))
    st_space("v", 1)

    show_details("""\
        Five stops: the counter runs from "1 / 5" to "5 / 5". Section A
        covers slides 1–3 (its own stop and the two break stops after it).
        Section B covers slide 4 only, shown "4", because Part B.1 starts
        the next row; Part B.1 is not a stop, so it takes the number of the
        slide it sits in, 4, and its row runs to the last stop, "4–5". The
        row of the current section is highlighted while you navigate;
        stops placed before the first listed marker highlight the first
        row. The sidebar Markers tab shows the same text as the popup.
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
    """, breaks=False)
    st_space("v", 1)

    with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
        with l.item():
            st_write(s.large, (s.bold, "Counter"),
                     " \"n / N\": the current slide number over the number of stops "
                     "(e.g. \"3 / 12\"); click it to type a slide number")
        with l.item():
            st_write(s.large, (s.bold, "Prev"), " and ", (s.bold, "Next"),
                     " buttons: they walk the stops, one press per slide")
        with l.item():
            st_write(s.large, "A ", (s.bold, "☰ list button"),
                     " that opens a popup with the listed markers, one row per range "
                     "of slides (\"4–8. Section B\")")
        with l.item():
            st_write(s.large, "An optional ", (s.bold, "label"),
                     ": the name of the current row of the ☰ list — a listed marker shows "
                     "its own label; any other marker (hidden, or with no role left) "
                     "shows its section")
    st_space("v", 1)

    st_write(s.large, """\
        The popup lists the listed markers of every page. In paginated
        mode, clicking a row on another page changes page, then scrolls
        to that marker.
    """, breaks=False)
    st_space("v", 1)

    st_write(s.large, """\
        A scroll tracker updates the current position as you scroll
        manually, keeping the counter and the highlighted row in sync.
    """, breaks=False)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Deep links — open a book at a given marker, slide or page
    # ------------------------------------------------------------------
    st_write(bs.sub, "Deep Links — ?marker=, ?slide= and ?page=", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A paginated book opens on page 1 — unless the address says
        otherwise. Three URL parameters are honoured on the **first run of
        a session**, in the live app and, client-side, in the static HTML
        export (the static server ignores the query, so **one URL form
        works for both**):

        - `?marker=<key-or-slug>` — the `key=` given to `st_marker()`, or
          the slug of the marker label (`"Electricity"` → `electricity`),
          or the anchor of a TOC heading attached to a marker; the book
          opens on the marker's page **and scrolls to it**;
        - `?slide=<n>` — the slide number the counter shows (1-based);
        - `?page=<n>` — a 1-based page number.

        Precedence: `?marker=` > `?slide=` > `?page=`. An unknown value is
        ignored (page 1); no other parameter is read or modified, so a
        project's own `?lang=` travels untouched. The HTML export also
        accepts `#<key>` and the sidebar convention `#stx-goto-<n>`
        (0-based); a paginated export (one file per page) sends each of
        these links to the right file.
    """)
    st_space("v", 1)

    show_code("""\
# blocks/bck_wave_electricity.py — a stable key survives a translation
st_marker(T({"en": "Electricity", "fr": "Électricité"}, lang), key="electricity")

# blocks/bck_hub.py — link to that wave, in the reader's language
from streamtex import page_url
url = page_url("https://example.org/waves?lang=fr", marker="electricity")
# → https://example.org/waves?lang=fr&marker=electricity
page_url("https://example.org/waves", slide=37)   # → ...?slide=37
page_url("https://example.org/waves", page=12)    # → ...?page=12
# several given: marker= > slide= > page=, as the reader applies them""")
    st_space("v", 1)

    st_write(bs.feature, "Executed while this page renders:")
    st_space("v", 1)
    with st_list(list_type="ul", l_style=bs.code, li_style=bs.code) as l:
        for kwargs in ({"marker": "electricity"}, {"slide": 37}, {"page": 12},
                       {"marker": "electricity", "slide": 37, "page": 12}):
            args = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            with l.item():
                st_write(bs.code, f"page_url(base, {args}) → "
                                  f"{page_url('https://example.org/waves?lang=fr', **kwargs)}")
    st_space("v", 1)

    show_details("""\
        **Why a key?** Without `key=`, the deep link matches the slug of the
        label as rendered — `electricity` in English, `électricité` in
        French: a link built for one language misses in the other. The
        key is language-independent.

        **Which link to share?** `?marker=<key>` is the durable one. Slide
        numbers shift when a slide is added before; page numbers shift
        when a block is added, and also when the book changes how it cuts
        pages (`st_book(paginate_by=...)`, see the "Composing by Atoms"
        chapter).

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

        marker.py — MarkerRoles and MarkerConfig, the MarkerRegistry
        (each entry carries stop, listed, toc, stop_index and origin),
        st_marker() for manual placement, annotate_marker_numbers() which
        gives each entry its slide number and each listed entry its row,
        and inject_marker_navigation() which emits the floating widget +
        keyboard/scroll JavaScript.

        book.py — Lifecycle integration. Calls reset_marker_registry()
        before rendering blocks, starts a new slide at each book entry,
        then inject_marker_navigation() after. In paginated mode, it
        completes the page's live markers with the cached markers of the
        other pages, so the arrows and the numbers cover the whole book.

        write.py — _handle_toc() registers a heading's TOC entry, then
        _bridge_toc_marker() gives it its marker: none (marker=False), its
        own (True, a MarkerRoles, or the automatic one of
        auto_marker_on_toc with toc_marker_roles), or a link to the
        slide's marker (marker="attach"). It raises the "second
        navigation stop" warning.
    """)
    st_space("v", 1)

    show_code("""\
# Lifecycle in book.py (simplified)
reset_marker_registry(marker_config)  # 1. Init registry

for block in blocks:                   # 2. Render blocks
    marker_slide_boundary()            #    each entry opens a slide
    st_include(block)                  #    (st_write / st_marker / breaks register markers)

inject_marker_navigation()             # 3. annotate_marker_numbers() (slide numbers,
                                       #    popup rows), then emit widget + JS""")
