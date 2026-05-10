"""Demo — evidence_insight composite slide template.

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Demo styles for evidence_insight."""
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
    """Dedicated demo for the evidence_insight composite template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — evidence_insight",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A composite template that fixes the order of four atomic
        patterns: **slide_heading -> stat_hero (or body) ->
        takeaways -> cite**. The reader's eye travels top-to-bottom
        through "headline + finding + what to remember + source".

        **When to use** — synthesis slides at the end of an
        evidence-heavy section. **When NOT to use** — single-stat
        slides without takeaways (use `stat_hero` alone),
        multi-source comparisons (use `comparison_table`).
    """)
    st_space("v", 2)

    # ---- Code skeleton ----
    st_write(bs.sub, "Code skeleton", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
def build():
    with st_block(s.project.containers.page_fill_top):
        with st_block(s.center_txt):
            # 1. slide_heading (with optional tooltip)
            with st_grid(cols="95% 5%", gap="0px",
                         cell_styles=...) as g:
                with g.cell():
                    with st_zoom(90):
                        st_write(bs.heading, "<Slide title>",
                                 tag=t.div, toc_lvl="+1")
                with g.cell():
                    st_hover_tooltip(...)

            st_space("v", 2)

            # 2. (optional) hero stat
            st_write(bs.stat, "<HERO STAT>")
            st_space("v", 1)

            # 3. (optional) one-paragraph body
            st_write(bs.body, "<Body explanation>")
            st_space("v", 2)

            # 4. takeaways (3-5 numbered insights)
            with st_zoom(110):
                with st_list(li_style=bs.body) as l:
                    for i, (lead, body) in enumerate(TAKEAWAYS, 1):
                        with l.item():
                            st_write(bs.body,
                                     (bs.label, f"{i}. {lead} "),
                                     (bs.body, f"-- {body}"))

            st_space("v", 2)
            st_write(bs.highlight, "<Punch line>")

        # 5. cite
        st_space("v", 1)
        st_write(bs.source, cite("<bib_key>"))""")
    st_space("v", 2)

    # ---- Live render ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Below is a faithful render of the five-section spine.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout + s.center_txt):
        # 1. slide_heading proxy
        st_write(bs.slide_title, "Evidence Synthesis", tag=t.div)
        st_space("v", 2)

        # 2. hero stat
        st_write(bs.stat, "7h")
        st_space("v", 1)

        # 3. body
        st_write(bs.body_c,
                 "Lost per team member weekly to AI inefficiencies.")
        st_space("v", 2)

        # 4. takeaways
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
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: composition order is fixed
        (heading -> stat/body -> takeaways -> cite); the slide
        presents **one** piece of evidence; citation is mandatory;
        the highlight punch line ends the slide and sets up the
        transition to the next concept.
    """)
    st_space("v", 1)
