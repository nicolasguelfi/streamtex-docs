from streamtex import *
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Overlay demo styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    overlay_text = s.text.colors.white + s.bold + s.Large
    overlay_bg = ns("background-color: rgba(0, 0, 0, 0.5); padding: 8pt;")
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Overlays", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # Basic overlay
        st_write(bs.sub,
                 "st_overlay with positioned layers",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Place content on top of a base element
            with absolute positioning.
        """)
        st_space("v", 1)

        show_code(file="examples/overlay/overlay_basic.py")
        st_space("v", 1)

        with st_overlay(s.container.sizes.width_full) as o:
            with st_block(s.container.bg_colors.dark_slate_blue_bg
                          + ns("height: 200px; width: 100%;")):
                st_write(s.text.colors.white + s.large,
                         "Base content area (dark background)")
            with o.layer(top=20, left=20):
                with st_block(bs.overlay_bg):
                    st_write(bs.overlay_text, "Top-Left")
            with o.layer(bottom=20, right=20):
                with st_block(bs.overlay_bg):
                    st_write(bs.overlay_text, "Bottom-Right")
        st_space("v", 2)

        # Positioning parameters
        st_write(bs.sub,
                 "Layer positioning: top, left, right, bottom",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each o.layer() accepts top, left, right, bottom
            positioning parameters.
        """)
        st_space("v", 1)

        show_details("""\
            Integer values are treated as pixels.

            String values are used as-is (e.g., "50%").

            The base content determines the overlay container size.
        """)
        st_space("v", 2)

        # Center positioning
        st_write(bs.sub,
                 "Center positioning: overlaying at center",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use CSS transforms to center overlays.

            Combine with percentage positioning for responsive centering.
        """)
        st_space("v", 1)

        show_code("""\
with st_overlay(s.container.sizes.width_full) as o:
    with st_block(s.container.bg_colors.light_blue_bg
                  + ns("height: 200px; width: 100%;")):
        st_write(s.large, "Background")

    # Center overlay
    with o.layer(top="50%", left="50%"):
        with st_block(ns("transform: translate(-50%, -50%);")):
            st_write(bs.overlay_text, "Centered")""")
        st_space("v", 2)

        # Multiple layers
        st_write(bs.sub,
                 "Multiple layers: stacking overlays",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Stack multiple overlay layers on top of each other.

            Each layer can have different positioning and content.
        """)
        st_space("v", 1)

        show_code(file="examples/overlay/overlay_multiple_layers.py")
        st_space("v", 2)

        # Use case: Badges and labels
        st_write(bs.sub,
                 "Use case: Badges and sale labels",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Overlays are perfect for adding badges, sale tags, or status indicators
            to content without modifying the base structure.
        """)
        st_space("v", 1)

        show_code(file="examples/overlay/overlay_badges.py")
        st_space("v", 2)

        # Use case: Tooltips and annotations
        st_write(bs.sub,
                 "Use case: Hover tooltips and annotations",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use overlays for static annotations.

            For interactive tooltips, consider combining with CSS hover states.
        """)
        st_space("v", 1)

        show_code("""\
with st_overlay(s.container.sizes.width_full) as o:
    # Main content
    with st_block(s.container.bg_colors.light_blue_bg
                  + ns("height: 100px; padding: 20px;")):
        st_write(s.large, "Feature List")

    # Annotation arrows/labels
    with o.layer(top=30, right=10):
        st_write(ns("color: #FF6600; font-size: 12px;"),
                "← New feature")""")
        st_space("v", 2)

        # Z-index and layering
        st_write(bs.sub,
                 "Advanced: z-index and layering order",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            By default, later overlay layers appear on top.

            Use z-index CSS to explicitly control stacking order.
        """)
        st_space("v", 1)

        show_code(file="examples/overlay/overlay_zindex.py")
        st_space("v", 2)

        # Responsive overlays
        st_write(bs.sub,
                 "Responsive overlays: percentage positioning",
                 toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Use percentage values for positioning to make overlays responsive.

            Percentages are relative to the base container.
        """)
        st_space("v", 1)

        show_code(file="examples/overlay/overlay_responsive.py")
        st_space("v", 2)

        # Best practices and limitations
        st_write(bs.sub,
                 "Best practices and limitations",
                 toc_lvl="+1")
        st_space("v", 1)

        st_write(s.large, (s.bold, "DO:"))
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, "Use overlays for static decorative elements")
            with l.item():
                st_write(s.large, "Position labels, badges, and annotations")
            with l.item():
                st_write(s.large, "Layer related content (image + caption)")
            with l.item():
                st_write(s.large, "Use percentage positioning for responsiveness")
            with l.item():
                st_write(s.large, "Keep overlay content minimal (text or icons)")

        st_write(s.large, (s.bold, "DON'T:"))
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, "Hide important content under overlays")
            with l.item():
                st_write(s.large, "Create overlays that block navigation")
            with l.item():
                st_write(s.large, "Use overlays for layouts (use st_grid instead)")
            with l.item():
                st_write(s.large, "Put interactive elements in overlays (not clickable)")
            with l.item():
                st_write(s.large, "Overlap too many layers (becomes unreadable)")

        st_write(s.large, (s.bold, "Limitations:"))
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, "Overlays are not interactive (no click events)")
            with l.item():
                st_write(s.large, "Complex nested overlays can be hard to maintain")
            with l.item():
                st_write(s.large, "Sizing depends on base container height")
            with l.item():
                st_write(s.large, "Export to HTML may not preserve all positioning")
        st_space("v", 2)

        show_details("""\
            Overlays are best for simple decorative layering.

            For complex interactive layouts, use st_grid or st_block instead.

            Remember: overlays don't affect document flow or layout.
        """)
