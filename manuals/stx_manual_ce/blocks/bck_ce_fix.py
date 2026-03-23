"""CE Manual — Part 2: FIX Phase."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the FIX phase block."""
    title = s.part_title if hasattr(s, "part_title") else {}
    phase = s.phase if hasattr(s, "phase") else {}


def build():
    """FIX phase: load review, apply corrections, verify, re-audit."""

    st_write("""
    ## FIX — Apply Corrections from Review

    The **FIX** phase is the complement to REVIEW. While REVIEW is read-only,
    FIX is **write-only in purpose**: it loads the review report, applies
    corrections to block files, verifies each fix, and runs a global re-audit
    to confirm resolution.

    FIX is a **new phase** in the CE cycle, introduced to separate the
    concerns of evaluation (REVIEW) and correction (FIX).
    """)

    show_explanation("The FIX Pipeline", """
    FIX operates in five sequential steps:

    **1. LOAD** — Read the review report
    - Parse all findings by severity (CRITICAL first)
    - Group findings by block for efficient processing
    - Identify dependencies between fixes

    **2. APPLY** — Execute corrections
    - Each finding is addressed with a targeted edit
    - CRITICAL fixes are applied first, then WARNINGs
    - INFO items are applied only with `--thorough`
    - Edits use minimal changes (no unnecessary rewrites)

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

    show_explanation("The REVIEW-FIX-REVIEW Iteration Loop", """
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
    - Iteration stops when: no CRITICAL, no WARNING, or max reached
    - Remaining INFO items are logged but do not block completion

    **The loop is automatic** in `/stx-ce:go` mode. In manual mode,
    the user triggers each REVIEW and FIX explicitly.
    """)

    show_explanation("Traceability Report", """
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

    show_details("Command Reference", """
    ```bash
    # Apply fixes from review report
    /stx-ce:fix

    # Fix critical issues only
    /stx-ce:fix --severity critical

    # Fix specific blocks only
    /stx-ce:fix --blocks bck_start_welcome,bck_start_install

    # Include INFO-level improvements
    /stx-ce:fix --thorough

    # Dry run (show planned fixes without applying)
    /stx-ce:fix --dry-run

    # Run the full REVIEW-FIX loop (max 3 iterations)
    /stx-ce:fix --iterate
    ```

    Fix reports are saved to `.ce/fix-report-N.md` (one per iteration).
    """)
