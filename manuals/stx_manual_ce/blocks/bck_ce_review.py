"""CE Manual — Part 2: REVIEW Phase."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the REVIEW phase block."""
    title = s.part_title if hasattr(s, "part_title") else {}
    phase = s.phase if hasattr(s, "phase") else {}


def build():
    """REVIEW phase: 5 parallel agents, severity levels, read-only."""

    st_write("""
    ## REVIEW — Multi-Agent Quality Evaluation

    The **REVIEW** phase performs a comprehensive, **read-only** evaluation of
    all produced blocks. Five specialized agents work in parallel, each
    analyzing the content from a different perspective. No modifications are
    made during REVIEW — all findings are recorded in a review report for
    the FIX phase.
    """)

    show_explanation("The 5 Review Agents", """
    Each agent focuses on a specific quality dimension:

    | Agent | Focus | What it checks |
    |-------|-------|----------------|
    | **audience-advocate** | Audience fit | Vocabulary level, assumed knowledge, accessibility |
    | **pedagogy-analyst** | Learning quality | Objective alignment, progression, examples coverage |
    | **visual-reviewer** | Visual design | Layout consistency, whitespace, widget usage |
    | **style-consistency-checker** | Code style | StreamTeX patterns, naming conventions, ruff compliance |
    | **content-editor** | Content quality | Grammar, clarity, accuracy, completeness |

    All five agents run **in parallel** on each block. Their findings are
    merged into a single review report with no duplicates.
    """)

    show_explanation("Severity Levels", """
    Every finding is tagged with a severity level:

    **CRITICAL** — Must be fixed before delivery
    - Broken imports or render errors
    - Factually incorrect content
    - Missing blocks referenced in navigation
    - Accessibility violations

    **WARNING** — Should be fixed, but not blocking
    - Inconsistent style across blocks
    - Suboptimal pedagogical flow
    - Missing `show_details()` for optional content
    - Overly long blocks (>150 lines)

    **INFO** — Suggestions for improvement
    - Alternative widget choices
    - Additional examples that could help
    - Minor wording improvements
    - Cosmetic layout tweaks

    The FIX phase processes CRITICAL items first, then WARNINGs. INFO items
    are optional and applied only if `--thorough` is specified.
    """)

    show_explanation("Review Report Structure", """
    ```
    === CE REVIEW REPORT ===
    Project: my-training-course
    Blocks reviewed: 24
    Total findings: 47

    SUMMARY:
      CRITICAL ...  3 findings (must fix)
      WARNING  ... 18 findings (should fix)
      INFO     ... 26 findings (optional)

    PER-BLOCK FINDINGS:
      bck_start_welcome (3 findings):
        [CRITICAL] content-editor: Missing introduction paragraph
        [WARNING]  visual-reviewer: Hero banner has no fallback text
        [INFO]     pedagogy-analyst: Consider adding a "what you'll learn" list

      bck_start_install (5 findings):
        [CRITICAL] style-consistency-checker: Missing BlockStyles class
        [WARNING]  audience-advocate: Assumes Linux; add Windows/macOS tabs
        ...

    CROSS-BLOCK FINDINGS:
      [WARNING] style-consistency-checker: 4 blocks use different heading levels
      [WARNING] pedagogy-analyst: No summary block at end of Part 2
    ```
    """)

    show_details("Command Reference", """
    ```bash
    # Review all produced blocks
    /stx-ce:review

    # Review specific blocks only
    /stx-ce:review --blocks bck_start_welcome,bck_start_install

    # Review with specific agents only
    /stx-ce:review --agents pedagogy-analyst,content-editor

    # Show only critical findings
    /stx-ce:review --severity critical

    # Export review report as standalone file
    /stx-ce:review --export review-report.md
    ```

    The review report is saved to `.ce/review-report.md` and consumed by FIX.
    REVIEW is strictly **read-only** — it never modifies block files.
    """)
