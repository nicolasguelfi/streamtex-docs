"""CE Manual — Part 3: REVIEW and COMPOUND Agents Detail."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """REVIEW and COMPOUND Phase Agents styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """REVIEW agents (5 perspectives) and COMPOUND agents."""

    st_space("v", 1)
    st_write(bs.heading, "REVIEW and COMPOUND Phase Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ", (s.project.titles.phase_kw, "REVIEW"),
              " phase applies ", (s.bold, "five independent perspectives"),
              " to the produced content. Each reviewer examines the same blocks "
              "but through a different lens, ensuring comprehensive quality coverage. "
              "The ", (s.project.titles.phase_kw, "COMPOUND"),
              " phase then harvests learnings from the entire cycle.")
    st_space("v", 1)

    show_explanation("""
    ### The Five Review Perspectives

    **1. audience-advocate** — Reviews from the reader's point of view.
    Checks whether explanations are clear, prerequisites are respected,
    jargon is defined, and the reading flow feels natural. Flags content
    that assumes too much or explains too little.

    **2. pedagogy-analyst** — Evaluates the learning design. Checks that
    concepts build progressively, examples follow explanations, practice
    opportunities exist, and the difficulty curve is appropriate. Ensures
    show_explanation() and show_details() are used effectively.

    **3. visual-reviewer** — Assesses layout and visual hierarchy. Checks
    spacing, heading levels, use of columns and expanders, image placement,
    table readability, and overall page balance. Flags walls of text and
    visual clutter.

    **4. style-consistency-checker** — Verifies adherence to the project's
    style conventions. Checks naming patterns, BlockStyles usage, consistent
    terminology, code formatting, and compliance with the custom styles
    defined in `custom/styles.py`.

    **5. content-editor** — Proofreads for accuracy, grammar, completeness,
    and tone. Suggests rewording for awkward sentences, flags factual errors,
    and checks that all promised content is actually delivered.
    """)

    st_space("v", 1)

    show_details("""
    ### Review Severity Levels

    Each reviewer assigns a severity to every finding:

    | Severity | Meaning | Action Required |
    |----------|---------|-----------------|
    | **blocker** | Prevents publication | Must fix before release |
    | **major** | Significantly degrades quality | Should fix in current cycle |
    | **minor** | Small improvement opportunity | Fix if time permits |
    | **suggestion** | Stylistic preference | Consider for next cycle |

    ### Review Report Structure

    ```
    Review: <perspective-name>
    Reviewer: <agent-name>
    Blocks reviewed: <count>

    Findings:
      [R001] bck_intro_welcome.py, line 34
         Severity: major
         Category: clarity
         Issue: Technical term "hydration" used without definition
         Suggestion: Add a one-sentence definition or link to glossary

      [R002] bck_advanced_api.py, line 78
         Severity: minor
         Category: visual
         Issue: Code block immediately follows another code block
         Suggestion: Add explanatory text between consecutive code blocks
    ```
    """)

    st_space("v", 1)

    show_explanation("""
    ### COMPOUND Agents

    The COMPOUND phase operates two agents that work outside the linear
    COLLECT-ASSESS-PLAN-PRODUCE-REVIEW pipeline.

    **feedback-detector** — Scans all artifacts produced during the cycle
    (inventory, assessment, plan, blocks, reviews) looking for insights
    that transcend the current project:

    - Patterns that could become reusable solutions
    - Recurring problems that suggest missing StreamTeX features
    - Workflow friction points worth reporting to the ecosystem
    - Effective techniques worth documenting in the producer profile

    **dev-governance** — Manages the formal capitalization outputs:

    - **Solutions axis**: packages proven patterns into reusable templates
      or block libraries with documentation.
    - **Profiles axis**: updates the producer profile with new skills,
      preferences, and learned conventions.
    - **Ecosystem axis**: formats feedback for StreamTeX developers —
      bug reports, feature requests, and documentation improvements.
    """)

    st_space("v", 1)

    show_details("""
    ### COMPOUND Agent Outputs

    | Agent | Output | Template Used | Destination |
    |-------|--------|---------------|-------------|
    | feedback-detector | Insight report | `tpl_ecosystem_feedback` | dev-governance input |
    | dev-governance | Solution package | `tpl_solution_package` | Project `docs/solutions/` |
    | dev-governance | Profile update | `tpl_producer_profile` | Project `docs/profile.md` |
    | dev-governance | Ecosystem feedback | `tpl_ecosystem_feedback` | GitHub issue / discussion |

    ### When COMPOUND Runs

    The COMPOUND phase runs **after every complete cycle**, but its intensity
    varies. A quick import cycle might produce only a minor profile update,
    while a major creation project could yield multiple solutions and several
    ecosystem feedback items. The feedback-detector uses heuristics to avoid
    generating noise — it only reports insights that meet a significance threshold.
    """)

    st_space("v", 1)
