"""CE Manual — Part 2: FIX Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """FIX phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """FIX phase: load review, apply corrections, verify, re-audit."""

    st_space("v", 1)
    st_write(bs.heading, "FIX — Apply Corrections from Review",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "FIX"),
             " phase is the complement to ",
             (s.project.titles.phase_kw, "REVIEW"),
             ". While ",
             (s.project.titles.phase_kw, "REVIEW"),
             " is read-only, ",
             (s.project.titles.phase_kw, "FIX"),
             " is ",
             (s.bold, "write-only in purpose"),
             ": it loads the review report, applies "
             "corrections to block files, verifies each fix, and runs a global re-audit "
             "to confirm resolution.")
    st_space("v", 1)

    st_write(s.large,
             (s.project.titles.phase_kw, "FIX"),
             " is a ",
             (s.bold, "new phase"),
             " in the CE cycle, introduced to separate the "
             "concerns of evaluation (",
             (s.project.titles.phase_kw, "REVIEW"),
             ") and correction (",
             (s.project.titles.phase_kw, "FIX"),
             ").")
    st_space("v", 1)

    show_explanation("""\
    ### The FIX Pipeline

    FIX operates in five sequential steps:

    **1. LOAD** — Read the review report
    - Parse all findings by severity (CRITICAL first)
    - Group findings by block for efficient processing
    - Identify dependencies between fixes

    **2. APPLY** — Execute corrections
    - Each finding is addressed with a targeted edit
    - CRITICAL fixes are applied first, then MAJORs
    - MINOR and SUGGESTION items are applied only with `--thorough`
    - Edits use minimal changes (no unnecessary rewrites)
    - Spacing inconsistencies: apply uniform SpacingConfig across blocks
    - Bibliography issues: add missing `st_bibliography()`, remove orphan `cite()` keys

    **3. VERIFY** — Check each fix individually
    - After each fix, the affected block is re-validated
    - Syntax check, render check, style check
    - If verification fails, the fix is rolled back

    **4. RE-AUDIT** — Global consistency check
    - All blocks are re-reviewed by the relevant agents
    - Cross-block findings are re-evaluated
    - New findings (introduced by fixes) are flagged

    **5. REPORT** — Traceability document
    - Every fix is logged with before/after diffs
    - Unresolved findings are listed with reasons
    - Overall quality score before and after FIX
    """)

    st_space("v", 1)

    show_explanation("""\
    ### The REVIEW-FIX-REVIEW Iteration Loop

    FIX is designed to iterate with REVIEW until quality converges:

    ```
    REVIEW  ->  FIX  ->  REVIEW  ->  FIX  ->  REVIEW (clean)
      47 findings  |    12 findings  |      0 findings
                   |                 |
              35 fixed          12 fixed
               0 new             0 new
    ```

    **Convergence rules:**
    - Maximum 3 iterations (prevents infinite loops)
    - If a fix introduces new findings, it is rolled back
    - Iteration stops when: no CRITICAL, no MAJOR, or max reached
    - Remaining MINOR and SUGGESTION items are logged but do not block completion

    **The loop is automatic** in `/stx-ce:go` mode. In manual mode,
    the user triggers each REVIEW and FIX explicitly.
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Traceability Report

    ```
    === CE FIX REPORT ===
    Iteration: 1 of 3
    Findings processed: 47
    Fixed: 35 | Skipped: 4 | Rolled back: 1 | Remaining: 7

    FIXES APPLIED:
      [FIX-01] bck_start_welcome: Added introduction paragraph
        Finding: [CRITICAL] content-editor
        Diff: +5 lines added at line 42
        Verified: PASS

      [FIX-02] bck_start_install: Added BlockStyles class
        Finding: [CRITICAL] style-consistency-checker
        Diff: +8 lines added at line 1
        Verified: PASS

    ROLLED BACK:
      [FIX-17] bck_core_types: Heading level change
        Reason: Introduced new cross-block inconsistency
        Action: Deferred to iteration 2

    QUALITY SCORE: 62% -> 89%
    ```
    """)

    st_space("v", 1)

    show_details("""\
    ### Command Reference

    ```bash
    # Apply fixes from review report
    /stx-ce:fix

    # Fix CRITICAL issues only
    /stx-ce:fix --severity CRITICAL

    # Fix specific blocks only
    /stx-ce:fix --blocks bck_start_welcome,bck_start_install

    # Include minor and suggestion-level improvements
    /stx-ce:fix --thorough

    # Dry run (show planned fixes without applying)
    /stx-ce:fix --dry-run

    # Run the full REVIEW-FIX loop (max 3 iterations)
    /stx-ce:fix --iterate
    ```

    Fix reports are saved to `docs/fix-report-N.md` (one per iteration).
    """)

    st_space("v", 1)
