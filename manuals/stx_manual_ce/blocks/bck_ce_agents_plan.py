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
    """PLAN agents: structure-architect, domain-researcher,
    learnings-researcher, plan-reconciler, objective-monitor."""

    st_space("v", 1)
    st_write(bs.heading, "PLAN Phase Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             ("The ", (s.project.titles.phase_kw, "PLAN"),
              " phase transforms assessment results into a concrete document "
              "skeleton. One main agent — the ",
              (s.project.titles.concept_kw, "structure-architect"),
              " — designs the skeleton, supported by two agents that feed it "
              "domain expertise and past learnings. Two additional agents — ",
              (s.project.titles.concept_kw, "plan-reconciler"),
              " and ",
              (s.project.titles.concept_kw, "objective-monitor"),
              " — engage on subsequent CE sessions to keep `book.py` and the master plan aligned, and to track whether the iteration's objectives have been met. "
              "The phase operates in two modes: ",
              (s.bold, "auto"),
              " (fully autonomous) and ",
              (s.bold, "interactive"),
              " (4-step collaborative iteration with the user). On the first iteration, structure-architect also produces the global TOC skeleton of the master plan; on subsequent iterations, it produces only the detailed plan for the current increment in coherence with the existing master plan."))
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
    2. Run supporting agents (domain-researcher, learnings-researcher)
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
    ### Agent: domain-researcher (supporting)

    The **domain-researcher** gathers domain knowledge, best practices,
    and technical references to inform the structure-architect's decisions.

    **Responsibilities:**

    - **Extract key topics** — identifies the core concepts and their
      relationships from the document plan and assessment outputs.
    - **Research best practices** — finds authoritative sources, standards,
      and patterns relevant to the subject matter.
    - **Identify technical references** — locates API documentation,
      specifications, and examples that should be referenced or included.
    - **Validate technical accuracy** — cross-checks planned content
      against authoritative sources to prevent errors.
    - **Recommend depth** — advises on how deeply each topic should be
      covered based on audience level and available references.

    **Output:** domain research report with key references, best practices,
    and depth recommendations for the structure-architect.
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
    ### Agent: plan-reconciler (cross-iteration)

    The **plan-reconciler** detects divergences between `book.py` (the live
    document structure executed by Streamlit) and the master plan TOC
    (`docs/master-plan.yaml -> toc` + `docs/master-plan.md` narrative TOC).
    It runs at the start of every CE session after the first, and also
    in FIX when patterns have been re-mapped.

    **Responsibilities:**

    - **Diff `book.py` vs master plan TOC** — detects additions, removals,
      renames, and reordering of blocks.
    - **Propose a global reconciliation** — one consolidated suggestion to
      align both, with an opt-out for a block-by-block walkthrough.
    - **Capture refusals as debt** — refused divergences are written to
      `master-plan.yaml -> coherence_debt` with the affected blocks.

    **Output:** reconciliation report surfaced through the universal QCM
    (recommended action + `Voir le détail bloc par bloc` + `Discutons-en`).
    """)

    st_space("v", 1)

    show_explanation("""
    ### Agent: objective-monitor (cross-iteration)

    The **objective-monitor** reads the master plan's free-text objectives
    (`master-plan.yaml -> objectives[*].criteria`) and the produced content
    of the current iteration, then judges — in plain text — whether each
    objective has been met. It does **not** compute metrics.

    **Responsibilities:**

    - **Read objectives + current state** — pulls free-text criteria and
      the iteration's content from blocks, reviews, and decisions log.
    - **Produce textual judgment** — per objective, a status (met / partial
      / not met) with rationale.
    - **Feed COMPOUND** — its output is consumed by Axis 4 of COMPOUND to
      update `master-plan.yaml -> objectives[*].status` and to flag
      unresolved objectives for the next iteration's PLAN.

    **Output:** objectives report integrated into the REVIEW synthesis and
    the COMPOUND master-plan-maintenance axis.
    """)

    show_details("""
    ### PLAN Agent Activation Summary

    | Agent | Role | Runs In | Input From | Output To |
    |-------|------|---------|------------|-----------|
    | structure-architect | Main | Auto + Interactive | Assessment brief, all supporting outputs | Document structure plan; master plan TOC (1st iteration only) |
    | domain-researcher | Supporting | Auto + Interactive | Assessment brief, document plan | Domain research report |
    | learnings-researcher | Supporting | Auto + Interactive | `docs/solutions/`, local + shared patterns catalog | Learnings research report |
    | plan-reconciler | Cross-iteration | CONTINUE, FIX | `book.py`, `master-plan.{yaml,md}` | Reconciliation proposal (QCM) |
    | objective-monitor | Cross-iteration | REVIEW, CONTINUE, COMPOUND | `master-plan.yaml -> objectives`, produced content | Textual judgment per objective |
    """)
