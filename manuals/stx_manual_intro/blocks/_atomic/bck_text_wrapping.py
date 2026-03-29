from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Text wrapping styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    demo = s.Large + s.text.wrap.hyphens
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Text Wrapping",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. Overview ---
        st_write(bs.sub, "Wrapping modes", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StreamTeX provides four text wrapping styles via
            `s.text.wrap.*`. These control how text flows and
            breaks inside containers, grids, and blocks.
        """)
        st_space("v", 1)

        show_code("""\
# Default browser wrapping
s.text.wrap.wrap       # text-wrap: wrap

# Prevent line breaks
s.text.wrap.nowrap     # text-wrap: nowrap

# Preserve newlines (\\n → line break)
s.text.wrap.preline    # white-space: pre-line

# Automatic hyphenation at line breaks
s.text.wrap.hyphens    # hyphens: auto; overflow-wrap: break-word""", language="python")
        st_space("v", 2)

        # --- 2. Hyphenation ---
        st_write(bs.sub, "Hyphenation (hyphens)", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            `s.text.wrap.hyphens` enables automatic word hyphenation.
            This is essential for large fonts in narrow containers
            (e.g. grid cells in presentations) where long words
            would otherwise overflow.

            Compose it with any text style:
        """)
        st_space("v", 1)

        show_code("""\
# Large text with automatic hyphenation
body = Style.create(
    s.Large + s.text.wrap.hyphens,
    "my_body",
)

# In a grid cell — prevents overflow
keyword = Style.create(
    s.Large + s.bold + s.project.colors.primary + s.text.wrap.hyphens,
    "my_keyword",
)

st_write(body, "Internationalization and Telecommunications")
st_write(keyword, "Artificial Intelligence")""", language="python")
        st_space("v", 2)

        show_details("""\
            Hyphenation depends on the browser's language detection.
            For best results with non-English text, set the `lang`
            attribute on the HTML document (Streamlit handles this
            automatically for the primary language).

            `overflow-wrap: break-word` is included as a fallback
            for words that the browser cannot hyphenate (e.g. URLs,
            technical terms without dictionary entries).
        """)
