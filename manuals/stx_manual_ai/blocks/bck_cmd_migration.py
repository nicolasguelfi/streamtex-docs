"""Migration Commands — Convert HTML content to StreamTeX blocks."""

import textwrap

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Migration commands block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    cmd_title = s.project.colors.ai_violet + s.bold + s.Large
    label_before = s.project.colors.error_red + s.bold + s.large
    label_after = s.project.colors.success_green + s.bold + s.large


bs = BlockStyles


def build():
    """Render the Migration Commands section."""
    st_space("v", 1)
    st_write(bs.heading, "Migration Commands", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        Migration commands convert existing HTML content into native
        StreamTeX blocks. Whether you have a single file or an entire
        directory of HTML pages, these commands automate the conversion
        while preserving structure and styling intent.
    """))
    st_space("v", 2)

    # ── Command 1: html-migrate ────────────────────────────────────
    st_write(bs.sub, "/migration:html-migrate", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Convert a Single HTML File", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Converts one HTML file into a StreamTeX block. The AI ",
            "maps HTML tags to stx functions, converts inline styles ",
            "to Style objects, and generates a complete block with ",
            "BlockStyles class and build() function.",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        /migration:html-migrate

        > Convert slides/intro.html to a StreamTeX block"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Before / After comparison ──────────────────────────────────
    st_write(bs.sub, "Before / After Example", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(bs.label_before, "HTML Input", tag=t.div)
                st_space("v", 1)
                show_code(textwrap.dedent("""\
                    <div style="text-align: center;">
                      <h1 style="color: #8B5CF6;
                          font-weight: bold;
                          font-size: 2em;">
                        Introduction
                      </h1>
                      <p style="font-size: 1.1em;">
                        Welcome to the course.
                      </p>
                      <ul>
                        <li>Topic A</li>
                        <li>Topic B</li>
                      </ul>
                    </div>"""), language="html")

        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.label_after, "StreamTeX Output", tag=t.div)
                st_space("v", 1)
                show_code(textwrap.dedent("""\
                    class BlockStyles:
                        heading = (
                            s.project.titles.section_title
                            + s.center_txt
                        )

                    bs = BlockStyles

                    def build():
                        st_space("v", 1)
                        st_write(
                            bs.heading,
                            "Introduction",
                            tag=t.div, toc_lvl="1",
                        )
                        st_space("v", 1)
                        st_write(
                            s.large,
                            "Welcome to the course.",
                        )
                        st_space("v", 1)
                        with st_list(list_type="ul"):
                            st_write(s.large, "Topic A")
                            st_write(s.large, "Topic B")
                    """), language="python")
    st_space("v", 2)

    # ── Command 2: html-convert-batch ──────────────────────────────
    st_write(bs.sub, "/migration:html-convert-batch",
             tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(bs.cmd_title, "Batch Convert Entire Directory", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Processes all .html files in a directory and creates a ",
            "blocks/ directory with the converted StreamTeX files. ",
            "Each HTML file becomes one block, named after the source.",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        /migration:html-convert-batch

        > Convert all files in legacy_slides/ to StreamTeX blocks

        Processing legacy_slides/ ...
          intro.html        -> blocks/bck_intro.py         OK
          chapter1.html     -> blocks/bck_chapter1.py      OK
          chapter2.html     -> blocks/bck_chapter2.py      OK
          summary.html      -> blocks/bck_summary.py       OK
          appendix.html     -> blocks/bck_appendix.py      WARN (complex table)

        Converted: 5 files (4 clean, 1 warning)
        Output: blocks/ directory created"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Tag mapping table ──────────────────────────────────────────
    st_write(bs.sub, "HTML to StreamTeX Mapping", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(s.project.titles.subsection_title,
                         "HTML Tags", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(s.large, "<h1> ... <h6>")
                    st_write(s.large, "<p>")
                    st_write(s.large, "<ul>, <ol>")
                    st_write(s.large, "<div>")
                    st_write(s.large, "<img>")
                    st_write(s.large, "<code>, <pre>")
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(s.project.titles.subsection_title,
                         "StreamTeX Functions", tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(s.large, "st_write() with toc_lvl")
                    st_write(s.large, "st_write()")
                    st_write(s.large, "st_list()")
                    st_write(s.large, "st_block()")
                    st_write(s.large, "st_image()")
                    st_write(s.large, "show_code()")
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Tip: always run /migration:conversion-audit after a batch
        conversion. It checks that every generated block is valid
        StreamTeX and flags any HTML constructs that could not be
        automatically converted (complex tables, embedded scripts,
        SVG elements).
    """))
    st_space("v", 1)
