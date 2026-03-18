"""Presentation Mode — fullscreen 16/9 slide deck with footer and sidebar controls.

Documents the Presentation API: PresentationConfig, set_presentation_config,
st_presentation_footer, and add_presentation_options.
"""

from streamtex import (
    st_write, st_block, st_space,
    PresentationConfig, set_presentation_config,  # noqa: F401 — API coverage
    st_presentation_footer, add_presentation_options,  # noqa: F401 — API coverage
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Presentation mode reference styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    field_name = s.bold + s.large
    field_desc = s.large


bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Presentation Mode", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            StreamTeX supports a fullscreen 16/9 presentation mode that
            transforms any book into a slide deck. The presentation system
            injects CSS to enforce aspect ratios, centre content vertically,
            hide Streamlit chrome, and add a fixed footer bar with slide
            counter and title.

            The API consists of four main exports: PresentationConfig (the
            configuration dataclass), set_presentation_config (to activate
            presentation mode), st_presentation_footer (to render the footer
            bar), and add_presentation_options (to add sidebar controls).
        """)
        st_space("v", 3)

        # --------------------------------------------------------------
        # PresentationConfig
        # --------------------------------------------------------------
        st_write(bs.sub, "PresentationConfig", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            PresentationConfig is a dataclass that controls every aspect
            of the presentation layout. All fields have sensible defaults
            — you only need to set what you want to customize.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import PresentationConfig

config = PresentationConfig(
    # Identity
    title="Introduction to Docker",
    subtitle="A hands-on workshop",

    # Aspect ratio
    aspect_ratio="16/9",       # CSS aspect-ratio ("16/9", "4/3", "16/10")
    enforce_ratio=True,        # Apply aspect-ratio + overflow:hidden

    # Footer
    footer=True,               # Show fixed slide counter bar
    counter_mode="bloc",       # "bloc" = section count, "slide" = marker count
    footer_height="48px",      # CSS height of the footer bar
    footer_bg=None,            # Background colour (None = inherit theme)
    footer_text_color=None,    # Text colour (None = inherit theme)
    footer_font_size="18px",   # Font size for footer text

    # Layout
    center_content=True,       # Vertically centre slide content
    content_padding="48px 64px",  # CSS padding inside each slide

    # Streamlit UI
    hide_streamlit_header=True,   # Hide the Streamlit header bar
    hide_streamlit_footer=True,   # Hide the "Made with Streamlit" footer
    hide_deploy_button=True,      # Hide the deploy button
    sidebar_default="collapsed",  # Initial sidebar state

    # Transitions (future)
    slide_transition="none",   # "none", "fade", "slide"
    transition_duration="0.3s",
)""")
        st_space("v", 3)

        # --------------------------------------------------------------
        # Setup in book.py
        # --------------------------------------------------------------
        st_write(bs.sub, "Setup in book.py", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            To activate presentation mode, call set_presentation_config()
            once at the top of your book.py, before st_book(). Combine it
            with set_slide_break_config() for slide separators and
            add_presentation_options() for sidebar controls.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import (
    st_book, PresentationConfig, set_presentation_config,
    add_presentation_options,
    SlideBreakConfig, SlideBreakMode, set_slide_break_config,
)

# 1. Configure presentation mode
set_presentation_config(PresentationConfig(
    title="My Presentation",
    aspect_ratio="16/9",
    footer=True,
    center_content=True,
    hide_streamlit_header=True,
    enforce_ratio=True,
))

# 2. Configure slide breaks
set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.FULL,
    space="5vh",
    marker=True,
))

# 3. Add sidebar controls (toggle footer, fullscreen)
add_presentation_options()

# 4. Launch the book
st_book([
    blocks.bck_title_slide,
    blocks.bck_agenda,
    blocks.bck_content,
    blocks.bck_conclusion,
], paginate=True)""")
        st_space("v", 3)

        # --------------------------------------------------------------
        # Presentation Footer
        # --------------------------------------------------------------
        st_write(bs.sub, "Presentation Footer", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The footer bar is rendered automatically by st_book() when a
            PresentationConfig is active. You can also call
            st_presentation_footer() manually for custom setups where
            you need full control over slide numbering.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_presentation_footer, PresentationConfig

# Automatic: st_book() renders the footer when PresentationConfig is set.
# No manual call needed in the standard workflow.

# Manual usage for custom setups:
st_presentation_footer(
    current_slide=3,
    total_slides=12,
    title="My Presentation",     # Falls back to config.title if omitted
    config=None,                 # Falls back to get_presentation_config()
)""")
        st_space("v", 1)

        show_details("""\
            The footer displays the presentation title on the left and
            a counter on the right. Two counter modes are available:

            - counter_mode="bloc" (default): shows "Bloc N / M" where
              N is the current section and M the total number of
              sections. The values are static (server-side).

            - counter_mode="slide": shows "Slide N / M" where N and M
              match the floating marker navigation bar. The counter is
              updated dynamically via JavaScript as you navigate
              between markers.

            The footer uses a fixed position at the bottom of the
            viewport with a subtle top border. It respects theme
            colours by default, but you can override footer_bg and
            footer_text_color in PresentationConfig.
        """)
        st_space("v", 3)

        # --------------------------------------------------------------
        # Sidebar Controls
        # --------------------------------------------------------------
        st_write(bs.sub, "Sidebar Controls", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            add_presentation_options() adds presenter controls to the
            sidebar (or any container you specify). It provides toggles
            for footer visibility and fullscreen mode.

            This function is a no-op if no PresentationConfig has been
            set, so it is safe to call unconditionally.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import add_presentation_options

# Add controls to the sidebar (default)
add_presentation_options()

# Add controls to a custom container
import streamlit as st
with st.expander("Presenter Controls"):
    add_presentation_options(container=st)""")
        st_space("v", 1)

        show_details("""\
            The sidebar controls include:
            - "Show footer" toggle — enables or disables the footer bar
            - "Fullscreen mode" toggle — controls the fullscreen layout

            Both toggles persist their state in Streamlit session state
            across reruns. The initial values are derived from the
            PresentationConfig (footer=True, fullscreen=True by default).
        """)
