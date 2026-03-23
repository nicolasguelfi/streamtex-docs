"""CE Manual — Part 2: COLLECT Phase."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the COLLECT phase block."""
    title = s.part_title if hasattr(s, "part_title") else {}
    phase = s.phase if hasattr(s, "phase") else {}


def build():
    """COLLECT phase: scan sources, classify, evaluate importability."""

    st_write("""
    ## COLLECT — Gather and Classify Source Material

    The **COLLECT** phase is the entry point of every CE cycle. Its purpose is to
    systematically scan all available sources, classify their content, and evaluate
    what can be imported into the target StreamTeX project.

    This phase runs **automatically** when `/stx-ce:go` is invoked, or can be
    triggered independently with `/stx-ce:collect`.
    """)

    show_explanation("The 4 Sub-Phases of COLLECT", """
    COLLECT operates through four sequential sub-phases:

    **1. SOURCE SCAN** — Enumerate all input sources
    - Local files (PDF, DOCX, PPTX, HTML, Markdown)
    - Existing StreamTeX projects and blocks
    - URLs and external references provided by the user

    **2. CONTENT CLASSIFICATION** — Categorize each source item
    - **Importable**: content that maps directly to StreamTeX blocks
    - **Adaptable**: content requiring transformation (e.g., HTML slides)
    - **Reference-only**: material for inspiration, not direct import
    - **Out-of-scope**: irrelevant to the current project

    **3. IMPORT ASSESSMENT** — Evaluate importability of each item
    - Structural compatibility with StreamTeX patterns
    - Content quality and completeness
    - Effort estimate (low / medium / high)

    **4. COLLECT REPORT** — Produce a structured summary for the next phase
    """)

    show_explanation("Specialized Agents", """
    Three agents collaborate during COLLECT:

    | Agent | Role |
    |-------|------|
    | **source-scanner** | Discovers and inventories all available material |
    | **import-assessor** | Evaluates structural fit and import effort |
    | **content-strategist** | Classifies items and recommends a collection strategy |

    Each agent writes its findings into the shared collect report. The
    content-strategist has final authority on classification decisions.
    """)

    show_details("Example Collect Report Output", """
    ```
    === CE COLLECT REPORT ===
    Project: my-training-course
    Sources scanned: 3 directories, 2 URLs, 1 existing project
    Total items found: 47

    CLASSIFICATION SUMMARY:
      Importable ......... 18 items (38%)
      Adaptable .......... 12 items (26%)
      Reference-only .....  9 items (19%)
      Out-of-scope .......  8 items (17%)

    TOP CANDIDATES FOR IMPORT:
      [IMP-01] slides/chapter1.pptx  -> 6 blocks, effort: LOW
      [IMP-02] docs/guide.md         -> 4 blocks, effort: LOW
      [IMP-03] website/tutorial.html  -> 8 blocks, effort: MEDIUM

    ITEMS REQUIRING ADAPTATION:
      [ADP-01] legacy/old-course.pdf  -> ~10 blocks, effort: HIGH
      [ADP-02] notes/handout.docx     -> 3 blocks, effort: MEDIUM

    Next phase: ASSESS (auto-detect pathway)
    ```
    """)

    show_details("Command Reference", """
    ```bash
    # Run COLLECT independently
    /stx-ce:collect

    # COLLECT with explicit source directories
    /stx-ce:collect --sources ./slides ./docs

    # COLLECT with URL scanning
    /stx-ce:collect --url https://example.com/course

    # Skip already-collected items (incremental mode)
    /stx-ce:collect --incremental
    ```

    The collect report is saved to `.ce/collect-report.md` and is consumed
    by the ASSESS phase.
    """)
