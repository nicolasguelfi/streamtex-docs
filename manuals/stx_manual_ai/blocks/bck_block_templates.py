"""Part 5 — Block composition templates: visual catalog of 10 template patterns."""

from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Template catalog block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Template card
    bp_card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border: 1px solid rgba(139, 92, 246, 0.20); "
        "border-radius: 8px; padding: 16px;",
        "bp_card",
    )
    bp_number = s.project.colors.ai_violet + s.bold + s.Large
    bp_name = s.project.colors.cyber_cyan + s.bold + s.large
    bp_use = s.large


bs = BlockStyles


def build():
    """Render the block composition template catalog section."""
    st_space("v", 1)
    st_write(bs.heading, "Block composition templates",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX projects compose every block from a small set of
        recurring layouts — title, section header, content + bullets,
        comparison, image + text, code demo, timeline, quote, gallery,
        conclusion. The AI agent selects the best template based on
        your description and generates a standards-compliant block.
        Reusable components (in installed packs) plug into these
        layouts; see the reuse-architecture skill for the catalog.
    """)
    st_space("v", 2)

    # ── Templates 1-4 ────────────────────────────────────────────
    st_write(bs.sub, "Templates 1 — 4", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "1", tag=t.div)
                st_write(bs.bp_name, "Title", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Course or project title page with
                    author info, date, and subtitle.
                    Always the first block in a project.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "2", tag=t.div)
                st_write(bs.bp_name, "Section Header", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Section divider with part number.
                    Marks the start of a new thematic
                    group of blocks.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "3", tag=t.div)
                st_write(bs.bp_name, "Content", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Title plus bullet points. The most
                    common template — used for teaching
                    concepts, listing features, or explaining
                    ideas.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "4", tag=t.div)
                st_write(bs.bp_name, "Comparison", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Two-column X vs Y layout. Ideal for
                    contrasting approaches, tools, or
                    before/after views.
                """)
    st_space("v", 1)

    # ── Templates 5-8 ────────────────────────────────────────────
    st_write(bs.sub, "Templates 5 — 8", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "5", tag=t.div)
                st_write(bs.bp_name, "Image + Text", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Image paired with explanatory text.
                    Used for diagrams, screenshots, or
                    visual examples alongside descriptions.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "6", tag=t.div)
                st_write(bs.bp_name, "Code Demo", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Code snippet with rendered output.
                    Shows both the source code and its
                    visual result side by side.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "7", tag=t.div)
                st_write(bs.bp_name, "Timeline", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Numbered steps or workflow sequence.
                    Perfect for installation guides,
                    processes, and step-by-step tutorials.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "8", tag=t.div)
                st_write(bs.bp_name, "Quote", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Highlighted citation or key message.
                    Draws attention to an important
                    insight, motto, or principle.
                """)
    st_space("v", 1)

    # ── Templates 9-10 ──────────────────────────────────────────
    st_write(bs.sub, "Templates 9 — 10", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "9", tag=t.div)
                st_write(bs.bp_name, "Gallery", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Grid of images arranged in columns.
                    Used for showcasing multiple visuals,
                    icons, or example outputs together.
                """)
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "10", tag=t.div)
                st_write(bs.bp_name, "Conclusion", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, """\
                    Synthesis of key takeaways. Wraps up
                    a section or project with a summary
                    of the most important points.
                """)
    st_space("v", 2)

    # ── How templates are used ──────────────────────────────────
    st_write(bs.sub, "From Description to Block",
             toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.large,
        "Describe what you want in plain English. "
        "The AI picks the best template and generates "
        "a complete, standards-compliant block:",
    )
    st_space("v", 1)

    show_code("""\
        # User prompt:
        "Create a block comparing Python vs JavaScript
        for data science."

        # AI selects: Template 4 — Comparison
        # Generates: bck_07_python_vs_js.py
        #   - Two-column grid layout
        #   - Left column: Python strengths
        #   - Right column: JavaScript strengths
        #   - BlockStyles class + build() function
        #   - All styles from custom/styles.py
    """, language="python", line_numbers=False)
    st_space("v", 2)

    # ── Composability tip ────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "Templates are composable",
        )
        st_space("v", 1)
        st_write(s.large, """\
            You can combine multiple templates in a single
            block. For example, a Content template followed
            by a Code Demo section, ending with a Quote
            callout. The AI understands these combinations
            and merges them naturally when your description
            calls for it. To pull reusable components from
            an installed pack (callouts, cards, headings,
            etc.), invoke `stx component list` and pass the
            component name to the AI.
        """)
    st_space("v", 1)

    show_details("""\
        Templates are guidelines, not rigid skeletons. The
        AI adapts each pattern to your specific content —
        adjusting column counts, adding or removing sections,
        and choosing appropriate styles. Think of them as
        starting points that ensure structural consistency
        across your project.
    """)
    st_space("v", 1)
