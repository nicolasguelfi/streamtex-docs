from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Rendering pipeline styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "The Rendering Pipeline",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Overview ---
        st_write(bs.sub, "Overview", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Every content call in StreamTeX (st_write, st_block,
            st_grid, etc.) ultimately generates HTML via st.html().
            The central _render() function is the dispatch point
            that converts content into an HTML string and sends it
            to Streamlit for display.
        """)
        st_space("v", 2)

        # --- 2. The _render() function ---
        st_write(bs.sub, "The _render() dispatch function", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            _render() is the heart of the rendering pipeline.
            It receives content and a Style object, builds an
            HTML string with inline CSS, and sends it to Streamlit.
            When the export buffer is active, the same HTML is
            also appended to the export buffer for later extraction.
        """)
        st_space("v", 1)

        show_code("""\
st_write(style, text)
    -> _render(style, text, tag)
        -> build HTML string with inline CSS
        -> st.html(html)              # Streamlit display
        -> export_append(html)         # Export buffer (if active)""", language="text")
        st_space("v", 2)

        # --- 3. Style resolution ---
        st_write(bs.sub, "Style resolution to CSS", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Style objects are resolved into CSS inline styles
            at render time. The Style's internal CSS string is
            inserted directly into the HTML element's style
            attribute. This avoids external stylesheets and
            ensures fully self-contained output.
        """)
        st_space("v", 1)

        show_code("""\
# A Style object wraps a CSS string
my_style = Style("color: red; font-weight: bold;", "my_style")

# At render time, it becomes:
# <div style="color: red; font-weight: bold;">content</div>""")
        st_space("v", 2)

        # --- 4. Context managers ---
        st_write(bs.sub, "Context managers and nesting", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Context managers like st_block, st_grid, and st_list
            use a push/pop mechanism for proper nesting. When you
            enter a context, the opening HTML tag is pushed. When
            you exit, the closing tag is popped. This ensures
            correct HTML structure even with deeply nested layouts.
        """)
        st_space("v", 1)

        show_code("""\
with st_block(style):      # push <div style="...">
    st_write(s, "Hello")   # renders inside the div
                           # pop </div>

# Nesting works correctly:
with st_block(outer):
    with st_grid(cols=2) as g:
        with g.cell():
            st_write(s, "Cell content")""")
        st_space("v", 2)

        # --- 5. Export buffer shadowing ---
        st_write(bs.sub, "Export buffer shadowing", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When the export buffer is active, every render call
            is shadowed: the HTML goes to both Streamlit display
            and the export buffer. This dual-render approach means
            the export output is identical to what appears on screen.
        """)
        st_space("v", 1)

        show_code("""\
# The export buffer captures everything rendered:
#
# st_write(s, "text")
#     -> st.html(html)          # user sees it on screen
#     -> buffer.append(html)    # captured for HTML export
#
# At the end, buffer.generate_full_html() produces
# a self-contained HTML file.""", language="text")
        st_space("v", 2)

        # --- 6. Full pipeline diagram ---
        st_write(bs.sub, "Full pipeline diagram", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
User code: st_write(style, "Hello World")
  |
  v
_render(style, text, tag)
  |
  +-> resolve Style -> inline CSS string
  |
  +-> build HTML: <tag style="css">text</tag>
  |
  +-> st.html(html)           [Streamlit iframe]
  |
  +-> export_append(html)     [if export active]""", language="text")
        st_space("v", 2)

        show_details("""\
            The rendering pipeline is intentionally simple:
            content in, HTML out.

            No virtual DOM, no diffing. Each call produces
            one st.html() invocation.

            This simplicity makes debugging straightforward:
            inspect the generated HTML string directly.
        """)
