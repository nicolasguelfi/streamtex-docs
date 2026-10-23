"""Zoom controls and responsive design demonstration."""

from streamtex import *
from streamtex.styles import Style
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code


class BlockStyles:
    """Styles for zoom and responsive demo."""

    heading = s.project.titles.section_title + s.center_txt
    section = s.project.titles.section_subtitle
    info_box = Style("background:rgba(100,150,200,0.1);padding:16px;border-radius:8px;", "info_box")
    code_block = s.project.containers.code_box
    feature_box = Style("background:rgba(100,150,200,0.1);padding:16px;border-radius:8px;", "feature_box")
    badge = Style("display:inline-block;padding:2px 10px;border-radius:10px;"
                  "background:rgba(100,150,200,0.3);font-size:14px;", "zoom_badge")


bs = BlockStyles


def build():
    """Demonstrate zoom controls and responsive design."""

    st_write(bs.heading, "Zoom Controls & Responsive Design", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    # Section 1: Zoom Controls
    st_write(bs.section, "Sidebar Zoom Control", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.info_box):
        st_write(
            s.large,
            (
                s.text.weights.bold_weight,
                "Automatic Feature: ",
            ),
            "StreamTeX automatically adds a zoom control button in the sidebar. "
            "This uses ",
            (s.bold, "CSS zoom property"),
            " (",
            (s.bold, "Baseline 2024"),
            ") for pixel-perfect scaling.",
        )
    st_space("v", 2)

    st_write(
        s.medium,
        "👉 Look at your ",
        (s.text.weights.bold_weight, "Sidebar"),
        " to find the Zoom % field (10 % to 400 %). "
        "Use it to scale the entire page content up/down without reflow.",
    )
    st_space("v", 2)

    # Section 2: How Zoom Works
    st_write(bs.section, "How Zoom Works", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.info_box):
        st_write(
            s.medium,
            (
                s.text.weights.bold_weight,
                "CSS zoom property: ",
            ),
            "Scales the entire element and descendants without changing layout flow. "
            "Perfect for ",
            (s.bold, "presentations"),
            " or ",
            (s.bold, "accessibility"),
            ".",
        )
    st_space("v", 1)

    show_code("""\
# Zoom is automatically injected by st_book()
# No need to manually add it to your blocks

# Users control it via the sidebar "Zoom %" field (10 % - 400 %)
# Starting value: st_book(zoom=100), or zoom in [book.defaults]""", language="python")
    st_space("v", 2)

    # Section 3: Responsive Design Pattern
    st_write(bs.section, "Responsive Design Patterns", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.medium, "Use these patterns for responsive layouts:")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item(): st_write(s.medium, "CSS Grid with 'repeat(auto-fit, ...)' for flexible columns")
        with l.item(): st_write(s.medium, "Relative sizing: '1fr 2fr' instead of fixed pixels")
        with l.item(): st_write(s.medium, "Percentages for widths and paddings")
        with l.item(): st_write(s.medium, "Mobile-first: start small, scale up with zoom")

    st_space("v", 2)

    # Section 4: Demo Responsive Grid
    st_write(bs.section, "Responsive Grid Demo", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.medium, "This 3-column grid adapts to page width. Try zooming:")
    st_space("v", 1)

    show_code("""\
responsive_gap = Style("gap:16px;", "responsive_gap")
with st_grid(
    cols="repeat(auto-fit, minmax(150px, 1fr))",
    grid_style=responsive_gap,
):
    for i in range(1, 7):
        card_style = Style(
            "background:rgba(100,150,200,0.15);padding:12px;"
            "border-radius:6px;text-align:center;", f"card_{i}")
        with st_block(card_style):
            st_write(s.Large + s.bold, str(i))
            st_write(s.medium, f"Card {i}")""", language="python")
    st_space("v", 1)

    # Create responsive grid (auto-fill)
    responsive_gap = Style("gap:16px;", "responsive_gap")
    with st_grid(
        cols="repeat(auto-fit, minmax(150px, 1fr))",
        grid_style=responsive_gap,
    ):
        for i in range(1, 7):
            with st_block(Style("background:rgba(100,150,200,0.15);padding:12px;border-radius:6px;text-align:center;", f"card_{i}")):
                st_write(s.Large + s.text.weights.bold_weight, str(i))
                st_write(s.medium, f"Card {i}")

    st_space("v", 2)

    # Section 5: Best Practices
    st_write(bs.section, "Best Practices", toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type="ol") as l:
        with l.item():
            st_write(
                s.medium,
                "Never fix font sizes in pixels — use relative sizes (12pt, 14pt, etc.)",
            )
        with l.item():
            st_write(
                s.medium,
                "Use grid with 'auto-fit' or 'auto-fill' for adaptive columns",
            )
        with l.item():
            st_write(
                s.medium,
                "Test at zoom levels: 80%, 100%, 120% to ensure readability",
            )
        with l.item():
            st_write(
                s.medium,
                "Zoom is transparent to users — content stays crisp and proportional",
            )

    st_space("v", 3)

    # Section 6: Scoped zoom — nesting and counter-zoom (streamtex-docs#10)
    st_write(bs.section, "Scoped Zoom: Nesting and Counter-Zoom", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.info_box):
        st_write(
            s.medium,
            (s.bold, "st_zoom multiplies. "),
            "with st_zoom(130): zooms its content only. Nested, the factors "
            "multiply: st_zoom(a) inside st_zoom(b) gives a × b, on top of the "
            "page zoom. Zoom scales every length, vw and vh included, and "
            "images or videos given an explicit width; only width-less, fluid "
            "elements keep filling their container.",
        )
    st_space("v", 1)

    st_write(
        s.medium,
        "To keep a widget (badge, tooltip, icon) at a fixed absolute size inside a "
        "zoomed region, wrap it in a counter-zoom: ",
        (s.bold, "st_zoom(10000 / outer_percent)"),
        ". Inside st_zoom(130), st_zoom(10000 / 130) ≈ 76.9 brings it back to 100 %.",
    )
    st_space("v", 1)

    show_code("""\
badge = Style("display:inline-block;padding:2px 10px;border-radius:10px;"
              "background:rgba(100,150,200,0.3);font-size:14px;", "zoom_badge")

with st_zoom(130):
    st_write(s.medium, "Slide text at 130 %")
    with st_zoom(130):
        st_write(s.medium, "Nested: 130 % × 130 % = 169 %")
    with st_zoom(10000 / 130):          # ≈ 76.9: back to 100 % absolute
        st_write(bs.badge, "Badge at 100 %")
st_write(bs.badge, "Badge at 100 % (outside any zoom)")""", language="python")
    st_space("v", 1)

    with st_zoom(130):
        st_write(s.medium, "Slide text at 130 %")
        with st_zoom(130):
            st_write(s.medium, "Nested: 130 % × 130 % = 169 %")
        with st_zoom(10000 / 130):
            st_write(bs.badge, "Badge at 100 %")
    st_write(bs.badge, "Badge at 100 % (outside any zoom)")
    st_space("v", 1)

    st_write(
        s.medium,
        "When the outer zoom varies from slide to slide, compute the counter-zoom "
        "from it, and clamp it if needed: st_zoom(max(20, min(100, round(10000 / slide_zoom)))).",
    )
    st_space("v", 2)

    # Section 7: Zoom in exports
    st_write(bs.section, "Zoom in Exports", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.medium, "Screen, HTML export and PDF export each have their own zoom:")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(s.medium, (s.bold, "Screen"), " — the sidebar Zoom %; the export panel carries it into the HTML and the PDF.")
        with l.item():
            st_write(s.medium, (s.bold, "HTML file"),
                     " — \"Zoom HTML (%)\" in the export panel: 0 follows the view zoom, "
                     "any other value replaces it in the HTML file only. From the command "
                     "line (streamtex 0.7.63): stx export html --zoom 80 opens the file as "
                     "if the browser were at 80 % (it multiplies with the document's own "
                     "st_zoom), --page-width 90 sets the page width in % of the window.")
        with l.item():
            st_write(s.medium, (s.bold, "PDF"),
                     " — \"Zoom (%)\" in the PDF layout (PdfConfig(zoom=...)): it multiplies "
                     "the view zoom, so view 80 % × PDF 70 % = 56 %. It shrinks everything, "
                     "vw/vh included; \"Scale\" (Chromium's print scale) only shrinks pt/px sizes.")
    st_space("v", 1)

    show_code("""\
st_book(
    [...],
    zoom=100,                       # screen
    html_export_zoom=0,             # HTML: follow the view
    pdf_config=PdfConfig(zoom=80),  # PDF: 80 % of the view
)""", language="python")
    st_space("v", 1)

    st_write(
        s.medium,
        "The Advanced manual (PDF Export) compares zoom and scale on real PDFs.",
    )
    st_space("v", 2)

    # Section 8: inject_zoom_logic (low-level API)
    st_write(bs.section, "Low-Level API: inject_zoom_logic()", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.feature_box):
        st_write(
            s.medium,
            (s.text.weights.bold_weight, "Note: "),
            "inject_zoom_logic() is the low-level function that injects the CSS zoom "
            "JavaScript into the page. It is called automatically by add_zoom_options(). "
            "You typically don't need to call it directly unless you are building "
            "a custom zoom control widget.",
        )
    st_space("v", 2)
