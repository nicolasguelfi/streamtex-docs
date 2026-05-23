"""Hover Tooltip widget — inline icon revealing a term/definition panel."""

from streamtex import *
from streamtex.enums import Tags as t

from blocks.helpers import show_code, show_explanation
from custom.styles import Styles as s


class BlockStyles:
    """Styles for the hover tooltip demo."""

    heading = s.project.titles.section_title + s.center_txt
    section = s.project.titles.section_subtitle
    inline = s.large


bs = BlockStyles


def build():
    """Demonstrate st_hover_tooltip: inline icon → reveal-on-hover panel."""

    st_write(bs.heading, "Hover Tooltip", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""
        `st_hover_tooltip` renders a small inline icon that reveals a panel
        of term / definition pairs on `:hover`. It enables the
        **"telegraphic slide + detail-on-hover"** pattern — keep the slide
        sparse, keep the definitions one gesture away. Palette-neutral,
        scales via a single `scale` parameter, and routes through `st_html`
        so it survives HTML/PDF export.
    """)
    st_space("v", 2)

    # Live demo (rendered)
    st_write(bs.section, "Live demo", toc_lvl="+1")
    st_space("v", 1)

    st_write(
        bs.inline,
        "Hover the icon to reveal a definition panel: ",
    )
    st_hover_tooltip(
        icon="💡",
        title="Reuse architecture — key terms",
        entries=[
            ("Pack", "Python package shipping reusable visual components."),
            ("Component", "A reusable rendering function with a typed contract."),
            ("DS", "Design system — tokens + bundles selectable per project."),
            ("Kit", "Bundle of components + DS choices applied together."),
        ],
        scale="1.2vw",
    )

    st_space("v", 3)

    # Code example
    st_write(bs.section, "Code", toc_lvl="+1")
    st_space("v", 1)

    show_code("""
        from streamtex import st_hover_tooltip

        st_hover_tooltip(
            icon="💡",
            title="Reuse architecture — key terms",
            entries=[
                ("Pack", "Python package shipping reusable visual components."),
                ("Component", "A reusable rendering function with a typed contract."),
                ("DS", "Design system — tokens + bundles selectable per project."),
                ("Kit", "Bundle of components + DS choices applied together."),
            ],
            scale="1.2vw",
        )
    """, language="python")

    st_space("v", 2)

    # When to use
    st_write(bs.section, "When to use", toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.medium,
                "Dense projection slides where extra prose would crowd the layout.",
            )
        with l.item():
            st_write(
                s.medium,
                "Reference cards / glossaries where the term is the headline ",
                "and the definition is optional.",
            )
        with l.item():
            st_write(
                s.medium,
                "Auditorium presentations: the panel opens on the side ",
                "opposite the icon so it never leaves the visible area.",
            )

    st_space("v", 2)

    # Key parameters
    st_write(bs.section, "Key parameters", toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "icon"),
                " — any character or emoji (default `ℹ️`).",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "scale"),
                " — base font unit (default `1.8vw`). Title is 1.3×, ",
                "term 1.1×, definition 1.0×. Bigger `scale` = bigger panel.",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "position"),
                " — `left` | `center` | `right` (default `center`). ",
                "The panel opens on the side opposite the icon.",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "direction"),
                " — `up` | `down` (default `down`). Whether the panel ",
                "opens above or below the icon.",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "max_height"),
                " — internal scrollbar above this height (default `80vh`).",
            )

    st_space("v", 3)
