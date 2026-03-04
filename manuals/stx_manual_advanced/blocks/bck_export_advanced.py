"""Advanced Export — ExportConfig, HtmlExportBuffer, and st_html()."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Styles for Advanced Export block."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight
    warning_box = ns("background:rgba(255,100,100,0.1);padding:16px;border-radius:8px;", "warning_box")
    tip_box = ns("background:rgba(100,200,100,0.1);padding:16px;border-radius:8px;", "tip_box")


bs = BlockStyles


def build():
    """Demonstrate advanced export features: ExportConfig, buffer, and st_html()."""

    st_write(bs.heading, "Advanced Export \u2014 ExportConfig & st_html", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX's HTML export system converts your live Streamlit app
        into a static, self-contained HTML file. This section covers the
        internal machinery: ExportConfig, the HtmlExportBuffer, the
        push/pop wrapper pattern, and the st_html() dual-render bridge.
    """)
    st_space("v", 2)

    # --- Section 1: ExportConfig ---
    st_write(bs.sub, "ExportConfig", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        ExportConfig is a dataclass that controls how the exported HTML
        page is generated. Pass it to st_book() via the export parameter.
    """)
    st_space("v", 1)

    show_code("""\
        from streamtex import ExportConfig

        export_cfg = ExportConfig(
            enabled=True,            # enable HTML export
            page_title="My Export",  # <title> of exported HTML
            page_width="90%",        # max-width of the page container
            page_padding="20px",     # padding around the page
        )

        st_book(blocks, export=export_cfg)""")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item(): st_write(s.medium, (bs.param_label, "enabled"), " \u2014 toggle export on or off (default False)")
        with l.item(): st_write(s.medium, (bs.param_label, "page_title"), " \u2014 the HTML page title in the exported file")
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
        all accumulated fragments into a complete, self-contained HTML
        document.
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

    show_explanation("""\
        The complete export cycle follows these steps:
    """)
    st_space("v", 1)

    with st_list(list_type="ol") as l:
        with l.item(): st_write(s.medium, "st_book() detects export is enabled and calls buffer.reset()")
        with l.item(): st_write(s.medium, "The book renders all blocks in order (paginated or continuous)")
        with l.item(): st_write(s.medium, "Each stx function appends its HTML fragment to the buffer")
        with l.item(): st_write(s.medium, "Nested containers use push/pop to maintain proper HTML structure")
        with l.item(): st_write(s.medium, "After all blocks render, generate_full_html() assembles the output")
        with l.item(): st_write(s.medium, "CSS from default.css is inlined into the HTML document")
        with l.item(): st_write(s.medium, "The final HTML file is offered for download via Streamlit")
    st_space("v", 2)

    # --- Section 7: CSS Bundling ---
    st_write(bs.sub, "CSS Bundling", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The exported HTML is fully self-contained. StreamTeX reads the
        project's default.css file and inlines it as a <style> block
        inside the generated HTML. This ensures that all styles render
        correctly when the HTML file is opened offline, without needing
        any external resources.
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
        #   </style>
        # </head>
        # <body>
        #   <div style="max-width:{page_width}; padding:{page_padding};">
        #     {accumulated_html_fragments}
        #   </div>
        # </body>
        # </html>""")
    st_space("v", 2)

    show_details("""\
        **ExportConfig** is a Python dataclass. All fields have sensible defaults.
        Only set enabled=True to activate export; the rest is optional.

        **HtmlExportBuffer** is a singleton managed by StreamTeX internally.
        You never instantiate it directly. It is reset at the start of each
        st_book() render cycle.

        **push/pop wrappers** are called automatically by context managers
        (st_block, st_grid, st_span). You only need to use export_push_wrapper
        and export_pop_wrapper if you are building custom container components.

        **st_html()** is the low-level bridge. Most users never call it directly.
        Higher-level functions (st_latex_doc, st_mermaid, st_tikz) use st_html()
        internally for iframe-based rendering.

        **CSS inlining** ensures the exported file works offline. If you add
        custom CSS files, they must be registered with StreamTeX to be included
        in the export bundle.

        **Performance note:** The export buffer accumulates all HTML in memory.
        For very large books (hundreds of blocks), memory usage may be significant
        during the export phase.
    """)
    st_space("v", 3)
