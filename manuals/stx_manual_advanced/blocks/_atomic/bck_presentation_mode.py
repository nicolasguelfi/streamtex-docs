"""Presentation Mode — fullscreen 16/9 slide deck with footer and sidebar controls.

Documents the Presentation API: PresentationConfig, set_presentation_config,
st_presentation_footer, add_presentation_options, the break marker
(SlideBreakConfig.marker), and the single slide construction st_slide
(0.7.37; marker=, key=, roles=, box=, zoom=, spacing=, config=) with
SLIDE_CONTAINER / set_slide_container / get_slide_container (per session),
set_slide_note (0.7.70) and set_slide_notes / SlideNote (0.7.72).
"""

from streamtex import (
    st_write, st_block, st_list, st_space,
    MarkerRoles,
    PresentationConfig, set_presentation_config,  # noqa: F401 — API coverage
    st_presentation_footer, add_presentation_options,  # noqa: F401 — API coverage
    ViewMode,  # noqa: F401 — API coverage
    st_slide, set_slide_container, get_slide_container, SLIDE_CONTAINER,  # noqa: F401 — API coverage
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
    code = s.text.fonts.font_monospace + s.big


bs = BlockStyles

#: Contradictory st_slide() calls: each raises before anything is drawn.
_SLIDE_RULES = [
    ("st_slide(box=False, style=...)",
     {"box": False, "style": Style("color: inherit;", "pm_rule_style")}),
    ("st_slide(zoom=80)", {"zoom": 80}),
    ('st_slide(cut=True, marker=False, key="x")', {"cut": True, "marker": False, "key": "x"}),
    ("st_slide(marker=MarkerRoles.HIDDEN, roles=MarkerRoles.NAMED)",
     {"marker": MarkerRoles.HIDDEN, "roles": MarkerRoles.NAMED}),
]


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
    enforce_ratio=True,        # Apply aspect-ratio + overflow:hidden (0.7.75: a page of several slides scrolls)

    # Footer
    footer=True,               # Show fixed slide counter bar
    counter_mode="bloc",       # "bloc" = page / entry count, "slide" = slide number over the stops
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
    st_book, MarkerConfig, PresentationConfig, set_presentation_config,
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

# 2. Configure slide breaks (stored per session)
set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.FULL,
    space="5vh",
    marker=True,          # each break: a stop, not listed (marker_hidden=True);
))                        # False = no marker; or a MarkerRoles(...)

# 3. Add sidebar controls (toggle footer, fullscreen)
add_presentation_options()

