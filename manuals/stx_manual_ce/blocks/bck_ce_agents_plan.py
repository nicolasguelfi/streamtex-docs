"""CE Manual — Part 3: PLAN Agents Detail."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """PLAN Phase Agents styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """PLAN agents: structure-architect, content-strategist,
    learnings-researcher, audience-analyst, visual-reviewer."""

    st_space("v", 1)
    st_write(bs.heading, "PLAN Phase Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             ("The ", (s.project.titles.phase_kw, "PLAN"),
              " phase transforms assessment results into a concrete document "
              "skeleton. One main agent — the ",
              (s.project.titles.concept_kw, "structure-architect"),
              " — designs the skeleton, supported by four agents that feed it "
              "content analysis, past learnings, audience insights, and visual "
              "proposals. The phase operates in two modes: ",
              (s.bold, "auto"),
              " (fully autonomous) and ",
              (s.bold, "interactive"),
              " (4-step collaborative iteration with the user)."))
    st_space("v", 1)

    show_explanation("""
    ### Agent: structure-architect (main)

    The **structure-architect** is the central agent of the PLAN phase. It
    designs the full document skeleton: parts, sections, blocks, navigation
    flow, and reading progression.

    **Responsibilities:**

    - **Load requirements** — reads the ASSESS outputs: objectives, audience
      profile, content strategy, and gap analysis (or angle selection for
      Pathway C).
    - **Map content to blocks** — assigns each content item to a specific
      block type and position within the document structure.
    - **Define navigation flow** — chooses from patterns such as linear,
      branching, hub-and-spoke, or progressive disclosure, depending on
      content type and audience needs.
    - **Validate progression** — checks that prerequisites are respected,
      the difficulty curve is smooth, pacing is appropriate, and all
      objectives have coverage.
    - **Interactive mode** — when activated, presents the skeleton for user
      iteration through 4 collaborative steps (see below).

    **Output:** document structure plan containing the skeleton, navigation
    map, and production plan (task list for the PRODUCE phase).
    """)

    show_details("""
    ### structure-architect: Auto vs Interactive Mode

    **Auto mode:**
    1. Load approved assessment from `docs/assess/`
    2. Run supporting agents (content-strategist, learnings-researcher)
    3. Structure-architect generates full plan in one pass
    4. **GATE** — user reviews and approves or requests changes

    **Interactive mode (4 steps):**

    | Step | Focus | User Action |
    |------|-------|-------------|
    | 1. Skeleton | Parts, sections, block list | Validate or reshape structure |
    | 2. Objectives | Per-block learning objectives | Confirm scope and depth |
    | 3. Design | Visual layout, navigation pattern | Choose palette and layout |
    | 4. Final Plan | Complete plan with production tasks | Approve for PRODUCE |

    Each step waits for user validation before proceeding. The user can
    go back to any previous step to refine decisions.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Agent: content-strategist (supporting)

    The **content-strategist** provides the structure-architect with a
    deep analysis of the available content.

    **Responsibilities:**

    - **Theme clustering** — groups content by theme and identifies natural
      section boundaries.
    - **Gap identification** — detects missing topics, prerequisites that
      lack coverage, and practical elements (examples, exercises) that
      should be added.
    - **Duplicate detection** — finds overlapping content across sources
      and recommends consolidation strategies.
    - **Progression logic** — evaluates whether the proposed reading order
      respects conceptual dependencies and builds knowledge incrementally.
    - **Objective validation** — cross-checks content coverage against the
      learning objectives from the ASSESS phase.

    **Output:** content strategy report with theme map, gap analysis, and
    recommendations for the structure-architect.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Agent: learnings-researcher (supporting)

    The **learnings-researcher** mines past project experience to prevent
    repeating mistakes and surface reusable patterns.

    **Responsibilities:**

    - **Search past solutions** — scans `docs/solutions/` for documented
      solutions from previous CE cycles that are relevant to the current
      project.
    - **Score relevance** — ranks each past learning by how applicable it
      is to the current context (content type, audience, format).
    - **Extract insights** — pulls out actionable information: warnings
      about pitfalls, proven patterns, time-saving shortcuts.
    - **Prevent regressions** — flags issues that were solved before but
      could recur if the same approach is used.

    **Output:** learnings research report with scored and annotated insights.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Agent: audience-analyst (advisory)

    The **audience-analyst** revisits the audience profile established
    during ASSESS, refining it for PLAN-phase decisions.

    - Confirms or adjusts the audience profile based on structural choices
      being considered by the structure-architect.
    - Advises on reading level, section granularity, and example density.

    **Output:** audience profile card (updated if needed).
    """)

    st_space("v", 1)

    show_explanation("""
    ### Agent: visual-reviewer (advisory)

    The **visual-reviewer** operates in advisory mode during the PLAN phase,
    providing design direction before production begins.

    - **Color palette** — proposes a palette aligned with content tone and
      audience expectations.
    - **Layout patterns** — recommends grid layouts, sidebar usage, and
      block density per page.
    - **Visual hierarchy** — defines heading sizes, spacing rhythm, and
      emphasis techniques for the document.

    **Output:** design proposals integrated into the structure plan.
    """)

    show_details("""
    ### PLAN Agent Activation Summary

    | Agent | Role | Runs In | Input From | Output To |
    |-------|------|---------|------------|-----------|
    | structure-architect | Main | Auto + Interactive | Assessment brief, all supporting outputs | Document structure plan |
    | content-strategist | Supporting | Auto + Interactive | Source inventory, assessment | Content strategy report |
    | learnings-researcher | Supporting | Auto + Interactive | `docs/solutions/` | Learnings research report |
    | audience-analyst | Advisory | Auto + Interactive | Assessment brief | Audience profile card |
    | visual-reviewer | Advisory | Auto + Interactive | Content strategy, audience profile | Design proposals |
    """)
