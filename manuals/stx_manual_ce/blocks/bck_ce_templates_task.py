"""CE Manual — Part 5: Task Templates Reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_details, show_code
except ImportError:
    from streamtex import show_details, show_code


class BlockStyles:
    """Task Templates styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Reference for the 4 task-specific templates."""

    st_space("v", 1)
    st_write(bs.heading, "Task Templates",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.tool_kw, "/stx-ce:task"),
             " command produces artifacts using ",
             (s.bold, "4 dedicated templates"),
             ". These templates complement the 12 standard CE templates "
             "and follow the same conventions: YAML frontmatter, required "
             "and optional sections, and machine-readable formatting for "
             "downstream agents.")
    st_space("v", 1)

    # ── task-review.md ────────────────────────────────────────────
    st_write(bs.sub, "task-review.md", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Template Structure

    **Frontmatter fields:**
    - `template`: `task_review` (fixed)
    - `task`: the task description string
    - `date`: creation timestamp
    - `blocks_reviewed`: number of blocks examined
    - `perspective`: the custom review focus

    **Required sections:**
    - **Findings** — Table with columns: ID, Block, Line, Severity, Category, Issue
    - **Summary** — Count of findings per severity level

    **Optional sections:**
    - **Recommendations** — Prioritized list of suggested fixes
    - **Comparison** — Delta with previous review (if one exists)
    """)

    st_space("v", 1)

    show_code("""\
        ---
        template: task_review
        task: "Verify citation accuracy"
        date: 2026-04-01
        blocks_reviewed: 14
        perspective: citation-accuracy
        ---

        ## Findings

        | ID | Block | Line | Severity | Category | Issue |
        |----|-------|------|----------|----------|-------|
        | T001 | bck_overview | 45 | CRITICAL | citation | Dead URL: example.com/old |
        | T002 | bck_plan | 78 | MAJOR | citation | Missing publication year |
        | T003 | bck_review | 23 | MINOR | citation | Author last name only |

        ## Summary
        - CRITICAL: 1
        - MAJOR: 1
        - MINOR: 1
        - SUGGESTION: 0
        - Total: 3 findings across 14 blocks

        ## Recommendations
        1. Fix T001 immediately (dead link blocks publication)
        2. Add year to T002 reference (check source PDF page 3)
        3. Expand T003 author name when full name is available
    """, language="markdown", line_numbers=False)

    st_space("v", 1)

    # ── coverage-matrix.md ────────────────────────────────────────
    st_write(bs.sub, "coverage-matrix.md", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Template Structure

    **Frontmatter fields:**
    - `template`: `coverage_matrix` (fixed)
    - `task`: the task description string
    - `date`: creation timestamp
    - `sources_count`: number of source items evaluated
    - `blocks_count`: number of blocks evaluated
    - `coverage_pct`: overall coverage percentage

    **Required sections:**
    - **Forward Matrix** — Source -> Block mapping with status and fidelity
    - **Reverse Matrix** — Block -> Source mapping with grounding check
    - **Coverage Summary** — Aggregate statistics

    **Optional sections:**
    - **Gap Analysis** — Detailed notes on MISSING/PARTIAL items
    - **Recommendations** — Suggested actions to close gaps
    """)

    st_space("v", 1)

    show_code("""\
        ---
        template: coverage_matrix
        task: "Compare lecture notes with produced blocks"
        date: 2026-04-01
        sources_count: 8
        blocks_count: 12
        coverage_pct: 82
        ---

        ## Forward Matrix (Source -> Blocks)

        | Source Item | Status | Block(s) | Fidelity |
        |-------------|--------|----------|----------|
        | lecture-01.pdf pp.1-12 | COVERED | bck_intro, bck_basics | HIGH |
        | lecture-01.pdf pp.13-20 | PARTIAL | bck_basics | MEDIUM |
        | lecture-02.pdf pp.1-15 | COVERED | bck_advanced | HIGH |
        | lecture-03.pdf | MISSING | — | — |
        | notes/errata.md | SKIPPED | — | N/A |

        ## Reverse Matrix (Blocks -> Source)

        | Block | Source(s) | Grounded? |
        |-------|-----------|-----------|
        | bck_intro | lecture-01.pdf pp.1-8 | YES |
        | bck_summary | — | NO (original) |

        ## Coverage Summary
        - Sources: 8 total, 5 covered, 1 partial, 1 missing, 1 skipped
        - Blocks: 12 total, 11 grounded, 1 original
        - Overall coverage: 82%
    """, language="markdown", line_numbers=False)

    st_space("v", 1)

    # ── task-analysis.md ──────────────────────────────────────────
    st_write(bs.sub, "task-analysis.md", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Template Structure

    **Frontmatter fields:**
    - `template`: `task_analysis` (fixed)
    - `task`: the task description string
    - `date`: creation timestamp
    - `scope`: what was analyzed (sources, blocks, or both)

    **Required sections:**
    - **Themes** — Major themes identified with frequency counts
    - **Statistics** — Quantitative summary (word counts, section counts, etc.)

    **Optional sections:**
    - **Citations** — Bibliography entries found in the analyzed content
    - **Key Concepts** — Glossary of domain terms with definitions
    - **Relationships** — Concept graph or dependency map
    """)

    st_space("v", 1)

    show_code("""\
        ---
        template: task_analysis
        task: "Summarize key themes across source files"
        date: 2026-04-01
        scope: sources
        ---

        ## Themes

        | # | Theme | Frequency | Sources |
        |---|-------|-----------|---------|
        | 1 | Container orchestration | 23 mentions | ch1, ch3, ch5 |
        | 2 | Security hardening | 18 mentions | ch2, ch4 |
        | 3 | Monitoring & observability | 15 mentions | ch5, ch6 |
        | 4 | CI/CD pipelines | 12 mentions | ch3, ch7 |

        ## Statistics
        - Total sources analyzed: 7
        - Combined word count: ~45,000
        - Unique technical terms: 89
        - Code examples found: 34

        ## Key Concepts
        - **Pod**: smallest deployable unit in Kubernetes
        - **Sidecar**: helper container sharing a pod's network namespace
        - **Ingress**: API object managing external access to services

        ## Citations
        - Burns, B. (2018). "Kubernetes: Up and Running". O'Reilly.
        - Hausenblas, M. (2019). "Programming Kubernetes". O'Reilly.
    """, language="markdown", line_numbers=False)

    st_space("v", 1)

    # ── task-report.md ────────────────────────────────────────────
    st_write(bs.sub, "task-report.md", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Template Structure

    **Frontmatter fields:**
    - `template`: `task_report` (fixed)
    - `task`: the task description string
    - `archetype`: which archetype was used
    - `date`: creation timestamp
    - `duration`: execution time
    - `gate_outcome`: approved | dismissed | auto-passed | skipped

    **Required sections:**
    - **Actions** — Ordered list of actions performed
    - **Artifacts** — Files created or modified with paths

    **Optional sections:**
    - **Cycle Impact** — How this task affected the CE cycle state
    - **Next Steps** — Recommended follow-up actions
    - **Gate Log** — Details of gate evaluation if triggered
    """)

    st_space("v", 1)

    show_code("""\
        ---
        template: task_report
        task: "Add block about error handling after bck_api_basics"
        archetype: produce
        date: 2026-04-01
        duration: 3m 42s
        gate_outcome: approved
        ---

        ## Actions
        1. Read current plan (2026-03-28-003-structure-plan.md)
        2. Identified insertion point: after bck_api_basics (Part 2, position 4)
        3. Created block file: blocks/bck_api_error_handling.py
        4. Versioned plan: 2026-04-01-004-structure-plan.md
        5. Updated book.py: registered block at position 5 in Part 2
        6. Gate triggered (always mode) — user approved

        ## Artifacts
        - Created: `blocks/bck_api_error_handling.py`
        - Created: `docs/plans/2026-04-01-004-structure-plan.md`
        - Modified: `book.py` (block registration)
        - Created: `docs/reports/task-report-2026-04-01.md` (this file)

        ## Cycle Impact
        - Plan version: 003 -> 004
        - Block count: 18 -> 19
        - Next review should include the new block

        ## Next Steps
        - Run `/stx-ce:review --blocks bck_api_error_handling` to review new block
        - Consider `/stx-ce:task coverage` to verify source coverage still holds
    """, language="markdown", line_numbers=False)

    st_space("v", 1)
