from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Export pipeline styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "The Export Pipeline",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. HtmlExportBuffer ---
        st_write(bs.sub, "HtmlExportBuffer", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            HtmlExportBuffer is the core data structure for
            HTML export. It accumulates HTML fragments as content
            is rendered, using push/pop for proper nesting of
            container elements like blocks and grids.
        """)
        st_space("v", 1)

        show_code("""\
# Simplified buffer lifecycle:
buffer = HtmlExportBuffer()

buffer.append('<div style="...">')   # open tag
buffer.append('<p>Hello</p>')        # content
buffer.append('</div>')              # close tag

html = buffer.generate_full_html()   # self-contained HTML""")
        st_space("v", 2)

        # --- 2. Dual-render architecture ---
        st_write(bs.sub, "Dual-render architecture", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Every content call goes to both Streamlit and the
            export buffer simultaneously. This dual-render approach
            ensures the exported HTML is pixel-identical to what
            appears on screen. No separate export pass is needed.
        """)
        st_space("v", 1)

        show_code("""\
# Inside _render():
def _render(style, content, tag):
    html = build_html(style, content, tag)

    # 1. Send to Streamlit for display
    st.html(html)

    # 2. Send to export buffer (if active)
    if export_config.enabled:
        export_buffer.append(html)""")
        st_space("v", 2)

        # --- 3. ExportConfig ---
        st_write(bs.sub, "ExportConfig", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            ExportConfig controls the export behavior: whether
            export is enabled, the page title, the page width,
            and other formatting options for the generated HTML.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import ExportConfig

export_cfg = ExportConfig(
    enabled=True,
    page_title="My Manual",
    page_width="900px",
)""")
        st_space("v", 2)

        # --- 4. st_html and the buffer ---
        st_write(bs.sub, "st_html(): the display + buffer bridge", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_html() is the bridge function that sends HTML to
            both Streamlit's display and the export buffer. All
            content-rendering functions ultimately call st_html()
            rather than st.html() directly.
        """)
        st_space("v", 1)

        show_code("""\
# StreamTeX's st_html() wraps Streamlit's st.html():
def st_html(html: str):
    st.html(html)                      # Streamlit display
    if _export_active():
        _export_buffer.append(html)    # Export capture""")
        st_space("v", 2)

        # --- 5. Export-aware widgets ---
        st_write(bs.sub, "Export-aware widgets", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Some Streamlit widgets (st.dataframe, st.metric, etc.)
            are interactive and cannot be captured as pure HTML.
            StreamTeX provides export-aware wrappers that render
            a static HTML equivalent into the export buffer while
            still showing the interactive widget on screen.
        """)
        st_space("v", 1)

        show_code("""\
# Export-aware wrapper example:
# On screen: interactive st.dataframe
# In export:  static HTML table

# The wrapper detects if export is active and writes
# both the interactive widget and the static HTML.""")
        st_space("v", 2)

        # --- 6. Buffer lifecycle ---
        st_write(bs.sub, "Buffer lifecycle", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
Buffer lifecycle:

1. reset()              — clear all accumulated HTML
2. append(html)         — add fragment to buffer
   push(open_tag)       — open a nested container
   pop(close_tag)       — close a nested container
3. generate_full_html() — produce self-contained HTML file
   |
   +-> wraps fragments in <html><head>...<body>...</body></html>
   +-> injects page title, width, and base styles
   +-> returns a single string ready for download""", language="text")
        st_space("v", 2)

        show_details("""\
            The **dual-render** approach adds minimal overhead: the
            buffer is just a list of strings.

            **Push/pop nesting** ensures correct HTML structure even
            with deeply nested grids inside blocks.

            **Export-aware widgets** provide graceful degradation:
            interactive on screen, static in export.
        """)
