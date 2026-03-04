import os
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Theme demo styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Themes", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # How themes work
        st_write(bs.sub, "How themes work", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            A theme is a Python dictionary
            mapping style_ids to replacement CSS strings.
        """)
        st_space("v", 1)

        # Read actual themes.py
        try:
            # _atomic/ → blocks/ → project root → custom/
            _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            themes_path = os.path.join(_project_root, "custom", "themes.py")
            with open(themes_path) as f:
                themes_source = f.read()
            show_code(themes_source)
        except Exception:
            show_code("""\
# custom/themes.py
dark = {
    "primary_blue": "color: #7AB8F5;",
    "section_title": "color: #7AB8F5; font-weight: bold;",
    "good_example_bg": "background-color: rgba(...);",
}""")
        st_space("v", 2)

        # Activating a theme
        st_write(bs.sub, "Activating a theme in book.py", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Set the theme dict in book.py
            before rendering blocks.
        """)
        st_space("v", 1)

        show_code("""\
import streamtex.styles as sts
from custom.themes import dark
sts.theme = dark""")
        st_space("v", 2)

        # Override table
        st_write(bs.sub,
                 "This project's theme overrides",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The dark theme remaps specific style_ids
            for better contrast on dark backgrounds.
        """)
        st_space("v", 1)

        with st_grid(cols="1fr 1fr 1fr", cell_styles=bs.cell) as g:
            # header
            with g.cell(): st_write(s.bold + s.large, "style_id")
            with g.cell(): st_write(s.bold + s.large, "Original")
            with g.cell(): st_write(s.bold + s.large, "Dark Override")
            # row 1
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "primary_blue")
            with g.cell(): st_write(s.large, "#4A90D9")
            with g.cell(): st_write(s.large, "#7AB8F5 (lighter)")
            # row 2
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "section_title")
            with g.cell():
                st_write(s.large, "Full style (blue 80pt bold)")
            with g.cell():
                st_write(s.large, "Lighter blue for dark bg")
            # row 3
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "good_example_bg")
            with g.cell(): st_write(s.large, "15% opacity green")
            with g.cell():
                st_write(s.large, "25% opacity (brighter on dark)")
        st_space("v", 2)

        show_details("""\
            Override only what needs dark adaptation.

            Most styles work well in both modes
            if you avoid hardcoded black/white.
        """)
        st_space("v", 2)

        # StyleGrid in themed layouts
        st_write(bs.sub, "StyleGrid: Per-cell styling in themes", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            StyleGrid allows different cells in a grid to have different styles.
            Perfect for creating themed table layouts where each cell inherits
            the theme's overrides.
        """)
        st_space("v", 1)

        show_code(file="examples/theme/stylegrid_per_cell.py")
        st_space("v", 2)

        # Theme composition
        st_write(bs.sub, "Theme composition and merging", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Themes are dictionaries that can be composed:
            - Base theme with foundational colors
            - Light/dark variants override specific entries
            - Merge multiple themes for compound effects
        """)
        st_space("v", 1)

        show_code(file="examples/theme/theme_composition.py")
        st_space("v", 2)

        # Theme switching patterns
        st_write(bs.sub, "Dynamic theme switching", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use Streamlit session state to switch themes at runtime.
            Each theme change updates the global sts.theme dictionary.
        """)
        st_space("v", 1)

        show_code(file="examples/theme/theme_dynamic_switching.py")
        st_space("v", 2)

        # Custom theme creation best practices
        st_write(bs.sub, "Creating custom themes: best practices", toc_lvl="+1")
        st_space("v", 1)

        st_write(s.large, (s.bold, "DO:"))
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, "Use consistent color palettes (same hue, different lightness)")
            with l.item():
                st_write(s.large, "Override only what changes between themes (not everything)")
            with l.item():
                st_write(s.large, "Use RGBA colors for backgrounds to support transparency")
            with l.item():
                st_write(s.large, "Document which style_ids are overridden in comments")
            with l.item():
                st_write(s.large, "Test both light and dark modes")

        st_write(s.large, (s.bold, "DON'T:"))
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, "Hardcode black (#000000) or white (#FFFFFF)")
            with l.item():
                st_write(s.large, "Override every single style_id (most work in both modes)")
            with l.item():
                st_write(s.large, "Mix color schemes (don't mix warm and cool accents)")
            with l.item():
                st_write(s.large, "Use opaque colors that hide content (use transparency)")
            with l.item():
                st_write(s.large, "Assume all users have same display brightness")
        st_space("v", 2)

        show_details("""\
            The theme system is optional. Styles work fine without themes.

            Themes are powerful when you need dark/light mode or brand customization.

            Keep themes focused on color and contrast — not layout or typography.
        """)
