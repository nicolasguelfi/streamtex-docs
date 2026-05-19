"""Gallery — list-shaped patterns: ptn_card_grid, ptn_comparison_table,
ptn_takeaways, ptn_term_definition_list.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_and_run


class BlockStyles:
    """List patterns gallery styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    body_c = s.large + s.center_txt
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal
    highlight = s.bold + s.project.colors.highlight_amber
    label = s.bold + s.project.colors.primary_violet
    term = s.large + s.bold + s.project.colors.primary_violet
    definition = s.large
    separator = s.large + s.project.colors.neutral_gray
    sub_recap = s.large + s.bold + s.project.colors.accent_teal + s.center_txt
    key_msg = (
        s.huge + s.bold + s.project.colors.highlight_amber + s.center_txt
    )
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


CARDS = [
    ("AgileGen", "Gherkin + memory pool"),
    ("SE 3.0", "intent-centric"),
    ("MAISTRO", "7-phase agile"),
]

TABLE_ROWS = [
    ("Day 1", "GenAI fundamentals", "Vibecoding clinic"),
    ("Day 2", "GenSEM methods", "GSE-One workshop"),
    ("Day 3", "Compound Engineering", "Capstone & wrap-up"),
]

TAKEAWAYS = [
    ("Gains are real but variable",
     "depends on experience, context, task complexity"),
    ("The methodology is the multiplier",
     "10% with tools -> 25-30% with process"),
    ("Senior expertise + structured process",
     "= where the real value is captured"),
]

GLOSSARY = [
    ("ACI", "Agent-Computer Interface — structured protocols for AI "
            "agents to interact with tools."),
    ("CHOP", "Chat-Oriented Programming — multi-turn conversational "
             "interaction with LLMs."),
    ("MCP", "Model Context Protocol — open protocol connecting AI "
            "agents to external tools and data sources."),
    ("RAG", "Retrieval-Augmented Generation — combining LLMs with "
            "external knowledge retrieval."),
    ("TDD", "Test-Driven Development — write tests before "
            "implementation (Red-Green-Refactor)."),
]

RECAP_SECTIONS = [
    ("Why GenSEM matters",
     [("Evidence", "AI alone produces variable gains."),
      ("Method", "A discipline turns variable gains into reliable ones."),
      ("Shift", "Software engineering is being re-grounded around AI.")]),
    ("What GSE-One adds",
     [("Lifecycle", "8 phases keyed to AI-assisted work."),
      ("Guardrails", "Hard + soft + emergency rules per phase."),
      ("Capitalization", "Every cycle compounds prior learnings.")]),
]
RECAP_KEY_MESSAGE = "Methodology is the multiplier."


