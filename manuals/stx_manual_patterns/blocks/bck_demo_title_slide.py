"""Demo — ptn_title_slide template (image-dominant cover slide).

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import (
    show_explanation, show_details, show_and_run,
)


class BlockStyles:
    """Demo styles for ptn_title_slide."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    title = (
        s.huge + s.bold + s.project.colors.primary_violet + s.center_txt
    )
    subtitle = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    info = s.large + s.center_txt + s.project.colors.neutral_gray
    placeholder = (
        s.center_txt
        + s.container.borders.dashed_border
        + s.container.paddings.large_padding
        + s.project.backgrounds.tip_bg
    )


bs = BlockStyles


def build():
    """Dedicated demo for the ptn_title_slide template."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Demo — ptn_title_slide",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- What it is ----
    st_write(bs.sub, "What it is", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The opening slide of a session, course module, or major
        section. A center-aligned, image-dominant layout: huge
        primary-color title, an AI-generated hero image, two-line
        subtitle, and a small caption with session/author info.

        **When to use** — the very first slide of a presentation, or
        major chapter dividers. **When NOT to use** — sub-section
        dividers (use `ptn_slide_heading`), pure data slides (use
        `ptn_stat_hero`), conclusion slides (use `ptn_takeaways`).
    """)
    st_space("v", 2)

    # ---- Live render (code shown == code rendered) ----
    st_write(bs.sub, "Live render", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The AI hero image is replaced by a dashed placeholder so the
        demo runs without the AI provider configured.
    """)
    st_space("v", 1)

    def _demo():
        with st_block(s.project.containers.tip_callout + s.center_txt):
            st_write(bs.title, "AI for Software Engineering",
                     tag=t.div)
            st_space("v", 1)

            with st_block(bs.placeholder):
                st_write(s.large + s.center_txt + s.italic,
                         "[ AI hero illustration -- "
                         "1536x1024 landscape -- editable=True ]")
            st_space("v", 1)

            st_write(bs.subtitle,
                     "VibeEngineering: The Future of Software",
                     tag=t.div)
            st_write(bs.subtitle,
                     "Development with Generative AI", tag=t.div)
            st_space("v", 0.5)
            st_write(bs.info,
                     "Session 1 — DLH Luxembourg")

    show_and_run(_demo)
    st_space("v", 1)

    show_details("""\
        **INVARIANTS**: center-aligned layout, title uses
        `s.project.colors.primary` and `s.Huge`, AI hero image
        present and declared via a module-level `HERO_PROMPT` (never
        inlined), `IS_EDITABLE` flag wired so the user can regenerate
        the image, `toc_lvl="1"` on the title.
    """)
    st_space("v", 1)
