"""Gallery — atomic patterns: slide_heading, cite, inline_emphasis.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_and_run


class BlockStyles:
    """Atoms gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    highlight = s.bold + s.project.colors.highlight_amber
    label = s.bold + s.project.colors.primary_violet + s.center_txt
    slide_title = (
        s.Large + s.bold + s.project.colors.accent_teal + s.center_txt
    )
    source = (
        s.large + s.italic + s.center_txt + s.project.colors.neutral_gray
    )
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Compact gallery of three atomic patterns."""
    with st_block(s.center_txt):
        st_write(bs.heading,
                 "Atoms Gallery — slide_heading, cite, inline_emphasis",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    show_explanation("""\
        Three small but pervasive atoms used across StreamTeX
        presentation projects. They appear in nearly every content
        slide. Each entry below shows what the pattern does and renders
        it live, with the *exact same code* shown above the render.
    """)
    st_space("v", 2)

    # ---- slide_heading ----
    st_write(bs.sub, "slide_heading — title row + tooltip", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A 95% / 5% grid: a centered slide title on the left and a
        small marker on the right (placeholder for the presenter's
        hover tooltip). Below: code shown == code rendered.
    """)
    st_space("v", 1)

    def _demo_slide_heading():
        with st_grid(cols="95% 5%", gap="0px",
                     cell_styles=bs.cell) as g:
            with g.cell():
                st_write(bs.slide_title,
                         "Evidence Synthesis — METR Paradox",
                         tag=t.div)
            with g.cell():
                st_write(s.large + s.center_txt, (bs.keyword, "?"))

    show_and_run(_demo_slide_heading)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_slide_heading.md"),
             (bs.accent, " for full details."))
    st_space("v", 2)

    # ---- cite ----
    st_write(bs.sub, "cite — source attribution footer", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A small italic centered citation footer placed under stats,
        quotes, or claims. Real usage wires it to the project's BibTeX
        file via `streamtex.bib.cite("<bib_key>")`. The demo below
        renders a static string so the gallery has no external
        dependency.
    """)
    st_space("v", 1)

    def _demo_cite():
        st_write(bs.body_c, "GenAI tools made developers ",
                 (bs.keyword, "19% slower"),
                 " on real-world tasks.")
        st_space("v", 0.5)
        st_write(bs.source, "— METR (2025), arXiv:2507.09089")

    show_and_run(_demo_cite)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_cite.md"),
             (bs.accent, " for full details."))
    st_space("v", 2)

    # ---- inline_emphasis ----
    st_write(bs.sub,
             "inline_emphasis — keyword / accent / highlight",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A trio of inline tuple styles for mixing emphasised fragments
        inside a single `st_write` call. Each variant carries
        **semantic meaning**, not just color: `keyword` (primary
        term), `accent` (tool / identifier), `highlight` (paradox /
        warning fact).
    """)
    st_space("v", 1)

    def _demo_inline_emphasis():
        with st_block(s.project.containers.result_box):
            st_write(bs.body,
                     "Predicted AI would make them ",
                     (bs.keyword, "24% faster"),
                     ", but they were ",
                     (bs.highlight, "actually 19% slower"),
                     ".")

    show_and_run(_demo_inline_emphasis)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_inline_emphasis.md"),
             (bs.accent, " for full details."))
    st_space("v", 1)
