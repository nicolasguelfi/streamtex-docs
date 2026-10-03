"""Presentation Mode — fullscreen 16/9 slide deck with footer and sidebar controls.

Documents the Presentation API: PresentationConfig, set_presentation_config,
st_presentation_footer, add_presentation_options, and the slide helper
st_slide / SLIDE_CONTAINER / set_slide_container (0.7.37).
"""

from streamtex import (
    st_write, st_block, st_space,
    PresentationConfig, set_presentation_config,  # noqa: F401 — API coverage
    st_presentation_footer, add_presentation_options,  # noqa: F401 — API coverage
    ViewMode,  # noqa: F401 — API coverage
    st_slide, set_slide_container, SLIDE_CONTAINER,  # noqa: F401 — API coverage
)
from streamtex.styles import Style
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
], paginate=True, view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS])""")
        st_space("v", 3)

        # --------------------------------------------------------------
        # View Modes
        # --------------------------------------------------------------
        st_write(bs.sub, "View Modes", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The view_modes parameter on st_book() controls which viewing
            modes are available to the reader. By default both Paginated
            and Continuous modes are offered via a radio button in the
            sidebar. You can restrict the available modes by passing a
            subset — if only one mode is listed, the radio button is
            hidden entirely.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_book, ViewMode

# Both modes available (default — radio button visible)
st_book(blocks, view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS])

# Paginated only — radio button hidden
st_book(blocks, view_modes=[ViewMode.PAGINATED])

# Continuous only — radio button hidden
st_book(blocks, view_modes=[ViewMode.CONTINUOUS])

# None = both modes (same as omitting the parameter)
st_book(blocks, view_modes=None)""")
        st_space("v", 1)

        show_details("""\
            Typical use case: restrict a deployed web version to
            paginated-only while keeping both modes during local
            development.

            import os
            from streamtex import st_book, ViewMode

            if os.getenv("STX_DEPLOYED"):
                modes = [ViewMode.PAGINATED]
            else:
                modes = [ViewMode.PAGINATED, ViewMode.CONTINUOUS]

            st_book(blocks, paginate=True, view_modes=modes)

            When a PresentationProfile switch targets a mode that is
            not in the allowed list, the value is automatically clamped
            to the first allowed mode.
        """)
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
        st_space("v", 3)

        # --------------------------------------------------------------
        # One slide — st_slide() (0.7.37)
        # --------------------------------------------------------------
        st_write(bs.sub, "One slide — st_slide()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            A block often holds several slides. st_slide() writes the two
            calls a block would otherwise write by hand for each of them:
            the break before the slide (cut=True calls st_slide_break()),
            then the slide container (an st_block). Nothing else.

            The helper is deliberately thin. The title, the marker, the
            zoom, the alignment and every size stay written in the block,
            slide by slide — so any slide can be specialised at any time
            without fighting a helper that decided for you.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex import st_slide, st_write, st_zoom
from streamtex.styles import Style
from custom.styles import Styles as s

def build():
    with st_slide():                      # first slide: no break before it
        st_zoom(120)
        st_write(s.huge + s.center_txt, "Why containers?", toc_lvl="1")

    with st_slide(cut=True):              # a break, then the slide
        st_write(s.large, "Three reasons", toc_lvl="+1")

    # This slide only: a style added (+) to the container
    with st_slide(cut=True, style=Style("min-height: 60vh;", "short_slide")):
        st_write(s.large, "Questions?")""")
        st_space("v", 1)

        show_explanation("""\
            Live example — st_slide(style=...) with a short container, so
            that the slide fits in this page. The dashed border is part of
            the per-call style; the title and its size are written here,
            in the block.
        """)
        st_space("v", 1)

        demo_slide = Style("min-height: 20vh; margin: 2vh 0; "
                           "border: 1px dashed rgba(128,128,128,0.6);",
                           "pm_demo_slide")
        with st_slide(style=demo_slide):
            st_write(s.huge + s.center_txt, "A slide written by st_slide()")
        st_space("v", 2)

        show_details("""\
            SLIDE_CONTAINER, the default container:

            min-height: 80vh; margin: 10vh 0; display: flex;
            flex-direction: column; justify-content: center;

            — at least 80 % of the window, 10 vh above and below, content
            centred vertically. A style passed with style= is added to it
            (box + style), so its declarations win for that slide only.
        """)
        st_space("v", 2)

        st_write(bs.sub, "One container per book — set_slide_container()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            set_slide_container(style) replaces SLIDE_CONTAINER for every
            st_slide() of the book. Call it once in book.py — typically
            with the design system's own slide container. None restores
            SLIDE_CONTAINER. A per-call style= still applies on top.
        """)
        st_space("v", 1)

        show_code("""\
# book.py — once, before st_book()
import streamtex as stx
from custom.styles import Styles as s

stx.set_slide_container(s.project.containers.slide_center)

# Back to the library default
stx.set_slide_container(None)""")
        st_space("v", 1)

        show_details("""\
            What st_slide() does NOT do, on purpose: no title, no
            st_marker(), no st_zoom(), no sizes. Writing them in the block
            keeps every value explicit and visible where the slide is read.
            st_slide() was promoted from a helper used on 341 slides of a
            training project; that project keeps working unchanged.
        """)
