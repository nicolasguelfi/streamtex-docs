"""MarkerConfig Reference — complete field-by-field documentation.

Covers every MarkerConfig field (defaults read from the library at render
time), documents vs decks, the "second navigation stop" warning, modifier
key syntax, a full book.py example, keyboard safety notes and NumberingMode.
"""

import dataclasses

from streamtex import (
    MarkerConfig, MarkerRoles, st_write, st_block, st_space,
)
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """MarkerConfig reference styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    field_name = s.bold + s.large
    field_desc = s.large


bs = BlockStyles

#: field -> (type, description); the default is read from MarkerConfig itself.
_FIELDS = {
    "show_nav_ui": (
        "bool",
        "Show the floating navigation widget (counter, ◀ ▶ buttons, ☰ popup, label). "
        "The sidebar offers the same switch to the reader."),
    "auto_marker_on_toc": (
        "bool | int",
        "Which TOC heading levels get a marker automatically: True = all levels, "
        "N = levels 1 to N, False (or 0) = none. For documents, where the headings "
        "give the stops; 0 in a deck."),
    "toc_marker_roles": (
        "MarkerRoles | dict[int, MarkerRoles]",
        "Roles of those automatic heading markers: one MarkerRoles for every level, "
        "or a dict level → MarkerRoles (missing levels: MarkerRoles.NAMED). "
        "A toc_lvl inside is ignored: the heading decides its level."),
    "nav_position": (
        "str",
        'Widget position: "bottom-right" or "bottom-center".'),
    "nav_label_chars": (
        "int",
        "Max characters of the current marker's label in the widget; 0 hides it. "
        "An unlisted marker without a label of its own shows its section."),
    "popup_open": (
        "bool",
        "Initial state of the ☰ popup (the list of listed markers)."),
    "next_keys": (
        "list[str]",
        "Keys that go to the next stop. Supports modifier syntax (see below)."),
    "prev_keys": (
        "list[str]",
        "Keys that go to the previous stop. Supports modifier syntax (see below)."),
    "draggable": (
        "bool",
        "Let the reader drag the widget anywhere on screen (mouse and touch). "
        "The position is kept in localStorage."),
    "collapsible": (
        "bool",
        "Show a ⋮ button that collapses / expands the widget. "
        "The collapsed state is kept in localStorage."),
    "scroll_offset": (
        "int",
        "Pixels left above a marker when navigation scrolls to it (also the CSS "
        "scroll-margin-top of marker anchors), room for a header or a toolbar. "
        "0 for a deck whose slides fill the viewport."),
}


def _default_text(f: dataclasses.Field) -> str:
    """The default of a MarkerConfig field, as one would write it."""
    if f.default is not dataclasses.MISSING:
        value = f.default
    elif f.default_factory is not dataclasses.MISSING:
        value = f.default_factory()
    else:
        return "(required)"
    if isinstance(value, MarkerRoles):
        for name in ("NAMED", "HIDDEN", "ANCHOR"):
            if value == getattr(MarkerRoles, name):
                return f"MarkerRoles.{name}"
    return repr(value).replace("'", '"')


def build():
    st_write(bs.heading, "MarkerConfig Reference", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        MarkerConfig is a dataclass that controls the marker navigation
        system. Pass it to st_book() via the marker_config= parameter;
        without it, a book has no markers at all.

        All fields have defaults — you only set what you want to change.
        The defaults below are read from the library while this page
        renders.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Field reference — defaults read from the dataclass
    # ------------------------------------------------------------------
    st_write(bs.sub, "Field Reference", toc_lvl="+1")
    st_space("v", 1)

    for f in dataclasses.fields(MarkerConfig):
        type_str, desc = _FIELDS.get(f.name, ("", "(not documented here yet)"))
        _field_row(f.name, type_str, _default_text(f), desc)

    st_space("v", 2)

    # ------------------------------------------------------------------
    # Documents and decks
    # ------------------------------------------------------------------
    st_write(bs.sub, "Documents and Decks — One Way per Book", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A book takes its stops from one source. A **document** takes them
        from its headings: auto_marker_on_toc=1 (or more), no slide breaks
        with markers. A **deck** takes one stop per slide from the slide's
        own marker — st_slide(marker=...), the break's marker, or an
        st_marker() at the head of the slide — keeps auto_marker_on_toc=0,
        and links a heading to its slide with st_write(..., marker="attach").
    """)
    st_space("v", 1)

    show_code("""\
# book.py of a document — the headings give the stops
marker_config = MarkerConfig(auto_marker_on_toc=1)

# book.py of a deck — one stop per slide, slides fill the viewport
marker_config = MarkerConfig(auto_marker_on_toc=0, scroll_offset=0)

# a slide of the deck
with st_slide(cut=True, marker="Prompt patterns"):        # the slide's stop, listed
    st_write(bs.title, "Prompt patterns", toc_lvl="2", marker="attach")""")
    st_space("v", 1)

    show_details("""\
        **The "second navigation stop" warning.** When a slide opened by
        st_slide_break() or st_slide() already has its stop and an automatic
        heading marker (auto_marker_on_toc) would add a second stop to it,
        the library warns, naming both:

        The heading 'Prompt patterns' adds a second navigation stop to a
        slide that already has one ('Marker 12'): write marker="attach" to
        link the heading to the slide, or marker=False (or
        auto_marker_on_toc=0 in a deck).

        The book mixes heading stops (documents) with slide stops (decks).
        Nothing is merged behind your back: the heading still gets its
        stop, and the reader presses ▶ twice on that slide until you follow
        the advice. A heading with an explicit marker= never triggers it.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Modifier key syntax
    # ------------------------------------------------------------------
    st_write(bs.sub, "Keyboard Modifier Syntax", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
        "Key definitions use the JavaScript ", (s.bold, "KeyboardEvent.key"),
        " values. Combine a modifier with a key using the ", (s.bold, "+"), " separator:",
    )
    st_space("v", 1)

    show_code("""\
# Single keys
next_keys=["PageDown", "ArrowRight"]

# With modifiers: Ctrl, Shift, Alt, Meta (Cmd on macOS)
next_keys=["PageDown", "Ctrl+ArrowRight"]
prev_keys=["PageUp", "Ctrl+ArrowLeft"]

# Multiple modifiers are NOT chained — use one modifier per entry""")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Complete example
    # ------------------------------------------------------------------
    st_write(bs.sub, "Complete Example in book.py", toc_lvl="+1")
    st_space("v", 1)

    show_code(file="examples/nav/marker_config_complete.py")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Keyboard safety
    # ------------------------------------------------------------------
    st_write(bs.sub, "Keyboard Safety", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        The keyboard handler automatically ignores key presses when
        the focus is on an input, textarea, select, or contentEditable
        element. This prevents marker navigation from interfering
        with form fields and text editing.

        Pressing Escape while the popup is open closes it without
        triggering any navigation.

        When search=True in TOCConfig, sidebar search filters marker
        entries alongside TOC entries — only markers from blocks
        matching the query are displayed.
    """)
    st_space("v", 3)

    # ------------------------------------------------------------------
    # NumberingMode reference
    # ------------------------------------------------------------------
    st_write(bs.sub, "NumberingMode Enum Reference", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        NumberingMode controls where TOC heading numbers are displayed.
        Set via TOCConfig(numbering=NumberingMode.XXX).
    """)
    st_space("v", 1)

    show_code("""\
from streamtex import NumberingMode, TOCConfig

# BOTH — numbers in the sidebar and inline in the content (default)
toc = TOCConfig(numbering=NumberingMode.BOTH)

# SIDEBAR_ONLY — numbers only in the sidebar TOC
toc = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY)

# MAIN_ONLY — numbers only in the content
toc = TOCConfig(numbering=NumberingMode.MAIN_ONLY)

# NONE — no numbering anywhere
toc = TOCConfig(numbering=NumberingMode.NONE)""")
    st_space("v", 1)

    show_details("""\
        BOTH is the TOCConfig default. SIDEBAR_ONLY is the usual choice
        for manuals (this one uses it): the content stays free of numbers.

        BOTH suits formal documents where section numbers should be
        visible in the rendered content.

        NONE disables numbering entirely (useful for single-page docs).
    """)


def _field_row(name: str, type_str: str, default: str, desc: str):
    """Render a single field documentation row."""
    with st_block(s.project.containers.explanation_box):
        st_write(bs.field_name, f"{name}")
        st_write(s.large,
                 (s.bold, "Type: "), f"{type_str}  —  ",
                 (s.bold, "Default: "), f"{default}")
        st_write(bs.field_desc, desc)
