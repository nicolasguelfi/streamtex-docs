"""Demo — narrative_transition slide template.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for narrative_transition."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    highlight = (
        s.large + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    placeholder = (
        s.center_txt
        + s.container.borders.dashed_border
        + s.container.paddings.large_padding
        + s.project.backgrounds.tip_bg
    )
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Dedicated demo for the narrative_transition slide template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — narrative_transition",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A bridge slide whose only job is to pivot the audience from
        "here is the problem we just established" to "here is the
        solution we are about to unfold". One rhetorical step, one
        visual anchor on the left, one pivot sentence on the right.

        **When to use** — end of an evidence section, between
        state-of-the-art and a method proposal, before introducing a
        named methodology. **When NOT to use** — content slides
        (the transition carries no data), conclusion slides (use
        `ptn_takeaways`), cover slides (use `ptn_title_slide`).
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Below: a faithful render of the layout. The logo on the left
        is replaced by a dashed placeholder so the demo runs without
        a project image; the pivot sentence on the right uses the
        `highlight` color and contains a `→` between the leaving and
        arriving concepts.
    """)
    st_space("v", 1)

    def _demo():
        with st_block(s.project.containers.tip_callout + s.center_txt):
            st_write(bs.slide_title, "The Methodological Gap",
                     tag=t.div)
            st_space("v", 2)

            with st_grid(cols="1fr 2fr", gap="24px",
                         cell_styles=bs.cell) as g:
                with g.cell():
                    with st_block(bs.placeholder):
                        st_write(s.large + s.center_txt + s.italic,
                                 "[ Logo / hero illustration "
                                 "of the destination ]")
                with g.cell():
                    st_write(
                        bs.highlight,
                        "Today: beyond VibeEngineering → "
                        "Generative SE as a discipline, "
                        "practiced through GSE-One",
                    )

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: image on the **left**, pivot sentence on the
        **right** (left-to-right reading order anchors the destination
        before the verbal claim); single `→` in the pivot sentence;
        `highlight` color (not `primary` or `accent`) signals
        "important transition"; the slide carries no data or citation
        — those belong in the slide *before* the transition (use
        `ptn_evidence_insight` for that).

        **Project specialisations**: when the destination is fixed for
        a whole collection (e.g. always GSE-One in `ai4se6d`), wrap
        the pattern as a project-local helper. See
        `projects/ai4se6d/ptn_transition_gse.md` for the canonical
        example.
    """)
    st_space("v", 1)
