"""Section Spacing with Profiles — Mode-specific spacing configuration."""
from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Section Spacing with Profiles",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            Each **PresentationProfile** can define its own **SpacingConfig**,
            which is the natural way to handle mode-specific spacing differences.

            When the user switches profiles, the spacing automatically changes.
            No mode-specific fields (paginated_margin_top etc.) needed.
        """)
        st_space("v", 2)

        # --- Profile spacing ---
        st_write(bs.sub, "Per-Profile Spacing", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
from streamtex import (
    PresentationProfile, PageLayout, ViewMode,
    Spacing, SpacingConfig,
)

presentation_profiles=[
    PresentationProfile(
        name="Slides",
        mode=ViewMode.PAGINATED,
        layout=PageLayout(width=100, zoom=100),
        spacing=SpacingConfig(
            block=Spacing(top=0),         # no gap in paginated
            section=Spacing(top=3),       # generous section spacing
        ),
    ),
    PresentationProfile(
        name="Handout",
        mode=ViewMode.CONTINUOUS,
        layout=PageLayout(width=80, zoom=90),
        spacing=SpacingConfig(
            block=Spacing(top="70px"),    # visible gap between blocks
            section=Spacing(top=1, left="5%", right="5%"),
        ),
    ),
]""")
        st_space("v", 2)

        # --- Override hierarchy ---
        st_write(bs.sub, "Override Hierarchy", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The 5-level override hierarchy (most specific wins):

            1. **Built-in** defaults (block.bottom="70px", section=None)
            2. **Book** global: set_spacing(SpacingConfig(...))
            3. **Profile**: PresentationProfile(spacing=SpacingConfig(...))
            4. **Block**: set_block_spacing(Spacing(...)) inside build()
            5. **Call-site**: st_slide_break(spacing=Spacing(...))

            Each level only overrides non-None fields. None = inherit from parent.
        """)
        st_space("v", 2)

        # --- Double-spacing prevention ---
        st_write(bs.sub, "Double-Spacing Prevention", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            block.top and section.top never stack at the start of a block.

            When st_book injects block.top before build(), the first
            st_slide_break or title marker in that block skips its own
            section.top to avoid double spacing.

            Subsequent breaks inject section.top normally.
        """)
        st_space("v", 2)

        # --- Horizontal margins ---
        st_write(bs.sub, "Horizontal Margins", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Spacing.left and Spacing.right control horizontal indentation
            per section. They affect both text content (via _render wrapping)
            and containers like st_block (via CSS :has() injection).

            **Note**: Native Streamlit widgets (st.button, st.slider) are not
            affected — only StreamTeX-rendered content.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_slide_break, Spacing

# Indented section (both text and containers move)
st_slide_break("Narrow Section", spacing=Spacing(
    top=2,
    left="15%",
    right="15%",
))

# Asymmetric indent (shifted right)
st_slide_break("Right-shifted", spacing=Spacing(
    left="20%",
))""")
