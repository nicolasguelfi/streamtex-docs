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
    banner_config=banner,
)""")
        st_space("v", 2)

        # --- 2. TOCConfig ---
        st_write(bs.sub, "TOCConfig: table of contents", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            TOCConfig controls the sidebar table of contents:
            numbering mode (decimal, roman, none), maximum
            sidebar depth, and search functionality.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import TOCConfig

toc = TOCConfig(
    numbering="decimal",   # "decimal", "roman", "none"
    sidebar_depth=3,       # max depth shown in sidebar
    search=True,           # enable TOC search
)""")
        st_space("v", 2)

        # --- 3. MarkerConfig ---
        st_write(bs.sub, "MarkerConfig: navigation markers", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            MarkerConfig manages auto-markers generated from the
            TOC and keyboard navigation. Markers are anchor points
            that enable quick jumps between sections.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import MarkerConfig

markers = MarkerConfig(
    auto_markers=True,     # generate markers from TOC entries
    keyboard_nav=True,     # enable arrow-key navigation
)""")
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
from streamtex import BannerConfig

banner = BannerConfig(
    mode="FULL",           # "FULL", "COMPACT", "HIDDEN"
)""")
        st_space("v", 2)

        # --- 5. Paginated vs continuous ---
        st_write(bs.sub, "Paginated vs continuous mode", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_book supports two rendering modes. In paginated
            mode, each block is a separate page with navigation.
            In continuous mode, all blocks render on a single
            scrollable page.
        """)
        st_space("v", 1)

        show_code("""\
# Paginated mode (default): one block per page
st_book(blocks, paginate=True)

# Continuous mode: all blocks on one page
st_book(blocks, paginate=False)""")
        st_space("v", 2)

        # --- 6. Bibliography ---
        st_write(bs.sub, "Bibliography setup", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_book can load and register bibliography sources
            (.bib files) for citation support. Once registered,
            blocks can cite references using st_cite() and a
            bibliography section is generated automatically.
        """)
        st_space("v", 1)

        show_code("""\
st_book(
    blocks,
    bib_sources=["references.bib"],  # BibTeX file(s)
)

# In a block:
# st_cite("author2024")  -> renders [Author, 2024]""")
        st_space("v", 2)

        # --- 7. Inspector integration ---
        st_write(bs.sub, "Inspector and link preview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The inspector is an optional live code editor panel
            that lets developers inspect and modify block code
            at runtime. Link preview injects JS/CSS for hover
            cards on cross-references and external links.
        """)
        st_space("v", 1)

        show_code("""\
st_book(
    blocks,
    inspector=True,        # enable live code inspector
    link_preview=True,     # enable hover cards on links
)""")
        st_space("v", 2)

        # --- 8. Full book.py example ---
        st_write(bs.sub, "Complete book.py example", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
from streamtex import st_book, TOCConfig, MarkerConfig, BannerConfig
from blocks import bck_intro, bck_setup, bck_architecture

toc = TOCConfig(numbering="decimal", sidebar_depth=3, search=True)
markers = MarkerConfig(auto_markers=True, keyboard_nav=True)
banner = BannerConfig(mode="FULL")

st_book(
    [bck_intro, bck_setup, bck_architecture],
    toc_config=toc,
    marker_config=markers,
    banner_config=banner,
    paginate=True,
    inspector=False,
    link_preview=True,
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