def build():
    """Compact gallery of list-shaped patterns."""
    with st_block(s.center_txt):
        st_write(bs.heading,
                 "List Patterns — card_grid, ptn_comparison_table, ptn_takeaways",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    show_explanation("""\
        Three patterns that organise lists of items: independent
        cards, comparable rows across attributes, and numbered key
        insights. Each shines in a different rhetorical situation.
    """)
    st_space("v", 2)

    # ---- ptn_card_grid ----
    st_write(bs.sub, "ptn_card_grid — responsive equal-weight cards",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Responsive grid (`auto-fit, minmax(220px, 1fr)`) of equal
        cards, each with a bolded keyword title and an optional body
        fragment. Used for taxonomies, inventories of risks, tools,
        principles.
    """)
    st_space("v", 1)

    def _demo_card_grid():
        with st_grid(cols="repeat(auto-fit, minmax(220px, 1fr))",
                     gap="12px", cell_styles=bs.cell) as g:
            for title, body in CARDS:
                with g.cell():
                    st_write(bs.body_c,
                             (bs.keyword, title),
                             (bs.body, f" — {body}"))

    show_and_run(_demo_card_grid)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_card_grid.md"),
             (bs.accent,
              " for cell tints (primary / accent / active) and limits."))
    st_space("v", 2)

    # ---- ptn_comparison_table ----
    st_write(bs.sub, "ptn_comparison_table — header row + aligned rows",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Multiple rows that share the same `cols=` template so columns
        align vertically. The header row uses a distinct cell style;
        an "active" row may be highlighted to draw the eye. Used for
        course schedules, tool comparisons, paradigm spectrums.
    """)
    st_space("v", 1)

    def _demo_comparison_table():
        with st_grid(cols="1fr 2fr 2fr", gap="8px",
                     cell_styles=bs.cell) as g:
            with g.cell():
                st_write(bs.body_c, (bs.label, "Day"))
            with g.cell():
                st_write(bs.body_c, (bs.label, "Morning"))
            with g.cell():
                st_write(bs.body_c, (bs.label, "Afternoon"))
            for day, am, pm in TABLE_ROWS:
                with g.cell():
                    st_write(bs.body_c, (bs.keyword, day))
                with g.cell():
                    st_write(bs.body_c, am)
                with g.cell():
                    st_write(bs.body_c, pm)

    show_and_run(_demo_comparison_table)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_comparison_table.md"),
             (bs.accent, " for active-row variants and column ratios."))
    st_space("v", 2)

    # ---- ptn_takeaways ----
    st_write(bs.sub, "ptn_takeaways — 3 to 5 numbered key insights",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Numbered list of 3 to 5 items, each with a bolded lead and a
        short explanation. Optionally closes with a one-line punch.
        The numbering is part of the rhetoric ("here are the 3 things
        to remember").
    """)
    st_space("v", 1)

    def _demo_takeaways():
        with st_block(s.project.containers.result_box):
            with st_list(li_style=bs.body) as l:
                for i, (lead, body) in enumerate(TAKEAWAYS, start=1):
                    with l.item():
                        st_write(bs.body,
                                 (bs.label, f"{i}. {lead} "),
                                 (bs.body, f"— {body}"))
            st_space("v", 1)
            st_write(bs.highlight + s.center_txt,
                     "This is why we need a methodology, not just tools.")

    show_and_run(_demo_takeaways)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_takeaways.md"),
             (bs.accent, " for the punch-line and cite composition."))
    st_space("v", 2)

    # ---- ptn_takeaways · multi-slide recap variant ----
    st_write(bs.sub,
             "ptn_takeaways · multi-slide recap variant",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        When a whole section needs to be recapped at the end, the
        pattern is paginated: one sub-recap per slide via
        `st_slide_break(...)`, ending with a single-line "key
        message" slide. Below the three slides are rendered
        side-by-side as compact previews — real usage inserts a slide
        break between each.
    """)
    st_space("v", 1)

    def _demo_multi_slide_recap():
        with st_grid(cols="1fr 1fr 1fr", gap="16px",
                     cell_styles=bs.cell) as g:
            for sub_title, items in RECAP_SECTIONS:
                with g.cell():
                    st_write(bs.sub_recap, sub_title, tag=t.div)
                    st_space("v", 0.5)
                    with st_list(li_style=bs.body) as l:
                        for i, (lead, body) in enumerate(items, start=1):
                            with l.item():
                                st_write(bs.body,
                                         (bs.label, f"{i}. {lead} "),
                                         (bs.body, f"— {body}"))
            with g.cell():
                st_write(bs.key_msg, RECAP_KEY_MESSAGE, tag=t.div)

    show_and_run(_demo_multi_slide_recap)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_takeaways.md · ## Variants"),
             (bs.accent, " for the full multi-slide recap rules."))
    st_space("v", 2)

    # ---- ptn_term_definition_list ----
    st_write(bs.sub,
             "ptn_term_definition_list — glossary rows",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Vertical list of `term — definition` rows for glossaries,
        notation tables, and abbreviation references. Each row uses a
        single tuple-style `st_write` so the term and definition wrap
        together as one line.
    """)
    st_space("v", 1)

    def _demo_term_definition_list():
        with st_block(s.project.containers.result_box):
            with st_zoom(120):
                for term, definition in GLOSSARY:
                    st_write(
                        bs.definition,
                        (bs.term, term),
                        (bs.separator, " — "),
                        (bs.definition, definition),
                    )
                    st_space("v", 0.5)

    show_and_run(_demo_term_definition_list)
    st_space("v", 1)

    st_write(bs.body, (bs.accent, "See "),
             (bs.keyword, "core/ptn_term_definition_list.md"),
             (bs.accent,
              " for full INVARIANTS (em-dash separator, muted color)."))
    st_space("v", 1)
