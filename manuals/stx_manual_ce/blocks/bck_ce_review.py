"""CE Manual — Part 2: REVIEW Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """REVIEW phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """REVIEW phase: 5 parallel agents, severity levels, read-only."""

    st_space("v", 1)
    st_write(bs.heading, "REVIEW — Multi-Agent Quality Evaluation",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "REVIEW"),
             " phase performs a comprehensive, ",
             (s.bold, "read-only"),
             " evaluation of all produced blocks. Five specialized agents work in parallel, each "
             "analyzing the content from a different perspective. No modifications are "
             "made during ",
             (s.project.titles.phase_kw, "REVIEW"),
             " — all findings are recorded in a review report for the ",
             (s.project.titles.phase_kw, "FIX"),
             " phase.")
    st_space("v", 1)

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

    st_space("v", 1)

    show_explanation("Severity Levels", """
    Every finding is tagged with a severity level:

    **blocker** — Must be fixed before delivery
    - Broken imports or render errors
    - Factually incorrect content
    - Missing blocks referenced in navigation
    - Accessibility violations

    **major** — Should be fixed, but not blocking
    - Inconsistent style across blocks
    - Suboptimal pedagogical flow
    - Missing `show_details()` for optional content
    - Overly long blocks (>150 lines)

    **minor** — Small improvement opportunity
    - Alternative widget choices
    - Additional examples that could help
    - Minor wording improvements

    **suggestion** — Stylistic or optional improvement
    - Cosmetic layout tweaks
    - Alternative approaches worth considering

    The FIX phase processes blocker items first, then majors. Minor items
    are optional and applied only if `--thorough` is specified.
    """)

    st_space("v", 1)

    show_explanation("Review Report Structure", """
    ```
    === CE REVIEW REPORT ===
    Project: my-training-course
    Blocks reviewed: 24
    Total findings: 47

    SUMMARY:
      blocker    ...  3 findings (must fix)
      major      ... 18 findings (should fix)
      minor      ... 16 findings (fix if time permits)
      suggestion ... 10 findings (optional)

    PER-BLOCK FINDINGS:
      bck_start_welcome (3 findings):
        [blocker]    content-editor: Missing introduction paragraph
        [major]      visual-reviewer: Hero banner has no fallback text
        [suggestion] pedagogy-analyst: Consider adding a "what you'll learn" list

      bck_start_install (5 findings):
        [blocker] style-consistency-checker: Missing BlockStyles class
        [major]   audience-advocate: Assumes Linux; add Windows/macOS tabs
        ...

    CROSS-BLOCK FINDINGS:
      [major] style-consistency-checker: 4 blocks use different heading levels
      [major] pedagogy-analyst: No summary block at end of Part 2
    ```
    """)

    st_space("v", 1)

    show_details("Command Reference", """
    ```bash
    # Review all produced blocks
    /stx-ce:review

    # Review specific blocks only
    /stx-ce:review --blocks bck_start_welcome,bck_start_install

    # Review with specific agents only
    /stx-ce:review --agents pedagogy-analyst,content-editor

    # Show only blocker findings
    /stx-ce:review --severity blocker

    # Export review report as standalone file
    /stx-ce:review --export review-report.md
    ```

    The review report is saved to `docs/review.md` and consumed by FIX.
    REVIEW is strictly **read-only** — it never modifies block files.
    """)

    st_space("v", 1)
