"""Part 4 — Agent: Project Architect — designs full project structures."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Project Architect block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Step card
    step_card = Style(
        "background: rgba(6, 182, 212, 0.08); "
        "border: 1px solid rgba(6, 182, 212, 0.25); "
        "border-radius: 8px; padding: 20px;",
        "architect_step",
    )
    step_number = s.project.colors.cyber_cyan + s.bold + s.Large
    step_text = s.large


bs = BlockStyles


def build():
    """Render the Project Architect agent section."""
    st_space("v", 1)
    st_write(bs.heading, "Agent: Project Architect",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The Project Architect designs a complete project structure
        from a natural language description. It reads block blueprints
        and design rules, then produces a ready-to-implement plan.
    """)
    st_space("v", 2)

    # ── What it does (5 steps) ─────────────────────────────────────
    st_write(bs.sub, "What It Does", toc_lvl="+1")
    st_space("v", 1)

    with st_block(bs.step_card):
        with st_list(list_type="ol") as l:
            with l.item():
                st_write(
                    bs.step_text, "Reads block blueprints and design rules",
                )
            with l.item():
                st_write(
                    bs.step_text, "Analyzes the user's natural language description",
                )
            with l.item():
                st_write(
                    bs.step_text, "Creates a block plan — names, contents, ordering",
                )
            with l.item():
                st_write(
                    bs.step_text, "Proposes a color palette and visual theme",
                )
            with l.item():
                st_write(
                    bs.step_text, "Generates a features list for the project",
                )
    st_space("v", 2)

    # ── Design principles ──────────────────────────────────────────
    st_write(bs.sub, "Design Principles", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=3, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "1 Block = 1 Idea",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Each block covers exactly one concept.
                    No mixing of unrelated topics in a
                    single block file.
                """))
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Max 15 Blocks",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    A project should have at most 15 blocks.
                    If content exceeds that, split into
                    multiple projects or parts.
                """))
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Logical Ordering",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Blocks progress from foundational
                    concepts to advanced topics. Each block
                    builds on the previous ones.
                """))
    st_space("v", 2)

    # ── Example ────────────────────────────────────────────────────
    st_write(bs.sub, "Example: From Description to Plan",
             toc_lvl="+1")
    st_space("v", 1)

    st_write(s.project.titles.subsection_title, "User prompt:")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        Create a course on Python basics for beginners.
        Cover variables, loops, functions, and data structures.
    """), language="text", line_numbers=False)
    st_space("v", 1)

    st_write(s.project.titles.subsection_title, "Architect output:")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Block Plan
        bck_01_title.py          # Course title and overview
        bck_02_variables.py      # Variables and data types
        bck_03_strings.py        # String manipulation
        bck_04_numbers.py        # Numbers and arithmetic
        bck_05_conditionals.py   # If/elif/else logic
        bck_06_loops_for.py      # For loops and iteration
        bck_07_loops_while.py    # While loops
        bck_08_functions.py      # Defining and calling functions
        bck_09_parameters.py     # Parameters and return values
        bck_10_lists.py          # Lists and list methods
        bck_11_dictionaries.py   # Dictionaries and key-value pairs
        bck_12_summary.py        # Course summary and next steps

        # Theme: Fresh Green palette (#10B981 primary)
        # Features: code examples, exercises, key takeaways
    """), language="python", line_numbers=False)
    st_space("v", 2)

    # ── When to use ────────────────────────────────────────────────
    st_write(bs.sub, "When to Use", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        Use the Project Architect when starting a new project from
        scratch. Describe your content goals in plain English and
        let the agent produce the full block structure. You can then
        refine the plan before handing individual blocks to the
        Slide Designer for implementation.
    """)
    st_space("v", 1)
