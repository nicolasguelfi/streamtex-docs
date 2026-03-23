"""CE Manual — Part 5: Templates Reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Templates Reference styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Reference of all 12 CE templates: structure, usage, and frontmatter."""

    st_space("v", 1)
    st_write(bs.heading, "Templates Reference",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "CE ", (s.project.titles.concept_kw, "agents"),
             " communicate through ", (s.bold, "12 structured templates"),
             ". Each ", (s.project.titles.concept_kw, "template"),
             " defines a document format with required sections, optional "
             "sections, and frontmatter metadata. ",
             (s.project.titles.concept_kw, "Templates"),
             " ensure consistency across cycles and make ",
             (s.project.titles.concept_kw, "artifacts"),
             " machine-readable for downstream agents.")
    st_space("v", 1)

    show_details("""
    ### Template Overview

    | # | Template | Phase | Purpose |
    |---|----------|-------|---------|
    | 1 | `tpl_source_inventory` | COLLECT | List of detected sources with metadata |
    | 2 | `tpl_complexity_report` | COLLECT | Import difficulty assessment per source |
    | 3 | `tpl_audience_profile` | ASSESS | Target reader characteristics |
    | 4 | `tpl_content_map` | ASSESS | Theme graph and learning objectives |
    | 5 | `tpl_gap_report` | ASSESS | Current vs. desired state comparison |
    | 6 | `tpl_angle_proposal` | ASSESS | Structural approach options (pathway C) |
    | 7 | `tpl_structure_plan` | PLAN | Document skeleton with parts and blocks |
    | 8 | `tpl_task_sequence` | PLAN | Ordered production tasks with estimates |
    | 9 | `tpl_review_report` | REVIEW | Findings from one review perspective |
    | 10 | `tpl_solution_package` | COMPOUND | Reusable pattern documentation |
    | 11 | `tpl_producer_profile` | COMPOUND | Personal conventions and skills |
    | 12 | `tpl_ecosystem_feedback` | COMPOUND | Bug report or feature request |
    """)

    st_space("v", 1)

    show_explanation("""
    ### Template Structure

    Every template follows the same general layout:

    1. **Frontmatter** — metadata block at the top identifying the template
       type, creation date, project, and phase.
    2. **Required sections** — sections that must be filled for the template
       to be valid. Agents will flag incomplete required sections.
    3. **Optional sections** — additional sections that add value when
       applicable but can be omitted without breaking the workflow.
    4. **References** — links to input artifacts and related templates.

    Templates are plain Markdown files stored in `docs/`. They are
    designed for both human reading and agent parsing.
    """)

    st_space("v", 1)

    show_details("""
    ### COLLECT Templates

    **tpl_source_inventory**
    ```
    ---
    template: source_inventory
    project: <name>
    date: <timestamp>
    pathway: A | B | C
    ---
    ## Sources
    [S001] <filename>
      Format: <type> | Size: <size> | Words: ~<count>
      Components: headings:<n>, images:<n>, tables:<n>, code:<n>
      Dependencies: <list>
    ```
    Required: at least one source entry (pathway A/B) or context entry (C).

    **tpl_complexity_report** (pathway A only)
    ```
    ---
    template: complexity_report
    project: <name>
    date: <timestamp>
    ---
    ## Assessments
    [S001] <filename>
      Complexity: low | medium | high
      Method: automated | assisted | manual
      Effort: <estimate>
      Notes: <details>
    ```
    """)

    st_space("v", 1)

    show_details("""
    ### ASSESS Templates

    **tpl_audience_profile**
    - Required: primary audience, knowledge level, reading context
    - Optional: secondary audience, accessibility needs, language notes

    **tpl_content_map**
    - Required: themes list, learning objectives, scope boundaries
    - Optional: theme relationships, prerequisite graph

    **tpl_gap_report** (pathways A/B)
    - Required: gap entries with severity, type, and affected items
    - Optional: recommended resolution order, effort estimates

    **tpl_angle_proposal** (pathway C)
    - Required: at least 3 angle descriptions with skeletons
    - Optional: trade-off matrix, hybrid angle suggestions
    """)

    st_space("v", 1)

    show_details("""
    ### PLAN, REVIEW, and COMPOUND Templates

    **tpl_structure_plan**
    - Required: parts with titles, blocks with names and responsibilities
    - Optional: navigation flow diagram, style requirements

    **tpl_task_sequence**
    - Required: ordered task list with dependencies and estimates
    - Optional: parallelization groups, milestone markers

    **tpl_review_report**
    - Required: perspective name, blocks reviewed, findings with severity
    - Optional: summary statistics, comparison with prior reviews

    **tpl_solution_package**
    - Required: context, pattern description, example, "when not to use"
    - Optional: related solutions, version history

    **tpl_producer_profile**
    - Required: writing style, structural preferences, quality standards
    - Optional: tool proficiency, lessons learned, project history

    **tpl_ecosystem_feedback**
    - Required: problem statement, impact assessment, priority
    - Optional: proposed solution, reproduction steps, screenshots
    """)

    st_space("v", 1)
