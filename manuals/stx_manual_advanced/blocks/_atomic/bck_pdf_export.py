"""PDF Export — PdfMode, PdfConfig, and export_pdf() reference."""

from streamtex import (
    st_write, st_space, st_block, st_list,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """PDF Export block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight


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
        and playwright install chromium.
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
        generation: page size, orientation, margins, scale, headers,
        footers, and page numbers.
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
    scale=1.0,             # scale factor (0.1 - 2.0)
    page_numbers=True,     # add page numbers in footer
)""")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.medium, (bs.param_label, "mode"), " \u2014 PdfMode.CONTINUOUS or PdfMode.PAGINATED")
            with l.item(): st_write(s.medium, (bs.param_label, "format"), " \u2014 page format string (A4, Letter, etc.)")
            with l.item(): st_write(s.medium, (bs.param_label, "landscape"), " \u2014 landscape orientation (default True)")
            with l.item(): st_write(s.medium, (bs.param_label, "scale"), " \u2014 scale factor from 0.1 to 2.0 (default 1.0)")
            with l.item(): st_write(s.medium, (bs.param_label, "page_numbers"), " \u2014 add centered page numbers in footer")
            with l.item(): st_write(s.medium, (bs.param_label, "header_template / footer_template"), " \u2014 custom Chromium print header/footer HTML")
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

# Or export directly to a file
export_pdf(html, output_path="output.pdf", config=PdfConfig(
    mode=PdfMode.CONTINUOUS,
    scale=0.8,
))""")
    st_space("v", 2)

    show_details("""\
        export_pdf() requires the playwright package and Chromium browser.
        Install with: uv add "streamtex[pdf]" then playwright install chromium.

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
