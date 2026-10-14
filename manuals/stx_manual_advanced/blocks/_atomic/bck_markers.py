"""Marker Navigation — the three roles of a marker and how to place one.

Covers: the three independent roles (stop, listed, in TOC), the eight
combinations and their MarkerRoles values, st_marker(stop=, listed=,
toc_lvl=, roles=, hidden=, visible=, key=), unlabelled markers, the
heading markers of st_write(marker=...) including "attach" for decks.

The tables of this page are computed by the library while the page
renders (roles, errors, registry entries): they cannot drift from it.
"""

from streamtex import (
    MarkerRoles, st_block, st_grid, st_list, st_marker, st_space, st_write,
)
from streamtex.enums import Tags as t
from streamtex.marker import marker_count, marker_entries, resolve_marker_roles
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Marker chapter styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    feature = s.project.titles.feature_title
    cell = (s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout)
    head = s.bold + s.big
    text = s.big
    code = s.text.fonts.font_monospace + s.medium
    mark = s.big + s.center_txt


bs = BlockStyles

#: The eight combinations: the call, its keywords (label apart), a typical use.
_COMBINATIONS = [
    ('st_marker("X")', {"label": "X"},
     "A named waypoint (the default)"),
    ('st_marker("X", hidden=True)', {"label": "X", "hidden": True},
     "A slide's own stop; the break markers"),
    ('st_marker("Part B", stop=False)', {"label": "Part B", "stop": False},
     "A list entry inside a scrolling slide: no arrow press"),
    ('st_marker(key="exercise-3", stop=False, listed=False)',
     {"stop": False, "listed": False},
     "An anchor kept for a deep link only"),
    ('st_marker("Prompting", toc_lvl="1")', {"label": "Prompting", "toc_lvl": "1"},
     "A TOC entry with its stop and its row, no heading drawn"),
    ('st_marker("X", hidden=True, toc_lvl="2")',
     {"label": "X", "hidden": True, "toc_lvl": "2"},
     "A TOC entry and a stop, out of the list"),
    ('st_marker("Part B", stop=False, toc_lvl="+1")',
     {"label": "Part B", "stop": False, "toc_lvl": "+1"},
     "A TOC entry and a row, no arrow press"),
    ('st_marker("Annex", stop=False, listed=False, toc_lvl="1")',
     {"label": "Annex", "stop": False, "listed": False, "toc_lvl": "1"},
     "A TOC entry only"),
]

#: Contradictory calls: st_marker raises before placing anything.
_RULES = [
    ('st_marker("X", hidden=True, listed=True)', {"label": "X", "hidden": True, "listed": True}),
    ('st_marker("X", hidden=True, stop=False)', {"label": "X", "hidden": True, "stop": False}),
    ('st_marker("X", hidden=False, listed=False)', {"label": "X", "hidden": False, "listed": False}),
    ('st_marker("X", roles=MarkerRoles.HIDDEN, stop=True)',
     {"label": "X", "roles": MarkerRoles.HIDDEN, "stop": True}),
    ('st_marker(toc_lvl="1")', {"toc_lvl": "1"}),
]


def _yes(flag: bool) -> str:
    return "✓" if flag else "–"


def _roles_value(r: MarkerRoles) -> str:
    """The MarkerRoles value to pass as roles=, by its constant name when it has one."""
    for name in ("NAMED", "HIDDEN", "ANCHOR"):
        if r == getattr(MarkerRoles, name):
            return f"roles=MarkerRoles.{name}"
    args = []
    if not r.stop:
        args.append("stop=False")
    if not r.listed:
        args.append("listed=False")
    if r.toc_lvl is not None:
        args.append(f'toc_lvl="{r.toc_lvl}"')
    return f"roles=MarkerRoles({', '.join(args)})"


