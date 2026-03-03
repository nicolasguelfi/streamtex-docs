"""Part 5 — Block Blueprints: visual catalog of the 10 template patterns."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Blueprints catalog block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Blueprint card
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
    """Render the Block Blueprints catalog section."""
    st_space("v", 1)
    st_write(bs.heading, "Block Blueprints",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The block-blueprints.md skill contains 10 reusable
        template patterns. Each blueprint defines a proven
        layout for a specific type of content. Agents select
        the best blueprint based on your description and
        generate a standards-compliant block.
    """)
    st_space("v", 2)

    # ── Blueprints 1-4 ────────────────────────────────────────────
    st_write(bs.sub, "Blueprints 1 — 4", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "1", tag=t.div)
                st_write(bs.bp_name, "Title", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Course or project title page with
                    author info, date, and subtitle.
                    Always the first block in a project.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "2", tag=t.div)
                st_write(bs.bp_name, "Section Header", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Section divider with part number.
                    Marks the start of a new thematic
                    group of blocks.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "3", tag=t.div)
                st_write(bs.bp_name, "Content", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Title plus bullet points. The most
                    common blueprint — used for teaching
                    concepts, listing features, or explaining
                    ideas.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "4", tag=t.div)
                st_write(bs.bp_name, "Comparison", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Two-column X vs Y layout. Ideal for
                    contrasting approaches, tools, or
                    before/after views.
                """))
    st_space("v", 1)

    # ── Blueprints 5-8 ────────────────────────────────────────────
    st_write(bs.sub, "Blueprints 5 — 8", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "5", tag=t.div)
                st_write(bs.bp_name, "Image + Text", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Image paired with explanatory text.
                    Used for diagrams, screenshots, or
                    visual examples alongside descriptions.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "6", tag=t.div)
                st_write(bs.bp_name, "Code Demo", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Code snippet with rendered output.
                    Shows both the source code and its
                    visual result side by side.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "7", tag=t.div)
                st_write(bs.bp_name, "Timeline", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Numbered steps or workflow sequence.
                    Perfect for installation guides,
                    processes, and step-by-step tutorials.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "8", tag=t.div)
                st_write(bs.bp_name, "Quote", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Highlighted citation or key message.
                    Draws attention to an important
                    insight, motto, or principle.
                """))
    st_space("v", 1)

    # ── Blueprints 9-10 ──────────────────────────────────────────
    st_write(bs.sub, "Blueprints 9 — 10", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2,
                 cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "9", tag=t.div)
                st_write(bs.bp_name, "Gallery", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Grid of images arranged in columns.
                    Used for showcasing multiple visuals,
                    icons, or example outputs together.
                """))
        with g.cell():
            with st_block(bs.bp_card):
                st_write(bs.bp_number, "10", tag=t.div)
                st_write(bs.bp_name, "Conclusion", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.bp_use, textwrap.dedent("""\
                    Synthesis of key takeaways. Wraps up
                    a section or project with a summary
                    of the most important points.
                """))
    st_space("v", 2)

    # ── How blueprints are used ──────────────────────────────────
    st_write(bs.sub, "From Description to Block",
             toc_lvl="+1")
    st_space("v", 1)

    st_write(
        s.large,
        "Describe what you want in plain English. "
        "The AI picks the best blueprint and generates "
        "a complete, standards-compliant block:",
    )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # User prompt:
        "Create a block comparing Python vs JavaScript
        for data science."

        # AI selects: Blueprint 4 — Comparison
        # Generates: bck_07_python_vs_js.py
        #   - Two-column grid layout
        #   - Left column: Python strengths
        #   - Right column: JavaScript strengths
        #   - BlockStyles class + build() function
        #   - All styles from custom/styles.py
    """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── Composability tip ────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(
            s.project.titles.tip_label,
            "Blueprints are composable",
        )
        st_space("v", 1)
        st_write(s.large, textwrap.dedent("""\
            You can combine multiple blueprint patterns in
            a single block. For example, a Content blueprint
            followed by a Code Demo section, ending with a
            Quote callout. The AI understands these
            combinations and will merge patterns naturally
            when your description calls for it.
        """))
    st_space("v", 1)

    show_details("""\
        Blueprints are guidelines, not rigid templates.
        The AI adapts each pattern to your specific content
        — adjusting column counts, adding or removing
        sections, and choosing appropriate styles. Think
        of them as starting points that ensure structural
        consistency across your project.
    """)
    st_space("v", 1)
