"""PDF Export — PdfMode, PdfConfig, and export_pdf() reference."""

import streamtex as stx
from streamtex import (
    st_write, st_space, st_block, st_list, st_grid, st_image,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """PDF Export block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    minor = s.project.titles.subsection_title
    param_label = s.medium + s.text.weights.bold_weight
    caption = s.medium + s.italic + s.project.colors.neutral_gray


bs = BlockStyles


def build():
    """PDF Export — PdfMode, PdfConfig, and export_pdf()."""

    st_write(bs.heading, "PDF Export", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX can export your book to PDF using Playwright and
        headless Chromium. The export system supports two modes:
        continuous (single flowing document) and paginated (one PDF
        page per slide break).

        Requires the optional pdf extra: uv add "streamtex[pdf]"
        and playwright install chromium. The app checks once per process
        whether Chromium is installed (0.7.43): after installing it,
        restart the app to see the PDF option in the export panel.
    """)
    st_space("v", 3)

    # --- Section 1: PdfMode ---
    st_write(bs.sub, "1. PdfMode", toc_lvl="+1")
    st_space("v", 2)

    show_explanation("""\
        PdfMode is an enum that controls how slide breaks are
        handled in the exported PDF.

        - **CONTINUOUS** \u2014 Removes all slide breaks. Content flows
        as a single continuous document.

        - **PAGINATED** \u2014 Inserts a PDF page break at each slide
        break and visible marker. Each section starts on a new page.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import PdfMode

# Continuous mode — single flowing document
mode = PdfMode.CONTINUOUS

# Paginated mode — page break at each slide break
mode = PdfMode.PAGINATED""")
    st_space("v", 3)

    # --- Section 2: PdfConfig ---
    st_write(bs.sub, "2. PdfConfig", toc_lvl="+1")
    st_space("v", 2)

    show_explanation("""\
        PdfConfig is a dataclass that controls all aspects of PDF
        generation: page size, orientation, margins, zoom and print
        scale, content width, headers, footers, page numbers, and how
        long the media may take to load.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import PdfConfig, PdfMode

config = PdfConfig(
    mode=PdfMode.PAGINATED,
    format="A4",           # A4, Letter, A3, Legal, Tabloid
    landscape=True,        # landscape orientation
    margin_top="10mm",     # CSS margin values
    margin_bottom="10mm",
    margin_left="15mm",
    margin_right="15mm",
    print_background=True, # include background colors
    zoom=100,              # zoom of everything, vw/vh included (10 - 400 %)
    scale=1.0,             # Chromium print scale (0.1 - 2.0): pt/px only
    content_width=100,     # content width in % of the page (10 - 100)
    page_numbers=True,     # add page numbers in footer
    load_timeout_ms=300_000,  # media loading limit before printing (0 = none)
)""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "mode"), " \u2014 PdfMode.CONTINUOUS or PdfMode.PAGINATED")
            with l.item(): st_write(s.medium, (bs.param_label, "format"), " \u2014 page format string (A4, Letter, etc.)")
            with l.item(): st_write(s.medium, (bs.param_label, "landscape"), " \u2014 landscape orientation (default True)")
            with l.item(): st_write(s.medium, (bs.param_label, "zoom"), " \u2014 zoom of the whole document in % (10\u2013400, default 100, 0.7.45): a CSS zoom on body, so px, pt, vw and vh all shrink or grow; it multiplies with the view zoom the HTML already carries")
            with l.item(): st_write(s.medium, (bs.param_label, "scale"), " \u2014 Chromium's print scale from 0.1 to 2.0 (default 1.0), like \u201cScale\u201d in Chrome's print dialog: shrinks pt/px and lets the text reflow, but vw/vh stay proportional to the page")
            with l.item(): st_write(s.medium, (bs.param_label, "content_width"), " \u2014 content width in % of the page (10\u2013100, default 100); the side padding is left and right only, the background stays full-bleed")
            with l.item(): st_write(s.medium, (bs.param_label, "load_timeout_ms"), " \u2014 how long Chromium may load the document and its media before printing (default 300 000 ms, 0 = no limit, 0.7.44); past it the PDF is printed without the media still loading")
            with l.item(): st_write(s.medium, (bs.param_label, "page_numbers"), " \u2014 add centered page numbers in footer")
            with l.item(): st_write(s.medium, (bs.param_label, "header_template / footer_template"), " \u2014 custom Chromium print header/footer HTML")
    st_space("v", 3)

    # Live defaults, read from the library
    _defaults = stx.PdfConfig()
    with st_block(s.project.containers.explanation_box):
        st_write(s.medium, (bs.param_label, "Live \u2014 PdfConfig() defaults: "),
                 f"zoom={_defaults.zoom}, scale={_defaults.scale}, "
                 f"content_width={_defaults.content_width}, "
                 f"load_timeout_ms={_defaults.load_timeout_ms}")
    st_space("v", 2)

    # --- Zoom or scale? ---
    st_write(bs.minor, "Zoom or scale? Three real PDFs")
    st_space("v", 1)

    show_explanation("""\
        To shrink a document uniformly, use zoom, not scale. Chromium
        resolves vw and vh against the printed page: scale shrinks what is
        sized in pt/px, while a frame of 60vw x 40vh keeps its size on
        the paper. zoom shrinks everything alike. Below, one page whose
        title is in min(4vw, 42pt), whose body text is in 20px and whose
        frame is 60vw x 40vh, printed three times on a 16:9 page, then
        rasterized at 72 dpi (pdftoppm): the frame measures 524 px, 525 px
        with scale=0.8, and 419 px (80 %) with zoom=80.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import export_pdf, PdfConfig, PdfMode

base = dict(mode=PdfMode.CONTINUOUS, format="16:9")
export_pdf(html, output_path="reference.pdf", config=PdfConfig(**base))
export_pdf(html, output_path="scale.pdf", config=PdfConfig(**base, scale=0.8))
export_pdf(html, output_path="zoom.pdf", config=PdfConfig(**base, zoom=80))""")
    st_space("v", 1)

    with st_grid(cols="repeat(auto-fit, minmax(300px, 1fr))", gap="16px") as g:
        for _name, _label in [
            ("reference", "Reference (zoom=100, scale=1.0)"),
            ("scale", "scale=0.8: the 20px text shrinks, the vw title and the 60vw x 40vh frame do not"),
            ("zoom", "zoom=80: everything is 80 %, the frame included"),
        ]:
            with g.cell():
                st_image(uri=f"export/pdf_zoom_comparison_{_name}.png", width="100%",
                         alt=f"First page of the PDF exported with {_label}")
                st_write(bs.caption, _label)
    st_space("v", 2)

    # --- Zoom in the export panel ---
    st_write(bs.minor, "Zoom in the \u201cDownload as...\u201d panel")
    st_space("v", 1)

    show_explanation("""\
        The PDF layout of the panel has a "Zoom (%)" field next to
        "Scale (%)" (0.7.45). The PDF zoom multiplies with the view zoom
        the exported HTML carries (sidebar Zoom %): view 80 % × PDF 70 %
        = 56 %. After generation, the panel shows the resulting zoom
        next to the PDF download ("PDF zoom: view 80% × 70% = 56%").

        "Full document" follows the current view: the full-book HTML is
        built once per session, and the export now gives it the zoom and
        page width of the moment, so a change of the view (sidebar,
        presentation profile) reaches the export without a rebuild. The
        caption of the PDF layout says what reaches the PDF: the view
        zoom, times the PDF zoom; the view width reaches only the HTML
        (the PDF uses "Content width").

        The HTML has its own "Zoom HTML (%)" field: 0 (the default)
        keeps the view zoom, a value replaces it for the HTML file only.
        Its starting value comes from st_book(html_export_zoom=...) or
        `html_export_zoom` in `[book.defaults]`.
    """)
    st_space("v", 2)

    # --- Load timeout and PdfLoadReport ---
    st_write(bs.minor, "Large documents: load_timeout_ms and PdfLoadReport")
    st_space("v", 1)

    show_explanation("""\
        Before printing, Chromium loads every medium of the document. A
        large document whose media come from the running Streamlit server
        can need minutes; load_timeout_ms bounds that wait (0.7.44). When
        it runs out, the PDF is printed anyway without the media still
        loading, and the panel says how many loaded, which are pending,
        and which setting to raise. In code, pass a PdfLoadReport
        (stx.PdfLoadReport) to export_pdf() to read the same facts.
    """)
    st_space("v", 1)

    show_code("""\
import streamtex as stx

report = stx.PdfLoadReport()
cfg = stx.PdfConfig(load_timeout_ms=600_000)   # 10 min; 0 = no limit
pdf_bytes = stx.export_pdf(html, config=cfg, report=report)

print(report.elapsed_s, report.finished, report.pending)
if report.timed_out:                           # the PDF lacks report.pending
    print(report.message(cfg.load_timeout_ms))""")
    st_space("v", 3)

    # --- Section 3: Usage in st_book() ---
    st_write(bs.sub, "3. Usage in st_book()", toc_lvl="+1")
    st_space("v", 2)

    show_explanation("""\
        Pass PdfConfig to st_book() via the pdf_config= parameter.
        StreamTeX automatically provides a PDF download button in
        the sidebar when export is enabled.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import st_book, PdfConfig, PdfMode

st_book(
    [bck_intro, bck_chapter_1, bck_chapter_2],
    pdf_config=PdfConfig(
        mode=PdfMode.PAGINATED,
        format="A4",
        landscape=True,
        margin_top="0",
        margin_bottom="0",
        margin_left="0",
        margin_right="0",
        page_numbers=True,
    ),
)""")
    st_space("v", 3)

    # --- Section 4: export_pdf() ---
    st_write(bs.sub, "4. export_pdf() \u2014 Programmatic Export", toc_lvl="+1")
    st_space("v", 2)

    show_explanation("""\
        export_pdf() converts an HTML document to PDF using Playwright.
        Use it for programmatic export outside of st_book(), for example
        in scripts or CI pipelines.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import export_pdf, PdfConfig, PdfMode
from streamtex.export import generate_export_html

# Get the HTML from the export buffer
html = generate_export_html()

# Export to PDF bytes
pdf_bytes = export_pdf(html, config=PdfConfig(
    mode=PdfMode.PAGINATED,
    format="A4",
))

# Or export directly to a file, everything shrunk to 80 %
export_pdf(html, output_path="output.pdf", config=PdfConfig(
    mode=PdfMode.CONTINUOUS,
    zoom=80,
))""")
    st_space("v", 2)

    show_details("""\
        export_pdf() requires the playwright package and Chromium browser.
        Install with: uv add "streamtex[pdf]" then playwright install chromium.
        The export panel reads Chromium's presence once per process:
        restart the app after installing it.

        The function launches headless Chromium, renders the HTML, and
        produces the PDF. It returns the PDF content as bytes and optionally
        writes to the specified output_path.

        Theme colors (theme_bg, theme_text) on PdfConfig control the
        background and text color of page numbers. st_book() sets these
        automatically from the current Streamlit theme.
    """)
    st_space("v", 3)

    # --- Section 5: Auto-export with exports=[] ---
    st_write(bs.sub, "5. Auto-Export to Disk", toc_lvl="+1")
    st_space("v", 2)

    show_explanation("""\
        Instead of using the sidebar panel, you can configure automatic
        export directly in book.py. Pass a list of ExportConfig to
        st_book(exports=[...]). Each config describes one output file.

        Three modes are available:
        - **ALWAYS** \u2014 auto-export after every render (files written to disk)
        - **MANUAL** \u2014 show in sidebar panel (user clicks Generate)
        - **NEVER** \u2014 disable export entirely

        You can mix modes: some configs auto-export, others show in sidebar.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import st_book, ExportConfig, ExportMode, PdfConfig

st_book([...],
    exports=[
        # HTML with timestamp: my-course-260318-155306.html
        ExportConfig(
            format="html",
            mode=ExportMode.ALWAYS,
            output_dir="./exports",
            filename="my-course",
            timestamp=True,
        ),
        # PDF for printing (A4 portrait)
        ExportConfig(
            format="pdf",
            mode=ExportMode.ALWAYS,
            output_dir="./exports",
            filename="my-course-print",
            timestamp=True,
            pdf=PdfConfig(format="A4", landscape=False),
        ),
        # PDF for projection (A4 landscape, no margins)
        ExportConfig(
            format="pdf",
            mode=ExportMode.ALWAYS,
            output_dir="./exports",
            filename="my-course-slides",
            timestamp=False,
            pdf=PdfConfig(
                format="A4", landscape=True,
                margin_top="0", margin_bottom="0",
                margin_left="0", margin_right="0",
            ),
        ),
    ],
)""")
    st_space("v", 1)

    show_details("""\
        When exports is provided, st_book() decides automatically
        whether to show the sidebar panel: it only appears if at least
        one config has mode=MANUAL.

        Files are written to output_dir/ after each render. The sidebar
        shows a caption listing the exported files.

        Backward compatibility: if exports is not provided, the existing
        export=True / pdf_config= behaviour is unchanged.
    """)
    st_space("v", 1)
