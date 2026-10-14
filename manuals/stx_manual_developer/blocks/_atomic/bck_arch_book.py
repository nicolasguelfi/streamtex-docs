from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Book orchestration styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Book Orchestration",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. st_book() ---
        st_write(bs.sub, "st_book(): the main page generator", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_book() is the top-level function that generates
            a complete page. It accepts a list of block modules
            (each with a build() function) and renders them in
            sequence, managing pagination, TOC, and navigation.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_book
from blocks import bck_chapter_1, bck_chapter_2, bck_chapter_3

st_book(
    [bck_chapter_1, bck_chapter_2, bck_chapter_3],
    toc_config=toc,
    marker_config=markers,
    banner=banner,
)""")
        st_space("v", 2)

        # --- 2. TOCConfig ---
        st_write(bs.sub, "TOCConfig: table of contents", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            TOCConfig controls the sidebar table of contents:
            where heading numbers appear (sidebar, content, both or
            none), maximum sidebar depth, and search functionality.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import NumberingMode, TOCConfig

toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,  # BOTH (default), SIDEBAR_ONLY, MAIN_ONLY, NONE
    sidebar_max_level=3,                   # max depth shown in sidebar
    search=True,                           # enable TOC search
)""")
        st_space("v", 2)

        # --- 3. MarkerConfig ---
        st_write(bs.sub, "MarkerConfig: navigation markers", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            MarkerConfig turns on the marker registry, the floating
            navigation widget and the keys. Markers are anchor points
            with three independent roles: stop (the arrows and the
            counter stop here), listed (a row of the popup and the
            Markers tab) and in TOC (linked to a TOC entry).
            auto_marker_on_toc gives TOC headings a marker, with the
            roles of toc_marker_roles.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import MarkerConfig, MarkerRoles

markers = MarkerConfig(
    auto_marker_on_toc=1,                 # level-1 headings get a marker
    toc_marker_roles=MarkerRoles.NAMED,   # ... a stop, listed (the default)
    next_keys=["PageDown"],               # next stop
    prev_keys=["PageUp"],                 # previous stop
)""")
        st_space("v", 1)

        st_write(bs.sub, "The marker registry", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            MarkerRegistry (marker.py) collects one dict per marker,
            in module order, during a render pass. st_marker(), the
            break of st_slide_break() / st_slide() and TOC headings
            (write.py, _bridge_toc_marker) all register through it.
            book.py starts a new slide at each entry
            (marker_slide_boundary), which st_write(marker="attach")
            and the "second navigation stop" warning read.
        """)
        st_space("v", 1)

        show_code("""\
# with st_slide(cut=True, marker="Prompt patterns", key="patterns"):
#     st_write(s.title, "Prompt patterns", toc_lvl="2", marker="attach")
{
    "index": 7,                 # position in the registry (module order)
    "label": "Prompt patterns", # "Marker N" when generated ("auto": True)
    "anchor": "stx-marker-prompt-patterns-7",   # DOM id (a TOC anchor when in TOC)
    "stop": True,               # the arrows, keys and counter stop here
    "listed": True,             # a row of the popup / Markers tab / page titles
    "toc": True,                # linked to a TOC entry ...
    "toc_anchor": "3-1-prompt-patterns", "toc_level": 2,   # ... this one
    "stop_index": 5,            # rank among the stops (None for a non-stop)
    "origin": "break",          # "marker", "break" or "toc"
    "key": "patterns",          # optional, from key= (deep links)
    "hidden": False,            # derived: stop and not listed (older tools)
    # added by annotate_marker_numbers():
    "number": 6,                # the slide number every surface shows
    "row_end": 9, "row_text": "6–9",   # listed entries only: their row
    # added in paginated mode, from the page cache:
    "page_idx": 3,              # 0-based page of the marker
}""")
        st_space("v", 1)

        show_details("""\
            Readers never test the fields directly: is_stop(),
            is_listed(), stop_entries(), stop_count(),
            listed_entries() and stop_of() (marker.py) give the
            roles, with defaults for entries of an older page cache
            (normalize_marker_entries fills stop / listed from hidden).
            annotate_marker_numbers() writes number, row_end and
            row_text once in Python; the live widget, the HTML export
            bar, the sidebar Markers tab and the footer read them.

            Paginated mode: the page cache holds every marker of the
            book with its page_idx. On each run, the registry is reset,
            then the cached entries of the pages before the current
            one are appended (pre-seed, every field copied), the page
            renders and registers its own markers live, and the cached
            entries of the later pages are appended (post-seed). The
            arrows and the numbers therefore cover the whole book while
            only one page is executed.
        """)
        st_space("v", 2)

        # --- 4. BannerConfig ---
        st_write(bs.sub, "BannerConfig: pagination banner", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            BannerConfig controls the pagination banner that
            appears at the top and/or bottom of pages. It can
            be FULL (prev/next with title), COMPACT (arrows only),
            or HIDDEN.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import BannerConfig, BannerMode

banner = BannerConfig(
    mode=BannerMode.FULL,  # BannerMode.FULL, .COMPACT, .HIDDEN
)
banner = BannerConfig.full()   # the same, with the default colour""")
        st_space("v", 2)

        # --- 5. Paginated vs continuous ---
        st_write(bs.sub, "Paginated vs continuous mode", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_book supports two rendering modes. In continuous mode
            (the default), all blocks render on a single scrollable
            page. In paginated mode, the book is cut into pages with
            navigation: one page per book entry by default, or pages
            that follow the composition tree with paginate_by (down to
            a depth, or one page per leaf). Only the current page is
            executed; a page cache built once gives the TOC and the
            markers of the other pages.
        """)
        st_space("v", 1)

        show_code("""\
# Continuous mode (default): all blocks on one page
st_book(blocks)                      # = st_book(blocks, paginate=False)

# Paginated mode: one page per book entry
st_book(blocks, paginate=True)       # paginate_by="entry" (default)

# Pages that follow the composition tree
st_book(blocks, paginate=True, paginate_by=2)       # down to depth 2
st_book(blocks, paginate=True, paginate_by="leaf")  # one page per leaf""")
        st_space("v", 2)

        # --- 6. Bibliography ---
        st_write(bs.sub, "Bibliography setup", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_book can load and register bibliography sources
            (.bib files) for citation support. Once registered,
            blocks can cite references using st_cite() (from
            streamtex.bib).
        """)
        st_space("v", 1)

        show_code("""\
st_book(
    blocks,
    bib_sources=["references.bib"],  # BibTeX file(s)
)

# In a block:
# from streamtex.bib import st_cite
# st_cite("author2024")  -> renders the citation (format set by BibConfig)""")
        st_space("v", 2)

        # --- 7. Inspector integration ---
        st_write(bs.sub, "Inspector integration", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The inspector is an optional live code editor panel
            that lets developers inspect and modify block code
            at runtime.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import InspectorConfig

st_book(
    blocks,
    inspector=InspectorConfig(enabled=True),   # enable live code inspector
)""")
        st_space("v", 2)

        # --- 8. Full book.py example ---
        st_write(bs.sub, "Complete book.py example", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig
from blocks import bck_intro, bck_setup, bck_architecture

toc = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=3, search=True)
markers = MarkerConfig(auto_marker_on_toc=1, next_keys=["PageDown"], prev_keys=["PageUp"])
banner = BannerConfig.full()

st_book(
    [bck_intro, bck_setup, bck_architecture],
    toc_config=toc,
    marker_config=markers,
    banner=banner,
    paginate=True,
    bib_sources=["references.bib"],
)""")
        st_space("v", 2)

        show_details("""\
            st_book() handles all the plumbing: page state,
            sidebar TOC, pagination, keyboard shortcuts, and export.

            Each block module only needs a build() function.
            The orchestrator calls build() at the right time.

            Inspector mode is for development only.
            Disable it in production deployments.
        """)
