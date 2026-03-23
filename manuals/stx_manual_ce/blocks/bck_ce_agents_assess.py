"""CE Manual — Part 3: ASSESS Agents Detail."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """ASSESS Phase Agents styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """ASSESS agents: audience-analyst, content-strategist, gap-analyst,
    format-explorer, angle-generator."""

    st_space("v", 1)
    st_write(bs.heading, "ASSESS Phase Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             ("The ", (s.project.titles.phase_kw, "ASSESS"),
              " phase transforms raw inventory data into strategic decisions. "
              "Five agents work here, though not all activate for every pathway. ",
              (s.project.titles.pathway_kw, "Pathways A"),
              " and ", (s.project.titles.pathway_kw, "B"),
              " use the gap-analyst; ",
              (s.project.titles.pathway_kw, "Pathway C"),
              " uses the angle-generator instead. "
              "The other three agents are shared across all pathways."))
    st_space("v", 1)

    show_explanation("""
    ### Agent: audience-analyst

    The **audience-analyst** profiles who will consume the final document.

    - **Audience profiling** — defines primary and secondary audiences with their
      background knowledge, expectations, and reading context.
    - **Prerequisite mapping** — lists what readers must already know and what
      the document must teach from scratch.
    - **Tone calibration** — recommends formality level, technical depth, and
      use of examples based on audience characteristics.

    This agent's output shapes every downstream decision — from content scope
    to visual complexity.
    """)

    show_explanation("""
    ### Agent: content-strategist

    The **content-strategist** defines the intellectual scope of the document.

    - **Theme identification** — extracts core themes from sources (pathways A/B)
      or from the project brief (pathway C).
    - **Learning objectives** — formulates what readers should know or be able to
      do after reading each section.
    - **Scope boundaries** — explicitly states what is included and what is
      deliberately excluded, preventing scope creep.
    - **Content map** — produces a high-level topic graph showing relationships
      between themes and their relative importance.
    """)

    show_explanation("""
    ### Agent: gap-analyst (Pathways A and B)

    The **gap-analyst** compares the current state against the desired outcome.

    - **For Pathway A (Import)**: compares source material against the target
      StreamTeX structure. Identifies content that maps cleanly, content that
      needs restructuring, and missing pieces that must be written fresh.
    - **For Pathway B (Improve)**: compares the existing StreamTeX project
      against quality criteria and new requirements. Lists outdated blocks,
      missing topics, style inconsistencies, and structural weaknesses.
    - **Gap severity** — each gap is rated: *critical* (blocks progress),
      *important* (degrades quality), or *minor* (nice to fix).
    """)

    show_details("""
    ### gap-analyst Output Structure

    ```
    Gap Analysis Report
    ===================
    Pathway: A (Import) | B (Improve)
    Sources evaluated: <count>

    Gaps:
      [G001] Missing introduction for Section 3
         Severity: critical
         Type: content-missing
         Affected: S003 -> Part 2, Block 5

      [G002] Outdated API examples in advanced chapter
         Severity: important
         Type: content-outdated
         Affected: blocks/bck_advanced_api.py

    Summary:
      Critical: 2 | Important: 5 | Minor: 8
    ```
    """)

    show_explanation("""
    ### Agent: format-explorer

    The **format-explorer** surveys available StreamTeX features and recommends
    the best block types and layouts for the content.

    - **Block type recommendation** — maps content categories to appropriate
      StreamTeX components: expanders, tabs, columns, lists, code blocks.
    - **Layout patterns** — suggests page-level organization: how many blocks
      per page, sidebar usage, navigation flow.
    - **Visual density** — balances information density against readability
      based on the audience-analyst's recommendations.
    """)

    show_explanation("""
    ### Agent: angle-generator (Pathway C Only)

    The **angle-generator** activates only for new document creation. Where the
    gap-analyst works from existing material, the angle-generator works from
    a blank canvas.

    - **Creative angles** — proposes 3-5 different approaches to structuring
      the document (e.g., tutorial-style, reference-style, narrative-style).
    - **Structural options** — for each angle, outlines the part/block skeleton
      and the reading flow.
    - **Trade-off analysis** — compares angles on: audience fit, production
      effort, maintainability, and reuse potential.

    The user picks one angle (or combines elements from several), and this
    choice feeds into the PLAN phase.
    """)

    show_details("""
    ### ASSESS Agent Activation Summary

    | Agent | Pathway A | Pathway B | Pathway C | Input From | Output To |
    |-------|-----------|-----------|-----------|------------|-----------|
    | audience-analyst | Yes | Yes | Yes | Source inventory / brief | Assessment brief |
    | content-strategist | Yes | Yes | Yes | Source inventory / brief | Assessment brief |
    | gap-analyst | Yes | Yes | -- | Source inventory + targets | Gap report |
    | format-explorer | Yes | Yes | Yes | Content map + audience | Format recommendations |
    | angle-generator | -- | -- | Yes | Project brief + audience | Angle proposals |
    """)
