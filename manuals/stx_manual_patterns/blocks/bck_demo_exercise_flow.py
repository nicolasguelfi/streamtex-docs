"""Demo — exercise_flow multi-slide template (briefing / action / debrief).

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for exercise_flow."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    accent = (
        s.large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    keyword = s.bold + s.project.colors.primary_violet
    instruction = (
        s.huge + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    timer = (
        s.huge + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    slide_label = (
        s.large + s.bold + s.project.colors.primary_violet + s.center_txt
    )
    slide_box = (
        s.container.borders.solid_border
        + s.container.paddings.medium_padding
        + s.container.layouts.vertical_center_layout
        + s.center_txt
    )


bs = BlockStyles


def build():
    """Dedicated demo for the exercise_flow multi-slide template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — exercise_flow",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A multi-slide template for a timed workshop exercise. Each
        instance produces **three slides** separated by
        `st_slide_break`:

        - **Briefing** — what the exercise is, why it matters,
          instructions, time budget.
        - **Action** — a minimal slide with a single instruction
          line and a big timer; intentionally near-empty so the
          audience focuses on doing.
        - **Debrief** — a question (callout) plus typical
          observations, optional takeaways.

        Typically used for `practice_pN` series in workshop modules.
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render — three layouts side by side",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The three slides are rendered side-by-side as compact previews
        for documentation purposes. Real usage inserts
        `st_slide_break` between each, producing one slide per page in
        paginated mode.
    """)
    st_space("v", 1)

    def _demo():
        with st_grid(cols="1fr 1fr 1fr", gap="16px",
                     cell_styles=bs.slide_box) as g:
            # Slide 1: Briefing
            with g.cell():
                st_write(bs.slide_label, "1. Briefing")
                st_space("v", 0.5)
                st_write(bs.slide_title, "Practice 1: Vibecoding clinic",
                         tag=t.div)
                st_space("v", 0.5)
                st_write(bs.body_c,
                         (bs.keyword, "1. Install Cursor"),
                         " from cursor.sh")
                st_write(bs.body_c,
                         (bs.keyword, "2. Open the demo repo"),
                         " in `.cursor` mode")
                st_write(bs.body_c,
                         (bs.keyword, "3. Run the agent"),
                         " on the failing test")
                st_space("v", 0.5)
                st_write(bs.accent, "Time: 30 minutes")

            # Slide 2: Action
            with g.cell():
                st_write(bs.slide_label, "2. Action")
                st_space("v", 0.5)
                st_write(bs.instruction,
                         "Follow the agent.")
                st_space("v", 0.5)
                st_write(bs.body_c,
                         "Note what surprises you.")
                st_space("v", 1)
                st_write(bs.timer, "30 min")

            # Slide 3: Debrief
            with g.cell():
                st_write(bs.slide_label, "3. Debrief")
                st_space("v", 0.5)
                st_write(bs.slide_title, "Debrief — Practice 1",
                         tag=t.div)
                st_space("v", 0.5)
                with st_block(s.project.containers.tip_callout):
                    st_write(bs.accent, "What did you notice?")
                st_space("v", 0.5)
                st_write(bs.body_c, (bs.keyword, "Speed"),
                         " — felt fast, was it really?")
                st_write(bs.body_c, (bs.keyword, "Trust"),
                         " — when did you check?")
                st_write(bs.body_c, (bs.keyword, "Surprise"),
                         " — what didn't work?")

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: three slides separated by `st_slide_break`;
        the briefing always names the time budget; the action slide
        is **minimal** (1 instruction + 1 timer); the debrief opens
        with a question callout. Never collapse the three slides into
        one — the workshop tempo depends on the dedicated slides.
    """)
    st_space("v", 1)
