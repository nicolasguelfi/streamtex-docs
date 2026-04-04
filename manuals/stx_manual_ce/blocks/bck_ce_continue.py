"""CE Manual — Part 2: /stx-ce:continue Session Resumption."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details, show_code
except ImportError:
    from streamtex import show_explanation, show_details, show_code


class BlockStyles:
    """/stx-ce:continue styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """/stx-ce:continue — session resumption and drift detection."""

    st_space("v", 1)
    st_write(bs.heading, "Session Resumption",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "CE cycles often span multiple sessions. Between sessions, "
             "sources may change, blocks may be edited manually, or the "
             "plan may become stale. The ",
             (s.project.titles.tool_kw, "/stx-ce:continue"),
             " command restores checkpoint context (if saved via ",
             (s.project.titles.tool_kw, "/stx-ce:pause"),
             "), detects drift, and proposes corrective actions before "
             "resuming work.")
    st_space("v", 1)

    st_write(s.large,
             "Without ",
             (s.project.titles.tool_kw, "/stx-ce:continue"),
             ", resuming a cycle risks working from outdated assumptions. "
             "If a checkpoint exists, it restores the decisions, in-progress "
             "items, and context from the previous session. Otherwise, "
             "drift detection still identifies what changed since the last "
             "CE activity.")
    st_space("v", 1)

    show_code("""\
        /stx-ce:continue
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    # ── The 4-Step Workflow ───────────────────────────────────────
    st_write(bs.sub, "The 4-Step Workflow", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### CHECKPOINT -> INSPECT -> DETECT DRIFT -> PROPOSE -> INTERACT

    **Step 0: RESTORE CHECKPOINT**
    If `docs/ce-checkpoint.md` exists (created by `/stx-ce:pause`),
    reads it and displays a restoration banner with the previous
    session's context: active work items, decisions, and pending
    issues. The checkpoint is archived after restoration.

    **Step 1: INSPECT**
    Reads all CE artifacts in `docs/` and all block files. Builds a
    snapshot of the current project state: which phases have completed,
    which artifacts exist, what the latest plan version says, and what
    blocks are registered.

    **Step 2: DETECT DRIFT**
    Compares the current snapshot against the last CE activity date.
    Identifies discrepancies across five drift categories (see below).

    **Step 3: PROPOSE**
    For each detected drift, generates a corrective proposal ranked by
    priority. Checkpoint active items are integrated as HIGH-priority
    proposals. Proposals are actionable: they specify exactly which CE
    command to run or which artifact to update.

    **Step 4: INTERACT**
    Presents the briefing and proposals to the user. The user can
    approve all proposals, select specific ones, modify them, or
    dismiss them and resume manually.
    """)

    st_space("v", 1)

    # ── Briefing ──────────────────────────────────────────────────
    st_write(bs.sub, "Briefing", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "The briefing is the first thing you see when running ",
             (s.project.titles.tool_kw, "/stx-ce:continue"),
             ". It summarizes the cycle state in a compact format.")
    st_space("v", 1)

    show_code("""\
        === CE Session Briefing ===

        Project:    stx_manual_ce
        Last phase: PRODUCE (completed 2026-03-28)
        Next phase: REVIEW
        Plan:       2026-03-25-002-structure-plan.md (v2)
        Blocks:     18 registered, 16 produced, 2 pending
        Sources:    12 files in docs/collect/

        Session gap: 6 days since last activity
        Drift detected: 3 items (1 CRITICAL, 2 INFO)
    """, language="text", line_numbers=False)
    st_space("v", 1)

    # ── Drift Detection ──────────────────────────────────────────
    st_write(bs.sub, "Drift Detection", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### 5 Drift Categories

    **1. source** — A source file in the collect inventory was modified,
    added, or deleted since the last session. Impact: the assessment or
    plan may be based on outdated content.

    **2. manual** — A block file was edited outside of CE (e.g., manual
    tweaks in an editor). Impact: the review findings may no longer
    match the current block content.

    **3. plan** — The plan references blocks that do not exist, or blocks
    exist that are not in the plan. Impact: production state is inconsistent.

    **4. stale** — An artifact (review, assessment) is older than the
    blocks it evaluated. Impact: quality judgments may be outdated.

    **5. unresolved** — CRITICAL or MAJOR review findings from the last
    cycle remain unfixed. Impact: quality debt is accumulating.
    """)

    st_space("v", 1)

    show_code("""\
        === Drift Report ===

        [CRITICAL] source: slides/chapter4.pdf modified (2026-04-01)
          -> Affects: assessment, plan blocks 14-16
          -> Proposal: re-run /stx-ce:collect, then /stx-ce:assess

        [INFO] manual: bck_ce_overview.py edited outside CE
          -> Affects: review findings for this block
          -> Proposal: mark block for re-review

        [INFO] stale: review report is 6 days old (3 blocks produced since)
          -> Affects: quality assessment completeness
          -> Proposal: run /stx-ce:review on new blocks only
    """, language="text", line_numbers=False)
    st_space("v", 1)

    # ── Proposals ─────────────────────────────────────────────────
    st_write(bs.sub, "Proposals", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Priority Logic

    | Priority | Condition | User Action |
    |----------|-----------|-------------|
    | **CRITICAL** | Source changed + affects plan | Must resolve before resuming |
    | **WARNING** | Manual edits detected | Should re-review affected blocks |
    | **MINOR** | Stale artifacts | Can proceed, re-review recommended |
    | **INFO** | Cosmetic or metadata drift | Safe to ignore |

    Proposals at CRITICAL priority block resumption: you cannot proceed
    without addressing them (approve, modify, or explicitly dismiss).
    All other priorities are advisory.
    """)

    st_space("v", 1)

    show_code("""\
        === Proposals ===

        [1/3] CRITICAL — Re-collect modified source
              Command: /stx-ce:collect
              Reason:  slides/chapter4.pdf changed, plan may be invalid
              Action:  approve | dismiss | modify

        [2/3] INFO — Re-review manually edited block
              Command: /stx-ce:task review "Check bck_ce_overview.py"
              Reason:  block edited outside CE
              Action:  approve | dismiss

        [3/3] INFO — Review new blocks
              Command: /stx-ce:review --blocks bck_ce_task,bck_ce_continue
              Reason:  3 blocks produced since last review
              Action:  approve | dismiss

        Enter: all | 1,3 | none >
    """, language="text", line_numbers=False)
    st_space("v", 1)

    # ── Best practices ────────────────────────────────────────────
    show_explanation("""\
    ### Best Practices for Multi-Session CE Work

    **1. Pause before leaving, continue when returning** — Use
    `/stx-ce:pause` before ending a session and `/stx-ce:continue`
    when starting the next one. This preserves context across sessions.

    **2. Always start with /stx-ce:continue** — Even if you think nothing
    changed, the command takes seconds and catches subtle drift (stale
    artifacts, unresolved findings) that you might miss. If a checkpoint
    exists, it restores your previous context automatically.

    **3. Commit CE artifacts to git** — The `docs/` folder should be
    version-controlled. This gives `/stx-ce:continue` reliable timestamps
    and makes drift detection more accurate. Include `ce-checkpoint.md`.

    **4. Prefer small sessions** — A 2-hour session that completes one
    phase is better than a marathon that leaves the cycle in an ambiguous
    state. Each phase boundary is a natural pause point.

    **5. Do not ignore CRITICAL drift** — If a source changed, the
    downstream artifacts (assessment, plan, blocks) may be based on
    wrong assumptions. Re-collecting is fast; debugging inconsistencies
    later is not.
    """)

    st_space("v", 1)
