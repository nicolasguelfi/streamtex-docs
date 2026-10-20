"""Advanced Export — ExportConfig, HtmlExportBuffer, st_html() and the paginated HTML export."""

import streamtex as stx
from streamtex import *
from streamtex.book import HTML_EXPORT_MODES
from streamtex.printing import resolve_printable
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Styles for Advanced Export block."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight
    warning_box = ns("background:rgba(255,100,100,0.1);padding:16px;border-radius:8px;", "warning_box")
    tip_box = ns("background:rgba(100,200,100,0.1);padding:16px;border-radius:8px;", "tip_box")
    caption = s.medium + s.italic + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """Demonstrate advanced export features: ExportConfig, buffer, and st_html()."""

    st_write(bs.heading, "Advanced Export \u2014 ExportConfig & st_html", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX's HTML export system converts your live Streamlit app
        into static HTML: one continuous file by default, or one file per
        page with `stx export html --html-mode paginated | both` (see
        "Paginated HTML export" below). This section covers the internal
        machinery: ExportConfig, the HtmlExportBuffer, the push/pop
        wrapper pattern, the st_html() dual-render bridge, and the
        paginated export.
    """)
    st_space("v", 2)

    # --- Section 1: ExportConfig ---
    st_write(bs.sub, "ExportConfig", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        ExportConfig is a dataclass that describes an exported document.
        st_book() builds the buffer's config itself from export= and
        export_title=; you pass ExportConfig objects to st_book(exports=[...])
        to describe the files written to disk (format, mode, output_dir,
        filename, asset_mode...).
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import ExportConfig, ExportMode

        # The buffer: st_book() fills enabled / page_title from these two
        st_book(blocks, export=True, export_title="My Export")

        # Files on disk: one ExportConfig per output file
        st_book(blocks, exports=[
            ExportConfig(format="html", mode=ExportMode.ALWAYS,
                         output_dir="./exports", filename="my-export"),
        ])""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "enabled"), " \u2014 toggle export on or off (default False; st_book sets it from export=)")
            with l.item(): st_write(s.medium, (bs.param_label, "page_title"), " \u2014 the HTML page title in the exported file (st_book sets it from export_title=)")
            with l.item(): st_write(s.medium, (bs.param_label, "page_width"), " \u2014 CSS max-width for the page container (default 90%)")
            with l.item(): st_write(s.medium, (bs.param_label, "page_padding"), " \u2014 CSS padding around the main content area")
    st_space("v", 2)

    # --- Section 2: HtmlExportBuffer ---
    st_write(bs.sub, "How the Export Buffer Works", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        When export is enabled, StreamTeX maintains an HtmlExportBuffer
        that accumulates HTML fragments as each block renders. Every
        st_write(), st_code(), st_block(), and other stx functions append
        their HTML representation into this buffer.

        At the end of the render cycle, generate_full_html() assembles
        all accumulated fragments into one complete HTML document, CSS
        inlined. That document is the continuous export; a paginated
        export cuts the same document into one file per page (see
        "Paginated HTML export" below).
    """)
    st_space("v", 1)

    show_code("""\
        # Simplified internal flow:
        #
        # 1. st_book() calls reset() on the buffer
        # 2. Each block's build() runs:
        #    - st_write() appends <div>...</div> to buffer
        #    - st_code() appends <pre><code>...</code></pre> to buffer
        #    - st_block() pushes/pops wrapper divs
        # 3. After all blocks: generate_full_html() produces the file""")
    st_space("v", 2)

    # --- Section 3: Push/Pop Pattern ---
    st_write(bs.sub, "The Push/Pop Wrapper Pattern", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Nested containers (st_block, st_grid, st_span) use a push/pop
        pattern to maintain proper HTML nesting in the export buffer.
        When entering a container, an opening tag is pushed. When
        exiting, the closing tag is popped.
    """)
    st_space("v", 1)

    show_code("""\
        # Internal mechanism (you don't call this directly):
        export_push_wrapper('<div style="display:flex; gap:16px;">')
        # ... content rendered inside appends to the buffer ...
        export_pop_wrapper('</div>')

        # This happens automatically when you use context managers:
        with st_block(my_style):
            st_write(s.medium, "Content inside the block")
            # push on __enter__, pop on __exit__""")
    st_space("v", 2)

    # --- Section 4: st_html() ---
    st_write(bs.sub, "st_html() \u2014 The Dual-Render Bridge", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        st_html() is the low-level function for injecting raw HTML into
        both the live Streamlit app and the export buffer. It supports
        two rendering modes based on the height parameter.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import st_html

        # Inline mode (height=0): renders via st.html()
        st_html(html_string, height=0)

        # Iframe mode (height>0): renders via components.html()
        st_html(html_string, height=400, light_bg=True, scrolling=True)""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item():
                st_write(
                    s.medium,
                    (bs.param_label, "height=0"),
                    " \u2014 inline rendering via st.html() (no iframe, content flows with page)",
                )
            with l.item():
                st_write(
                    s.medium,
                    (bs.param_label, "height>0"),
                    " \u2014 iframe rendering via components.html() (isolated, fixed height in px)",
                )
            with l.item():
                st_write(
                    s.medium,
                    (bs.param_label, "light_bg"),
                    " \u2014 injects color-scheme: light for white backgrounds inside the iframe",
                )
            with l.item():
                st_write(
                    s.medium,
                    (bs.param_label, "scrolling"),
                    " \u2014 enables scrollbar in iframe mode (default False)",
                )
    st_space("v", 2)

    # --- Section 5: Export-Aware Widgets ---
    st_write(bs.sub, "Export-Aware Widgets Reminder", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.warning_box):
        st_write(
            s.large,
            (s.text.weights.bold_weight, "Important:"),
            " native st.* widgets (st.dataframe, st.line_chart, etc.) "
            "are invisible in exported HTML. Always use their stx.st_* "
            "equivalents when export is enabled.",
        )
    st_space("v", 1)

    show_code("""\
        # WRONG - disappears in export
        st.dataframe(df)

        # CORRECT - visible in both live app and exported HTML
        stx.st_dataframe(df)""")
    st_space("v", 1)

    with st_block(bs.tip_box):
        st_write(
            s.medium,
            "See the ",
            (s.text.weights.bold_weight, "Export-Aware Widgets"),
            " section for the full list of available stx.st_* wrappers.",
        )
    st_space("v", 2)

    # --- Section 6: Full Export Lifecycle ---
    st_write(bs.sub, "Full Export Lifecycle", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(s.medium, "The complete export cycle follows these steps:")
        with st_list(list_type="ol") as l:
            with l.item(): st_write(s.medium, "st_book() detects export is enabled and calls buffer.reset()")
            with l.item(): st_write(s.medium, "The book renders all blocks in order (paginated or continuous)")
            with l.item(): st_write(s.medium, "Each stx function appends its HTML fragment to the buffer")
            with l.item(): st_write(s.medium, "Nested containers use push/pop to maintain proper HTML structure")
            with l.item(): st_write(s.medium, "After all blocks render, generate_full_html() assembles the output")
            with l.item(): st_write(s.medium, "CSS from default.css is inlined into the HTML document")
            with l.item(): st_write(s.medium, "The download button offers it: a ZIP (HTML + data/) with the default EXTERNAL assets, an .html file with EMBEDDED ones")
    st_space("v", 2)

    # --- Section 7: CSS Bundling ---
    st_write(bs.sub, "CSS Bundling", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Every exported HTML file carries its own styles: StreamTeX reads
        the library's default.css and inlines it as a <style> block, so
        the styles render offline. The media follow asset_mode: EXTERNAL
        (the default) writes them to a data/ folder next to the HTML,
        EMBEDDED inlines them as base64. Only the continuous export with
        EMBEDDED assets is a single self-contained file; a paginated
        export is a set of files that share one data/ folder.
    """)
    st_space("v", 1)

    show_code("""\
        # Simplified generate_full_html() output structure:
        #
        # <!DOCTYPE html>
        # <html>
        # <head>
        #   <title>{page_title}</title>
        #   <style>
        #     /* contents of default.css inlined here */
        #     .streamtex-page { max-width: {page_width}; padding: {page_padding}; }
        #   </style>
        # </head>
        # <body>
        #   <div class="streamtex-page">
        #     {accumulated_html_fragments}
        #   </div>
        # </body>
        # </html>""")
    st_space("v", 2)

    show_details("""\
        - **ExportConfig** is a Python dataclass. All fields have sensible defaults.
        st_book() sets enabled and page_title from export= and export_title=.

        - **HtmlExportBuffer** is a singleton managed by StreamTeX internally.
        You never instantiate it directly. It is reset at the start of each
        st_book() render cycle.

        - **push/pop wrappers** are called automatically by context managers
        (st_block, st_grid, st_span). You only need to use export_push_wrapper
        and export_pop_wrapper if you are building custom container components.

        - **st_html()** is the low-level bridge. Most users never call it directly.
        Higher-level functions (st_latex_doc, st_mermaid, st_tikz) use **st_html()**
        internally for iframe-based rendering.

        - **CSS inlining** ensures the exported file works offline. If you add
        custom CSS files, they must be registered with StreamTeX to be included
        in the export bundle.

        - **Performance note:** The export buffer accumulates all HTML in memory.
        For very large books (hundreds of blocks), memory usage may be significant
        during the export phase.
    """)
    st_space("v", 3)

    # --- Section 8: Paginated HTML export ---
    st_write(bs.sub, "Paginated HTML Export", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        `stx export html` writes a module in one of three modes. The mode
        is a module setting, `st_book(html_export_mode=...)` or the
        `html_export_mode` key of `[book.defaults]` in `stx.toml`, and the
        `--html-mode` option of the command wins over it. The pages are
        those of the page map: `st_book(paginate_by=...)` decides where the
        document is cut (one page per book entry by default).
    """)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(s.medium, (bs.param_label, "Accepted values (read live from streamtex.book.HTML_EXPORT_MODES): "),
                 ", ".join(HTML_EXPORT_MODES))
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "continuous"), " — one file, <name>.html (the default)")
            with l.item(): st_write(s.medium, (bs.param_label, "paginated"), " — one file per page in pages/; <name>.html becomes an entry file that sends every link to its page")
            with l.item(): st_write(s.medium, (bs.param_label, "both"), " — the continuous file and pages/, with a “Continuous view / Paginated view” button in the navigation bar of every file")
    st_space("v", 1)

    show_code("""\
        # book.py of the example module my_deck/: four blocks, one TOC entry
        # each, and a second slide inside bck_intro (st_slide(cut=True, marker=...))
        st_book(
            [blocks.bck_title, blocks.bck_intro, blocks.bck_details, blocks.bck_summary],
            toc_config=TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=2, search=True),
            marker_config=MarkerConfig(auto_marker_on_toc=1),
            paginate=True,
            html_export_mode="both",
        )""")
    st_space("v", 1)

    show_code("""\
        # stx.toml: the same settings for every book of the project
        [book.defaults]
        html_export_mode = "both"   # continuous | paginated | both
        paginate_by = "entry"       # one page per entry (or N, "depth:N", "leaf")""",
              language="toml", line_numbers=False)
    st_space("v", 1)

    show_code("""\
        stx export html --html-mode continuous my_deck
        stx export html --html-mode paginated my_deck
        stx export html --html-mode both my_deck""", language="bash", line_numbers=False)
    st_space("v", 2)

    st_write(bs.param_label, "What these three commands wrote (output ./static-html, external assets, both defaults)")
    st_space("v", 1)

    show_code("""\
        # --html-mode continuous
        static-html/my_deck/
          my_deck.html                  # the whole module
          data/images/b83deb264d99.png  # the sidebar logo

        # --html-mode paginated
        static-html/my_deck/
          my_deck.html                  # the entry file
          data/images/b83deb264d99.png
          pages/
            bck_details.html
            bck_intro.html              # both of its slides
            bck_summary.html
            bck_title.html

        # --html-mode both
        static-html/my_deck/
          my_deck.html                  # continuous, "Paginated view"
          data/images/b83deb264d99.png
          pages/
            bck_details.html            # each: "Continuous view"
            bck_intro.html
            bck_summary.html
            bck_title.html""", language="text", line_numbers=False, wrap=False)
    st_space("v", 1)

    show_explanation("""\
        File names carry no number: a page file is named after its block.
        When the same block makes several pages, each copy is qualified by
        its section (the list block that includes it, or the level-1
        heading before it), e.g.
        `exercice-1-la-question-directe--bck_title_bravo.html`.
        With `--asset-mode embedded` the files go straight into the output
        folder: `my_deck.html` and `my_deck-pages/`, media inlined.
    """)
    st_space("v", 2)

    st_write(bs.param_label, "Deep links through the entry file (opened in Chromium on the export above)")
    st_space("v", 1)

    show_code("""\
        my_deck.html?slide=3                 -> pages/bck_intro.html#stx-marker-second-slide-2
        my_deck.html?marker=Second%20slide   -> pages/bck_intro.html#stx-marker-second-slide-2
        my_deck.html?page=4                  -> pages/bck_summary.html
        my_deck.html#summary                 -> pages/bck_summary.html#4-summary
        my_deck.html                         -> pages/bck_title.html""",
              language="text", line_numbers=False, wrap=False)
    st_space("v", 1)

    show_explanation("""\
        The entry file keeps the address of the continuous export, so the
        links written for it keep working. Precedence: `marker` > `slide` >
        `page`; `?slide=n` opens the slide the counter calls n. Inside a
        page file the arrows walk the stops across files, one press per
        slide: from the second slide of `bck_intro.html`, the next press
        opens `bck_details.html`. In `both` mode the view button opens the
        same slide in the other view.
    """)
    st_space("v", 2)

    with st_grid(cols="repeat(auto-fit, minmax(600px, 1fr))", gap="24px") as g:
        with g.cell():
            st_image(uri="export/paginated_export_page_nav_bar.png", width="100%",
                     alt="Page file bck_intro.html of a paginated export, with its navigation bar")
            st_write(bs.caption, "pages/bck_intro.html (--html-mode both): the whole table of "
                     "contents with this page's entry marked; the bar shows 2 / 5 and the "
                     "“Continuous view” button")
        with g.cell():
            st_image(uri="export/paginated_export_continuous_view.png", width="100%",
                     alt="Continuous file my_deck.html of the same export")
            st_write(bs.caption, "my_deck.html (--html-mode both): the continuous file, "
                     "with the “Paginated view” button")
    st_space("v", 1)

    show_details("""\
        - Each page file holds only its page and requests only its own
        images, but carries the whole module's table of contents (a link to
        another page opens that file at the heading) and the global search
        index.

        - No rule is drawn at the head of a page file, as in the paginated app.

        - Only `stx export html` writes page files; the "Download as..."
        panel of the running app downloads the continuous document.

        - The developer manual (Export architecture) explains how the
        document is cut: page sentinels written during the page-cache
        build, then `streamtex/export_paginate.py`.
    """)
    st_space("v", 3)

    # --- Section 9: Run-time switches (0.7.39) ---
    st_write(bs.sub, "Run-time Switches \u2014 is_editable(), is_exportable(), env_flag()", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A deployed document is often read-only while the author's copy
        shows the export panel and the image editors. Two switches give
        one reading of that choice: is_exportable() reads STX_EXPORTABLE,
        is_editable() reads STX_EDITABLE (the legacy names IS_EXPORTABLE /
        IS_EDITABLE are accepted). Each is read from the environment, then
        from an optional .env file (env_file=), and defaults to False.
        Nothing in the library reads them implicitly: the book passes them
        where it wants them.
    """)
    st_space("v", 1)

    show_code("""\
        import streamtex as stx

        # book.py — the export panel only where STX_EXPORTABLE=1
        st_book([...], export=stx.is_exportable(), paginate=True)

        # a block — the image editor only where STX_EDITABLE=1
        st_image(uri="diagram.png", name="diagram",
                 editable=stx.is_editable(), alt="Architecture")

        # the same switches read from a .env file when not in the environment
        stx.is_editable(env_file=".env")

        # any other boolean switch, with an optional legacy name
        show_drafts = stx.env_flag("MY_SHOW_DRAFTS", default=False,
                                   legacy="SHOW_DRAFTS", env_file=".env")""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        st_write(s.medium, (bs.param_label, "Live \u2014 "),
                 "stx.is_exportable() = ", str(stx.is_exportable()),
                 ", stx.is_editable() = ", str(stx.is_editable()))
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "True"), " \u2014 1, true, yes, on (any case)")
            with l.item(): st_write(s.medium, (bs.param_label, "False"), " \u2014 0, false, no, off, empty")
            with l.item(): st_write(s.medium, (bs.param_label, "Anything else"), " \u2014 ValueError: a typo in a deployment variable is an error, not a silent default")
            with l.item(): st_write(s.medium, (bs.param_label, "Order"), " \u2014 the environment first (new name, then legacy), then env_file, then default")
    st_space("v", 3)

    # --- Section 10: Usage notice and print rules (0.7.55) ---
    st_write(bs.sub, "Usage Notice and Print Rules", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A module can state how it may be used and what a reader may print
        or download: `st_book(notice=..., printable=...)`. Each module has
        its own book.py, so the slides of a course can refuse printing
        while the participants' sheet of the same course allows it. The
        settings reach the live app and every HTML export of the module
        (`stx export html`, the "Download as..." panel, automatic exports).
    """)
    st_space("v", 1)

    show_code("""\
        # slides: readable everywhere, printable nowhere
        st_book(blocks,
                notice={"en": "For enrolled participants only",
                        "fr": "Réservé aux participants inscrits"},
                printable=False)

        # participants' sheet: printable as HTML, no PDF from the app
        st_book(blocks,
                notice="For enrolled participants only",
                printable=stx.PrintConfig(app_print=False, app_pdf=False,
                                          html_print=True))""")
    st_space("v", 1)

    _off = resolve_printable(False)
    with st_block(s.project.containers.explanation_box):
        st_write(s.medium, (bs.param_label, "printable=False (read live from streamtex.printing): "),
                 ", ".join(f"{k}={getattr(_off, k)}" for k in ("app_print", "app_pdf", "html_print", "app_html")))
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "app_print"), " \u2014 File \u203a Print on the live app")
            with l.item(): st_write(s.medium, (bs.param_label, "app_pdf"), " \u2014 the PDF box of the app's \u201cDownload as...\u201d panel")
            with l.item(): st_write(s.medium, (bs.param_label, "html_print"), " \u2014 File \u203a Print (and \u201cSave as PDF\u201d) on the exported HTML")
            with l.item(): st_write(s.medium, (bs.param_label, "app_html"), " \u2014 the HTML box of the panel; the panel disappears with nothing left to offer")
    st_space("v", 1)

    show_details("""\
        - The notice is one grey line under the version in the sidebar of
        the app and of the HTML export. When printing is off, the printed
        sheet carries the notice and nothing else.

        - Printing off is a `@media print` rule: no script, nothing changes
        on screen. It states a rule; it cannot stop a screenshot or an
        edited copy of the HTML file.

        - The PDF made by the panel ignores `html_print`. Automatic exports
        (`exports=[ExportConfig(format="pdf", ...)]`) are the author's and
        keep writing their PDF.
    """)
    st_space("v", 3)
