"""CE Manual — Part 2: /stx-ce:task Ad-Hoc Task Command."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details, show_code
except ImportError:
    from streamtex import show_explanation, show_details, show_code


class BlockStyles:
    """/stx-ce:task styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """/stx-ce:task — ad-hoc tasks outside the linear pipeline."""

    st_space("v", 1)
    st_write(bs.heading, "Ad-Hoc Tasks",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.tool_kw, "/stx-ce:task"),
             " command executes a ",
             (s.bold, "focused, single-purpose operation"),
             " within an existing CE cycle. Unlike ",
             (s.project.titles.tool_kw, "/stx-ce:go"),
             " which runs the full pipeline, ",
             (s.project.titles.tool_kw, "/stx-ce:task"),
             " targets one specific need: auditing coverage, reviewing "
             "citations, adding a block mid-cycle, or extracting a pattern.")
    st_space("v", 1)

    st_write(s.large,
             "Tasks are the right tool when the full pipeline is overkill. "
             "They read existing CE artifacts, perform a scoped action, "
             "and reconcile their output back into the cycle state.")
    st_space("v", 1)

    show_explanation("""\
    ### When to use /stx-ce:task vs /stx-ce:go

    **Use /stx-ce:task when:**
    - You need a single, focused operation (audit, review, add, extract)
    - The cycle is already running and you want to intervene
    - You want to inspect or analyze without modifying production flow
    - You need to add a block that was not in the original plan

    **Use /stx-ce:go when:**
    - You are starting a new document from scratch
    - You want the full COLLECT-to-COMPOUND pipeline
    - You need all 3 validation gates
    - You are doing a bulk import or major restructuring

    **Decision tree:**
    ```
    Need full pipeline?
      YES -> /stx-ce:go
      NO  -> Is it a single operation?
               YES -> /stx-ce:task <archetype> "description"
               NO  -> /stx-ce:task composite "A then B"
    ```
    """)

    st_space("v", 1)

    # ── 6 Task Archetypes ─────────────────────────────────────────
    st_write(bs.sub, "6 Task Archetypes", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "Every task maps to one of six ",
             (s.project.titles.concept_kw, "archetypes"),
             ". Each archetype defines the agents involved, the artifact "
             "produced, and the gate behavior.")
    st_space("v", 1)

    show_details("""\
    ### Archetype Summary

    | Archetype | Triggers | Artifact | Gate |
    |-----------|----------|----------|------|
    | **review** | "audit", "check", "review" | `task-review.md` | auto |
    | **coverage** | "coverage", "gap", "compare" | `coverage-matrix.md` | auto |
    | **produce** | "add", "create", "insert" | new block file(s) | always |
    | **analyze** | "analyze", "extract", "summarize" | `task-analysis.md` | never |
    | **plan-update** | "update plan", "revise", "reschedule" | new plan version | always |
    | **capitalize** | "pattern", "learn", "capitalize" | solution package | auto |
    """)

    st_space("v", 1)

    st_write(s.large + s.bold, "review — Targeted quality check")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task review "Check citation accuracy in all blocks"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "coverage — Source-to-block gap analysis")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task coverage "Compare lecture notes with produced blocks"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "produce — Add content mid-cycle")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task produce "Add a block about error handling patterns"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "analyze — Extract insights without modifying")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task analyze "Summarize key themes across all source files"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "plan-update — Revise the production plan")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task plan-update "Add security section after chapter 3"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "capitalize — Extract a reusable pattern")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task capitalize "Document the two-column comparison layout"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    # ── Composite Tasks ───────────────────────────────────────────
    st_write(bs.sub, "Composite Tasks", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### How multiple archetypes combine

    A composite task chains two or more archetypes in sequence.
    The output of each step feeds into the next. CE automatically
    detects composite intent from the task description and splits
    it into ordered sub-tasks.

    **Chaining rules:**
    - Each sub-task runs its own archetype logic independently
    - Artifacts from earlier sub-tasks are available to later ones
    - Gates are evaluated per sub-task (not once for the whole chain)
    - If any sub-task fails its gate, the chain pauses at that point

    **Common compositions:**
    - `coverage` then `produce` — find gaps, then fill them
    - `analyze` then `capitalize` — extract themes, then package patterns
    - `review` then `plan-update` — find issues, then adjust the plan
    """)

    st_space("v", 0.5)
    show_code("""\
        /stx-ce:task composite "Check source coverage, then add missing blocks"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    # ── Lifecycle Reconciliation ──────────────────────────────────
    st_write(bs.sub, "Lifecycle Reconciliation", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "When a task modifies the project (adding blocks, updating the plan), "
             "its changes must be ",
             (s.bold, "reconciled"),
             " with the existing CE cycle state. This ensures that "
             "subsequent phases see a consistent picture.")
    st_space("v", 1)

    show_details("""\
    ### Reconciliation Rules

    | Task Archetype | Modifies Plan? | Modifies Blocks? | Reconciliation Action |
    |----------------|---------------|------------------|----------------------|
    | **review** | No | No | Findings appended to `docs/reviews/` |
    | **coverage** | No | No | Matrix saved to `docs/collect/` |
    | **produce** | Yes (adds entry) | Yes (new file) | Plan versioned, block registered |
    | **analyze** | No | No | Analysis saved to `docs/assess/` |
    | **plan-update** | Yes (new version) | No | Plan versioned with change log |
    | **capitalize** | No | No | Solution saved to `docs/solutions/` |

    **Version propagation:** When a task creates a new plan version,
    subsequent `/stx-ce:produce` or `/stx-ce:review` commands automatically
    pick up the latest version. No manual re-linking is required.

    **Block registration:** When a `produce` task adds a new block,
    it updates both the plan (adds the block entry) and `book.py`
    (registers the block in the appropriate position).
    """)

    st_space("v", 1)

    # ── Conditional Gate ──────────────────────────────────────────
    st_write(bs.sub, "Conditional Gate", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Task Gate Behavior

    Each archetype has a default gate mode that controls whether
    user approval is required before the task commits its changes.

    **Gate modes:**

    - **auto** — The gate activates only when findings exceed a
      severity threshold. For `review`, the gate triggers if any
      CRITICAL finding is detected. For `coverage`, it triggers
      if coverage drops below 70%. Otherwise the task completes
      silently.

    - **always** — The gate always pauses for user approval.
      Used by `produce` (new content must be reviewed) and
      `plan-update` (plan changes are structural decisions).

    - **never** — No gate. The task runs to completion without
      pausing. Used by `analyze` which is read-only and produces
      no side effects.

    **Overriding the default:**
    ```bash
    # Force gate on an analyze task
    /stx-ce:task analyze --gate=always "Summarize themes"

    # Skip gate on a produce task (use with caution)
    /stx-ce:task produce --gate=never "Add glossary block"
    ```

    Gate overrides are logged in the task report for traceability.
    """)

    st_space("v", 1)
