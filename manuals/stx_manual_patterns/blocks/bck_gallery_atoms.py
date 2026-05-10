"""Gallery — atomic patterns: slide_heading, cite, inline_emphasis.

# @pattern: manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Atoms gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    highlight = s.bold + s.project.colors.highlight_amber
    label = s.bold + s.project.colors.primary_violet + s.center_txt
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
        st_write(bs.heading, "Atoms Gallery — slide_heading, cite, inline_emphasis",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    show_explanation("""\
        Three small but pervasive atoms used across the `ai4se6d`
        corpus. They appear in nearly every content slide. Each entry
        below shows what the pattern does, the smallest meaningful
        skeleton, and a pointer to its full markdown file.
    """)
    st_space("v", 2)

    # ---- slide_heading ----
    st_write(bs.sub, "slide_heading — title row + tooltip", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A 95% / 5% grid: a centered slide title on the left and a
        small hover-tooltip icon on the right (presenter notes
        revealed on hover). Used on roughly **54 slides** of the
        `ai4se6d` corpus.
    """)
    st_space("v", 1)

    show_code("""\
with st_grid(cols="95% 5%", gap="0px",
             cell_styles=s.project.containers.grid_cell_centered) as g:
    with g.cell():
        with st_zoom(90):
            st_write(bs.heading, "<Slide title>",
                     tag=t.div, toc_lvl="+1")
    with g.cell():
        st_hover_tooltip(title="<Note>",
                         entries=[("Label", "Body")],
                         scale="2vw", width="70vw", position="left")""")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/slide_heading.md"),
             (bs.accent, " for full details."))
    st_space("v", 2)

    # ---- cite ----
    st_write(bs.sub, "cite — source attribution footer", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A small italic centered citation footer placed under stats,
        quotes, or claims. Backed by the project's BibTeX file via
        `streamtex.bib.cite`. About **55 blocks** of the corpus
        import the helper.
    """)
    st_space("v", 1)

    show_code("""\
from streamtex.bib import cite

class BlockStyles:
    source = s.project.citation + s.large + s.center_txt

st_write(bs.source, cite("<bib_key>"))""")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/cite.md"),
             (bs.accent, " for full details."))
    st_space("v", 2)

    # ---- inline_emphasis ----
    st_write(bs.sub, "inline_emphasis — keyword / accent / highlight", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A trio of inline tuple styles for mixing emphasised fragments
        inside a single `st_write` call. Each variant carries
        **semantic meaning**, not just color: `keyword` (primary
        term), `accent` (tool / identifier), `highlight` (paradox /
        warning fact). Used in roughly **150 blocks** of the corpus.
    """)
    st_space("v", 1)

    show_code("""\
class BlockStyles:
    body = s.project.titles.body
    keyword = s.bold + s.project.colors.primary
    accent = s.bold + s.project.colors.accent
    highlight = s.bold + s.project.colors.highlight

st_write(bs.body,
         "Predicted AI would make them ",
         (bs.keyword, "24% faster"),
         ", but they were ",
         (bs.highlight, "actually 19% slower"),
         ".")""")
    st_space("v", 1)

    # Live demo for inline_emphasis (renders cleanly here)
    with st_block(s.project.containers.result_box):
        st_write(bs.body,
                 "Predicted AI would make them ",
                 (bs.keyword, "24% faster"),
                 ", but they were ",
                 (bs.highlight, "actually 19% slower"),
                 ".")
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/inline_emphasis.md"),
             (bs.accent, " for full details."))
    st_space("v", 1)