def _registry_table(entries: list[dict]) -> None:
    """The registry entries this page just placed: label and roles."""
    if not entries:
        st_write(bs.text, "(No marker registered on this pass: markers are off in this book.)")
        return
    with st_grid(cols="2fr 1fr 1fr 1fr", cell_styles=bs.cell) as g:
        for title in ("label", "stop", "listed", "in TOC"):
            with g.cell():
                st_write(bs.head, title)
        for e in entries:
            with g.cell():
                st_write(bs.text, e.get("label", ""))
            for flag in (e.get("stop", True), e.get("listed", True), e.get("toc", False)):
                with g.cell():
                    st_write(bs.mark, _yes(flag))


def build():
    st_write(bs.heading, "Marker Navigation", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        A marker is a named point in the content. The floating navigation
        widget, the keys (PageDown / PageUp by default), the ☰ popup, the
        sidebar Markers tab and the TOC all read markers, each through one
        of the marker's **three independent roles**.

        Markers work in continuous and paginated books and in the HTML
        export.
    """)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The three roles
    # ------------------------------------------------------------------
    st_write(bs.sub, "Three Roles per Marker", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, (s.bold, "stop"),
                         " — the ◀ ▶ buttons, the keys and the counter n / N stop here. "
                         "Stops are the slides of the book: N is the number of stops.")
            with l.item():
                st_write(s.large, (s.bold, "listed"),
                         " — the marker is a row of the ☰ popup and of the sidebar "
                         "Markers tab, and can name a paginated page.")
            with l.item():
                st_write(s.large, (s.bold, "in TOC"),
                         " — the marker is linked to a table-of-contents entry; "
                         "the TOC marks an entry linked to a stop with a ●.")
        st_write(s.large, "Whatever its roles, every marker keeps its anchor and its "
                          "deep link (?marker=…).")
    st_space("v", 2)

    # ------------------------------------------------------------------
    # The eight combinations — computed by the library
    # ------------------------------------------------------------------
    st_write(bs.sub, "The Eight Combinations", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, """\
        All eight combinations are valid. One value object, MarkerRoles,
        carries the three roles; three of them have a name: MarkerRoles.NAMED
        (stop, listed), MarkerRoles.HIDDEN (stop, not listed) and
        MarkerRoles.ANCHOR (neither). The roles below are resolved by the
        library from each call while this page renders.
    """, breaks=False)
    st_space("v", 1)

    with st_grid(cols="auto auto auto 2fr 1.3fr", cell_styles=bs.cell) as g:
        for title in ("stop", "listed", "in TOC", "call  ·  roles= value", "typical use"):
            with g.cell():
                st_write(bs.head, title)
        for call, kwargs, use in _COMBINATIONS:
            role_kw = {k: v for k, v in kwargs.items() if k != "label"}
            r = resolve_marker_roles(**role_kw)
            for flag in (r.stop, r.listed, r.toc_lvl is not None):
                with g.cell():
                    st_write(bs.mark, _yes(flag))
            with g.cell():
                st_write(bs.code, call)
                st_write(bs.code + s.project.colors.neutral_gray, _roles_value(r))
            with g.cell():
                st_write(bs.text, use)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # st_marker()
    # ------------------------------------------------------------------
    st_write(bs.sub, "Placing a Marker — st_marker()", toc_lvl="+1")
    st_space("v", 1)

    show_code('''\
from streamtex import st_marker, MarkerRoles

st_marker("Invisible Waypoint")                 # stop + listed; nothing drawn
st_marker("Section Start", visible=True)        # the same roles, drawn as a dashed line
st_marker("Slide 4", hidden=True)               # stop, NOT listed (shortcut)
st_marker("Part B", stop=False)                 # listed, no arrow press
st_marker("Prompting", toc_lvl="1")             # + a TOC entry at level 1
st_marker("Electricity", key="electricity")     # stable deep-link key
st_marker("X", roles=MarkerRoles(listed=False, toc_lvl="2"))  # all roles at once''')
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, (s.bold, "stop= / listed="),
                         " default to True. ", (s.bold, "hidden=True"),
                         " is the shortcut for a stop that is not listed; hidden=False means listed.")
            with l.item():
                st_write(s.large, (s.bold, "toc_lvl="),
                         " registers a TOC entry at that level (\"1\", \"+1\", \"-1\"… as "
                         "st_write) and the marker takes its anchor, so the TOC link and the "
                         "marker share one target. No heading is drawn, and a label is required.")
            with l.item():
                st_write(s.large, (s.bold, "roles="),
                         " gives the three roles at once as a MarkerRoles; it excludes "
                         "hidden=, stop=, listed= and toc_lvl=.")
            with l.item():
                st_write(s.large, (s.bold, "visible=True"),
                         " only draws a dashed line with the label in the content. It has "
                         "nothing to do with listed: a listed marker is invisible by default, "
                         "and an unlisted one can be drawn.")
            with l.item():
                st_write(s.large, (s.bold, "key="),
                         " a stable identifier for ?marker=<key>, independent of the label "
                         "(it survives a translation); without it the deep link uses the "
                         "label's slug.")
    st_space("v", 1)

    show_details("""\
        **Unlabelled markers.** st_marker() without a label gets a generated
        label, "Marker N". A listed one shows that label in the popup. An
        unlisted one — every stop placed by st_slide_break() — never shows
        "Marker N": the widget shows the current section instead, the label
        of the last listed marker before it. A TOC heading attached to an
        unlabelled marker (marker="attach", below) gives it its label.
    """)
    st_space("v", 1)

    st_write(bs.feature, "Contradictions raise (executed here):")
    st_space("v", 1)
    with st_grid(cols="1fr 1.4fr", cell_styles=bs.cell) as g:
        for call, kwargs in _RULES:
            try:
                st_marker(**kwargs)
                outcome = "accepted"
            except (TypeError, ValueError) as exc:
                outcome = f"{type(exc).__name__}: {exc}"
            with g.cell():
                st_write(bs.code, call)
            with g.cell():
                st_write(bs.code, outcome)
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Live demo — four markers on this page
    # ------------------------------------------------------------------
    st_write(bs.sub, "Live Demo — Markers on This Page", toc_lvl="+1")
    st_space("v", 1)

    show_code('''\
# stop, listed, drawn
st_marker("Visible Marker Demo", visible=True)
# stop, listed, not drawn
st_marker("Invisible Waypoint")
# listed only, drawn
st_marker("List entry, no stop", stop=False, visible=True)
# anchor only
st_marker("Anchor only", key="markers-demo-anchor", stop=False, listed=False)''')
    st_space("v", 1)

    first = marker_count()
    st_marker("Visible Marker Demo", visible=True)
    st_marker("Invisible Waypoint")
    st_marker("List entry, no stop", stop=False, visible=True)
    st_marker("Anchor only", key="markers-demo-anchor", stop=False, listed=False)
    st_space("v", 1)

    st_write(s.large, """\
        Two of them are stops: ▶ lands on each, and the counter counts them.
        Three are listed: open ☰ to find them. The last one has no role
        but its anchor: ?marker=markers-demo-anchor still opens it. What the
        marker registry recorded for them, read while this page rendered:
    """, breaks=False)
    st_space("v", 1)
    _registry_table(marker_entries()[first:])
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Headings — st_write(marker=)
    # ------------------------------------------------------------------
    st_write(bs.sub, "Heading Markers — st_write(marker=)", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, """\
        A TOC heading (st_write with toc_lvl) can carry a marker. Its
        marker= parameter takes five values:
    """, breaks=False)
    st_space("v", 1)

    with st_block(s.project.containers.explanation_box):
        with st_list(list_type="ul", l_style=s.large, li_style=s.large) as l:
            with l.item():
                st_write(s.large, (s.bold, "None"),
                         " (default) — a marker when MarkerConfig.auto_marker_on_toc covers the "
                         "heading's level, with the roles of MarkerConfig.toc_marker_roles; "
                         "otherwise none.")
            with l.item():
                st_write(s.large, (s.bold, "True"),
                         " — the heading declares its own stop, listed (MarkerRoles.NAMED), "
                         "even when auto_marker_on_toc is off.")
            with l.item():
                st_write(s.large, (s.bold, "False"),
                         " — no marker (an appendix, an index).")
            with l.item():
                st_write(s.large, (s.bold, "MarkerRoles(...)"),
                         " — the heading's own marker with exactly these roles, plus in TOC "
                         "(e.g. MarkerRoles.HIDDEN: a TOC entry and a stop, not listed). "
                         "Leave its toc_lvl unset: the heading decides the level (ValueError otherwise).")
            with l.item():
                st_write(s.large, (s.bold, "\"attach\""),
                         " — no new marker: the TOC entry is linked to the marker that opens "
                         "the slide, which keeps its roles. One stop per slide, as a deck needs.")
    st_space("v", 1)

    show_code("""\
# A document: the headings give the stops (MarkerConfig(auto_marker_on_toc=1))
st_write(s.huge, "Appendix", toc_lvl="1", marker=False)              # no marker
st_write(s.huge, "Important", toc_lvl="2", marker=True)              # its own listed stop
st_write(s.huge, "Detail", toc_lvl="2", marker=MarkerRoles.HIDDEN)   # TOC + stop, not listed

# A deck: the slide has its stop, the heading is linked to it
st_marker("Prompt patterns", hidden=True)                            # the slide's stop
st_write(bs.title, "Prompt patterns", toc_lvl="2", marker="attach")  # one stop, in the TOC""")
    st_space("v", 1)

    show_details("""\
        **What "attach" links to.** The most recent marker, if it was placed
        in the current slide by st_marker(), st_slide() or a break, and is
        not in the TOC yet. A slide begins with each book entry, each
        st_slide_break() and each st_slide(). The marker gains the in-TOC
        role and the heading's anchor leads to it (?marker= and #anchor
        links too); a generated label is replaced by the heading's.

        **Warnings.** "attach" with nothing to link to warns
        (st_write(marker='attach'): no marker opens the slide of …) and the
        heading gets its own marker, with the roles of toc_marker_roles. Any
        marker= given without toc_lvl warns that it has no effect: only a
        TOC heading carries a marker. An automatic heading stop added to a
        slide that already has one warns too — see "Documents and decks"
        in the MarkerConfig Reference chapter.
    """)
    st_space("v", 1)

    st_write(bs.feature, "Live: a heading attached to its stop")
    st_space("v", 1)
    show_code("""\
# an unlabelled stop, not listed
st_marker(hidden=True)
# the heading: no marker of its own, linked to the stop above
st_write(bs.feature, "Attached Heading Demo", toc_lvl="+1", marker="attach")""")
    st_space("v", 1)

    first = marker_count()
    st_marker(hidden=True)
    st_write(bs.feature, "Attached Heading Demo", toc_lvl="+1", marker="attach")
    st_space("v", 1)
    st_write(s.large, """\
        One entry, not two: the stop placed by st_marker() took the
        heading's label and the in-TOC role (its sidebar entry shows the ●).
    """, breaks=False)
    st_space("v", 1)
    _registry_table(marker_entries()[first:])
    st_space("v", 2)

    # ------------------------------------------------------------------
    # Automatic heading markers
    # ------------------------------------------------------------------
    st_write(bs.sub, "Automatic Heading Markers", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large, """\
        auto_marker_on_toc decides which heading levels get a marker;
        toc_marker_roles decides their roles, for every level or per level:
    """, breaks=False)
    st_space("v", 1)

    show_code(file="examples/nav/marker_auto_toc.py")
    st_space("v", 1)

    show_code("""\
from streamtex import MarkerConfig, MarkerRoles

# Level-1 headings listed, level-2 headings stops but not listed
cfg = MarkerConfig(
    auto_marker_on_toc=2,
    toc_marker_roles={1: MarkerRoles.NAMED, 2: MarkerRoles.HIDDEN},
)""")
    st_space("v", 1)

    show_details("""\
        **Markers of an included block.** st_include(block, markers=False)
        keeps the anchors of the markers an included block places but
        removes their stop and listed roles; markers="hidden" keeps the
        stops out of the list. The "Composing by Atoms" chapter shows
        when a host slide needs it.
    """)