# 4. Launch the book — a deck: one stop per slide, no heading stops
st_book([
    blocks.bck_title_slide,
    blocks.bck_agenda,
    blocks.bck_content,
    blocks.bck_conclusion,
], paginate=True, view_modes=[ViewMode.PAGINATED, ViewMode.CONTINUOUS],
   marker_config=MarkerConfig(auto_marker_on_toc=0, scroll_offset=0))""")
        st_space("v", 1)

        show_details("""\
            SlideBreakConfig.marker is the marker of every break: True (a
            stop; listed only when marker_hidden=False), False (no marker)
            or a MarkerRoles. One call overrides it with
            st_slide_break(marker=True | False | MarkerRoles(...)). Every
            break starts a new slide, with or without a marker: a heading
            after it can be linked to the break's stop with
            st_write(..., marker="attach").
        """)
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
              N is the current page and M the number of pages (in
              continuous mode: 1 over the number of book entries). The
              values are static (server-side).

            - counter_mode="slide": shows "Slide N / M" where N is the
              slide number and M the number of stops — the same numbers
              as the floating widget's counter, updated as you navigate.
              A paginated page paints the slide number from the start:
              the deep-linked marker's, else the page's first stop, else
              the last stop before the page. Without any stop, it falls
              back to the page count.

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
        # One slide — st_slide()
        # --------------------------------------------------------------
        st_write(bs.sub, "One slide — st_slide()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            st_slide() (0.7.37) is the single construction for one slide
            of a block. It writes three things, in this order: the break
            before the slide (cut=True), the slide's marker, then the slide
            box. Nothing else: the title, the zoom of the content, the
            alignment and every size stay written in the block, slide by
            slide — so any slide can be specialised at any time without
            fighting a helper that decided for you.
        """)
        st_space("v", 1)

        show_code("""\
st_slide(
    cut=False,        # True: st_slide_break() before the slide
    style=None,       # a Style added (+) to the box, for this slide only
    *,
    marker=None,      # the slide's marker: None | False | True | "Label" | MarkerRoles(...)
    key=None,         # its stable deep-link key (as st_marker(key=))
    roles=None,       # its roles (as st_marker(roles=))
    box=True,         # False: no box, the content flows (forms B and D)
    zoom=None,        # settings of the break before the slide,
    spacing=None,     #   as st_slide_break() takes them;
    config=None,      #   they need cut=True
)                     # a context manager: with st_slide(...): ...""")
        st_space("v", 1)

        st_write(bs.field_name, "marker= — at most one marker per slide")
        st_space("v", 1)
        with st_block(s.project.containers.explanation_box):
            with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
                with l.item():
                    st_write(s.large, (s.bold, "None"),
                             " (default) — as before: with cut=True the break places its "
                             "usual marker (SlideBreakConfig: a stop, not listed); without "
                             "cut, no marker.")
                with l.item():
                    st_write(s.large, (s.bold, "False"),
                             " — no marker; with cut=True the break still draws its rule "
                             "and spacer and starts a new slide.")
                with l.item():
                    st_write(s.large, (s.bold, "True"), " — a stop, not listed.")
                with l.item():
                    st_write(s.large, (s.bold, "\"Label\""),
                             " — a stop, listed, with that label (as st_marker(\"Label\")).")
                with l.item():
                    st_write(s.large, (s.bold, "key= / roles="),
                             " — as st_marker; a MarkerRoles can also be given as marker=.")
            st_write(s.large, """\
                With cut=True the marker takes the place of the break's own
                marker; without, it comes just before the box, never inside.
                An explicit marker is placed whatever the break mode or the
                sidebar's slide-break switch: it belongs to the slide. Link
                the slide's title to it with marker="attach".
            """, breaks=False)
        st_space("v", 1)

        show_code("""\
from streamtex import st_slide, st_write
from custom.styles import Styles as s

def build():
    with st_slide(marker="Why containers?"):          # first slide: its listed stop, then the box
        st_write(s.huge + s.center_txt, "Why containers?", toc_lvl="1", marker="attach")

    with st_slide(cut=True, marker="Three reasons", key="reasons"):  # break, stop, box
        st_write(s.large, "Three reasons", toc_lvl="+1", marker="attach")

    # The break's usual stop; this slide only: a style added (+) to the box
    with st_slide(cut=True, style=s.project.containers.slide_top):
        st_write(s.large, "Questions?")

    with st_slide(cut=True, zoom=80):                 # the break's settings (cut=True only)
        st_write(s.large, "Appendix")""")
        st_space("v", 1)

        st_write(bs.field_name, "Three forms, one construction")
        st_space("v", 1)
        with st_block(s.project.containers.explanation_box):
            with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
                with l.item():
                    st_write(s.large, (s.bold, "S"),
                             " — each slide in the module's slide box (box=True, the "
                             "default). The usual form.")
                with l.item():
                    st_write(s.large, (s.bold, "B"),
                             " — free content cut by breaks, inside a composite only: "
                             "with st_slide(cut=True, box=False).")
                with l.item():
                    st_write(s.large, (s.bold, "D"),
                             " — a scrolling slide, taller than the screen: no box, no "
                             "break inside, one marker at its head: "
                             "with st_slide(cut=True, marker=\"Long read\", box=False).")
        st_space("v", 1)

        st_write(bs.field_name, "Rules (executed here)")
        st_space("v", 1)
        with st_list(list_type="ul", l_style=s.big, li_style=s.big) as l:
            for call, kwargs in _SLIDE_RULES:
                try:
                    with st_slide(**kwargs):
                        pass
                    outcome = "accepted"
                except (TypeError, ValueError) as exc:
                    outcome = f"{type(exc).__name__}: {exc}"
                with l.item():
                    st_write(s.big, (bs.code, call), " → ", outcome)
        st_space("v", 2)

        show_explanation("""\
            Live example — st_slide(style=..., marker=True,
            key="st-slide-demo") with a short box, so that the slide fits
            in this page. The slide has its own stop, not listed: ▶ lands
            on it, and ?marker=st-slide-demo opens it. The dashed border is
            part of the per-call style; the title and its size are written
            here, in the block.
        """)
        st_space("v", 1)

        demo_slide = Style("min-height: 20vh; margin: 2vh 0; "
                           "border: 1px dashed rgba(128,128,128,0.6);",
                           "pm_demo_slide")
        with st_slide(style=demo_slide, marker=True, key="st-slide-demo"):
            st_write(s.huge + s.center_txt, "A slide written by st_slide()")
        st_space("v", 2)

        show_details("""\
            SLIDE_CONTAINER, the default box:

            min-height: 80vh; margin: 10vh 0; display: flex;
            flex-direction: column; justify-content: center;

            — at least 80 % of the window, 10 vh above and below, content
            centred vertically. A style passed with style= is added to it
            (box + style), so its declarations win for that slide only.
        """)
        st_space("v", 2)

        st_write(bs.sub, "One box per module — set_slide_container()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            set_slide_container(style) replaces SLIDE_CONTAINER for every
            st_slide() of the module. Call it once in book.py, before
            st_book(), with the design system's own slide box. None
            restores SLIDE_CONTAINER; get_slide_container() returns the box
            st_slide() uses now. A per-call style= still applies on top.
        """)
        st_space("v", 1)

        show_code("""\
# book.py — once, before st_book()
import streamtex as stx
from custom.styles import Styles as s

stx.set_slide_container(s.project.containers.slide_center)

stx.get_slide_container()          # the box st_slide() uses now
stx.set_slide_container(None)      # back to SLIDE_CONTAINER""")
        st_space("v", 1)

        st_write(s.large, (s.bold, "In this manual: "),
                 "get_slide_container() is ",
                 (bs.code, get_slide_container().style_id),
                 " (read while this page renders).")
        st_space("v", 1)

        show_details("""\
            Per session: set_slide_container() and set_slide_break_config()
            store their value in the Streamlit session. book.py runs at
            every rerun of every session, so each session gets its module's
            box and break settings, and two modules served by one process
            no longer overwrite each other. Outside a session (tests, the
            stx CLIs) a process-wide value is used. The marker and TOC
            registries, the spacing state and the export buffer stay
            process-wide.
        """)
        st_space("v", 2)

        st_write(bs.sub, "A note at the foot of every slide — set_slide_note()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            set_slide_note(note, link=, style=) closes every st_slide() of
            the module with one small line, in the app and in every HTML
            export (streamtex 0.7.70): a copyright line, a source. The note
            is a text or a leaf {"en": …, "fr": …} (the module's language);
            link= makes it a link to that marker, opened in a new tab so
            that the reader keeps the slide. It sits just under the slide
            box, in its bottom margin, and adds no height. A function
            instead of a text draws the note itself. st_slide_note() draws
            the same note on a page without st_slide(). Stored per session,
            like set_slide_container().
        """)
        st_space("v", 1)

        show_code("""\
# book.py — once, before st_book()
import streamtex as stx

stx.set_slide_note({"fr": "© 2026 … — lecture réservée aux participants",
                    "en": "© 2026 … — for the participants only"},
                   link="legal-notice")      # the key= of the legal notice's marker

stx.st_slide_note()                       # the same note, on a page without st_slide()
stx.marker_href("legal-notice")           # "?marker=legal-notice", app and exports alike
stx.set_slide_note(None)                  # no note""")
        st_space("v", 1)

        show_details("""\
            In the paginated HTML export, a link ?marker=, ?slide= or ?page=
            written in a page points at the entry file, which knows every
            page. marker_href() keeps the app's other parameters (?lang=).
        """)
        st_space("v", 2)

        st_write(bs.sub, "Several notes, placed by the designer — set_slide_notes()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            set_slide_notes(SlideNote(…), …) sets one or several notes
            (streamtex 0.7.72). Each has a place — in the slide (below,
            above, left, right in vertical text, across as a watermark),
            fixed on the screen (screen-top, screen-bottom, screen-left,
            screen-right) or in the presentation bar of the app
            (bar-after-title, bar-title, bar-before-counter) — a text per
            display mode (slides, document, html, phone, default; None = no
            note there), an opacity, a style, and a layer: under the content
            by default, so that a text placed over the note hides it, its
            link still clickable; over to draw it above.
        """)
        st_space("v", 1)

        show_code("""\
# book.py — once, before st_book()
import streamtex as stx

stx.set_slide_notes(
    stx.SlideNote({"slides": "© 2026 … — participants only",
                   "html": "© 2026 … — for the participants only; any other use by written permission",
                   "phone": "© 2026 …"},
                  place="below", link="legal-notice"),
    stx.SlideNote("© ACME", place="across"),                   # watermark, opacity 0.08
    stx.SlideNote("Legal notice", place="bar-before-counter", link="legal-notice"),
)""")
        st_space("v", 1)

        show_details("""\
            A slide place follows the box of SLIDE_CONTAINER (80vh high,
            10vh margins): under a slide taller than the screen it follows
            the box. A note fixed on the screen is drawn once per page, in
            every page file of the HTML export too; screen-left sits at the
            window's edge, under an open sidebar. The bar exists in the app
            only: pair a bar note with a screen note whose text is only for
            html. set_slide_note(text, link=) is the note
            SlideNote(text, place="below", opacity=1).

            Downloads (streamtex 0.7.73): downloads="always" (default),
            "never" or "choice" decides whether a note goes into a file
            downloaded from the app (Download as…, HTML and PDF); "choice"
            adds a box, ticked by default, to the panel. The PDF shows the
            pdf text of a note, else its html text. A new line in a text
            (written \\n in Python) starts a new line.
        """)
        st_space("v", 2)

        st_write(bs.sub, "Migrating a project's own slide() helper", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            A project that wrote its own slide(cut, style) helper — a break,
            then the design system's box — can retire it: st_slide() takes
            cut and style at the same positions with the same meaning. Two
            lines, no block file changes, no visual change.
        """)
        st_space("v", 1)

        show_code("""\
# shared/slides.py — the helper becomes an alias
from streamtex import st_slide as slide

# book.py — the box the helper used, once, before st_book()
import streamtex as stx
stx.set_slide_container(s.project.containers.slide_center)

# then, slide by slide, a marker written apart can move onto its slide:
#   st_marker("RAG")              →   with slide(marker="RAG"):
#   with slide():                          ...
#       ...""")
