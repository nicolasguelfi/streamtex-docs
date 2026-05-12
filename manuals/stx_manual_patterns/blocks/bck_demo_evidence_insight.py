"""Demo — ptn_evidence_insight composite slide template.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for ptn_evidence_insight."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    stat = (
        s.Huge + s.bold + s.project.colors.primary_violet + s.center_txt
    )
    keyword = s.bold + s.project.colors.primary_violet
    label = s.bold + s.project.colors.primary_violet
    highlight = (
        s.large + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    source = s.large + s.italic + s.center_txt + s.project.colors.neutral_gray


bs = BlockStyles


TAKEAWAYS = [
    ("Gains are real but variable",
     "depends on experience, context, task complexity"),
    ("The methodology is the multiplier",
     "10% with tools -> 25-30% with process"),
    ("Senior expertise + structured process",
     "= where the real value is captured"),
]


def build():
    """Dedicated demo for the ptn_evidence_insight composite template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — ptn_evidence_insight",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A composite template that fixes the order of four atomic
        patterns: **ptn_slide_heading -> ptn_stat_hero (or body) ->
        ptn_takeaways -> cite**. The reader's eye travels top-to-bottom
        through "headline + finding + what to remember + source".

        **When to use** — synthesis slides at the end of an
        evidence-heavy section. **When NOT to use** — single-stat
        slides without takeaways (use `ptn_stat_hero` alone),
        multi-source comparisons (use `ptn_comparison_table`).
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    def _demo():
        with st_block(s.project.containers.tip_callout + s.center_txt):
            # 1. ptn_slide_heading proxy
            st_write(bs.slide_title, "Evidence Synthesis", tag=t.div)
            st_space("v", 2)

            # 2. hero stat
            st_write(bs.stat, "7h")
            st_space("v", 1)

            # 3. body
            st_write(bs.body_c,
                     "Lost per team member weekly to AI inefficiencies.")
            st_space("v", 2)

            # 4. ptn_takeaways
            with st_list(li_style=bs.body) as l:
                for i, (lead, body) in enumerate(TAKEAWAYS, start=1):
                    with l.item():
                        st_write(bs.body,
                                 (bs.label, f"{i}. {lead} "),
                                 (bs.body, f"— {body}"))
            st_space("v", 2)
            st_write(bs.highlight,
                     "This is why we need GSE-One.")

            # 5. cite
            st_space("v", 1)
            st_write(bs.source, "— GitLab DevSecOps Survey (2025)")

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: composition order is fixed
        (heading -> stat/body -> ptn_takeaways -> cite); the slide
        presents **one** piece of evidence; citation is mandatory;
        the highlight punch line ends the slide and sets up the
        transition to the next concept.
    """)
    st_space("v", 1)
