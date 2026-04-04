"""CE Manual — Part 3: Task Agents — Ad-Hoc Reviewer and Extended Agents."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Task Agents styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Task agents: ad-hoc reviewer, gap analyst, learnings researcher."""

    st_space("v", 1)
    st_write(bs.heading, "Task Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.tool_kw, "/stx-ce:task"),
             " command activates specialized agents that extend the standard "
             "CE agent roster. These agents are designed for ",
             (s.bold, "scoped, on-demand operations"),
             " rather than full-pipeline phases. They share the same artifact "
             "format and severity conventions as the built-in agents but operate "
             "on a narrower focus defined by the task description.")
    st_space("v", 1)

    # ── Ad-Hoc Reviewer ──────────────────────────────────────────
    st_write(bs.sub, "Ad-Hoc Reviewer", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### What it does

    The ad-hoc reviewer is a single-perspective reviewer that evaluates
    blocks through the lens specified in the task description. Unlike the
    5 built-in reviewers (audience, pedagogy, visual, style, content),
    the ad-hoc reviewer focuses on **one user-defined concern**.

    **How it differs from built-in reviewers:**
    - Built-in reviewers run all 5 perspectives automatically
    - The ad-hoc reviewer runs exactly 1 perspective, defined by you
    - It can target a subset of blocks (not necessarily all)
    - It produces a `task-review.md` artifact (not `review-report.md`)
    - It can check for things the built-in reviewers do not cover
      (e.g., citation accuracy, regulatory compliance, brand voice)

    **Examples of custom perspectives:**
    - "Check that all code examples are runnable"
    - "Verify accessibility of image alt-texts"
    - "Ensure GDPR-related disclaimers are present"
    """)

    st_space("v", 1)

    show_details("""\
    ### Input / Output Format

    **Input:**
    - Task description (the review focus)
    - Block files (all, or a filtered subset)
    - Existing review reports (for context, not re-evaluation)

    **Output: `task-review.md`**
    ```
    ---
    template: task_review
    task: "Check citation accuracy in all blocks"
    date: 2026-04-01
    blocks_reviewed: 12
    ---

    ## Findings

    | ID | Block | Line | Severity | Category | Issue |
    |----|-------|------|----------|----------|-------|
    | T001 | bck_ce_overview | 45 | MAJOR | citation | Missing source for claim |
    | T002 | bck_ce_plan | 78 | MINOR | citation | Author name misspelled |
    | T003 | bck_ce_produce | 112 | CRITICAL | citation | Dead URL reference |

    ## Summary
    - CRITICAL: 1
    - MAJOR: 1
    - MINOR: 1
    - SUGGESTION: 0
    - Total: 3 findings across 12 blocks
    ```

    **Severity levels** follow the same scale as built-in reviewers:
    CRITICAL > MAJOR > MINOR > SUGGESTION.
    """)

    st_space("v", 1)

    # ── Gap Analyst ───────────────────────────────────────────────
    st_write(bs.sub, "Gap Analyst — Bidirectional Mode", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Forward and Reverse Coverage

    The gap analyst operates in two directions:

    **Forward (source -> blocks):** For each source item in the collect
    inventory, checks whether corresponding content exists in the
    produced blocks. Answers: "Is all source material covered?"

    **Reverse (blocks -> source):** For each produced block, checks
    whether it traces back to a source item. Answers: "Is all produced
    content grounded in sources?"

    **Why bidirectional matters:**
    - Forward-only misses "orphan blocks" — content that was invented
      without a source basis (acceptable in pathway C, problematic in A/B)
    - Reverse-only misses "dropped content" — source material that was
      skipped or forgotten during production
    - Together, they give a complete fidelity picture

    The gap analyst is activated by the `coverage` archetype in
    `/stx-ce:task coverage "description"`.
    """)

    st_space("v", 1)

    show_details("""\
    ### Coverage Matrix Format

    The gap analyst produces a `coverage-matrix.md` artifact:

    | Source Item | Status | Block(s) | Fidelity |
    |-------------|--------|----------|----------|
    | `slides/ch1.pdf` pp.1-5 | COVERED | bck_intro_welcome | HIGH |
    | `slides/ch1.pdf` pp.6-10 | PARTIAL | bck_intro_scope | MEDIUM |
    | `slides/ch2.pdf` pp.1-8 | MISSING | — | — |
    | `notes/errata.md` | SKIPPED | — | N/A (out of scope) |

    **Reverse section:**

    | Block | Source(s) | Grounded? |
    |-------|-----------|-----------|
    | bck_intro_welcome | slides/ch1.pdf pp.1-5 | YES |
    | bck_intro_summary | — | NO (original content) |

    **Status values:** COVERED, PARTIAL, MISSING, SKIPPED
    **Fidelity values:** HIGH (faithful), MEDIUM (adapted), LOW (loosely inspired)
    """)

    st_space("v", 1)

    # ── Learnings Researcher ──────────────────────────────────────
    st_write(bs.sub, "Learnings Researcher — Targeted Mode", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Topic-Based Search for Deduplication

    The learnings researcher scans existing solution packages in
    `docs/solutions/` and producer profile entries in `docs/profile.md`
    to determine whether a new insight is genuinely novel or duplicates
    something already captured.

    **When it activates:** The `capitalize` archetype calls the learnings
    researcher before creating a new solution package. This prevents
    the solutions folder from accumulating redundant entries.

    **How it works:**
    1. Takes the topic description from the task
    2. Searches existing solutions by title, tags, and content
    3. Searches the producer profile for related conventions
    4. Returns a similarity report:
       - **NOVEL** — no match found, safe to create
       - **SIMILAR** — related entry exists, suggest merging
       - **DUPLICATE** — near-identical entry exists, skip creation

    **On SIMILAR results:** The researcher presents both the existing
    entry and the new insight side by side, letting the user decide
    whether to merge, replace, or keep both.

    **On DUPLICATE results:** The researcher skips creation and logs
    the dedup decision in the task report for traceability.
    """)

    st_space("v", 1)
