import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Style system internals styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "The Style System Internals",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. The Style class ---
        st_write(bs.sub, "The Style class", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The Style class is the fundamental building block of
            StreamTeX's styling system. It wraps a CSS string and
            a style_id that uniquely identifies it for theme
            overrides and debugging.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.styles import Style

# Create a style from a CSS string
my_style = Style("color: blue; font-size: 1.2em;", "my_style")

# The CSS string is stored internally
# The style_id is used for theme lookups and debugging""")
        st_space("v", 2)

        # --- 2. Style composition ---
        st_write(bs.sub, "Style composition: + and -", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Styles can be composed using the + operator to merge
            CSS properties, and the - operator to remove specific
            properties. This creates a new Style without modifying
            the originals.
        """)
        st_space("v", 1)

        show_code("""\
# Merge two styles (CSS properties are combined)
combined = style_a + style_b

# Add CSS via string
with_margin = style_a + "margin-top: 1em;"

# Remove a property
no_border = style_a - "border"

# Chain operations
result = base + bold + "padding: 8px;" - "margin" """)
        st_space("v", 2)

        # --- 3. Style.create() ---
        st_write(bs.sub, "Style.create() for theme overrides", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Style.create() copies an existing style with a new
            style_id. This is essential for theme overrides,
            where you want the same CSS but a different identity
            so the theme system can target it.
        """)
        st_space("v", 1)

        show_code("""\
# Copy a style with a new ID
my_heading = Style.create(s.bold + s.Large, "my_heading")

# The theme system can now override "my_heading" specifically
# without affecting the original s.bold or s.Large""")
        st_space("v", 2)

        # --- 4. StxStyles aggregation ---
        st_write(bs.sub, "StxStyles: the style aggregation class", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StxStyles is the aggregation class that organizes all
            built-in styles into logical groups: Text, Container,
            Grid, Visibility, and more. Project-level styles
            (custom/styles.py) follow the same pattern.
        """)
        st_space("v", 1)

        show_code("""\
# Built-in style groups accessed via stx.sts or s:
s.bold          # Text style
s.large         # Text style
s.center_txt    # Text alignment
s.container.borders.solid_border   # Container style
s.container.paddings.small_padding # Container style""")
        st_space("v", 2)

        # --- 5. Package structure ---
        st_write(bs.sub, "styles/ package structure", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
streamtex/styles/
    __init__.py      # exports Style, StyleGrid, StxStyles
    core.py          # Style class, StyleGrid class
    text.py          # text styles (bold, italic, sizes)
    container.py     # container styles (borders, padding, layout)
    visibility.py    # visibility styles (hidden, export-only)
    base.py          # base/reset styles""", language="text")
        st_space("v", 2)

        # --- 6. Theme overrides ---
        st_write(bs.sub, "Theme overrides and dark mode", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The theme system uses a dictionary mapping style_id
            to replacement CSS. When a style is rendered, the
            system checks if a theme override exists for its
            style_id and substitutes the CSS if so.
        """)
        st_space("v", 1)

        show_code("""\
# Theme override dictionary
dark_theme = {
    "heading_style": "color: #e0e0e0; font-weight: bold;",
    "body_style": "color: #cccccc;",
}

# Apply a theme
sts.theme = dark_theme

# Now any Style with style_id="heading_style" will use
# the dark theme CSS instead of its original CSS""")
        st_space("v", 2)

        show_details("""\
            Style composition is immutable: + and - always return
            new Style objects.

            Use Style.create() when you need theme-targetable styles.

            The styles/ package is designed for extension: add new
            .py files with style classes and register them in StxStyles.
        """)
