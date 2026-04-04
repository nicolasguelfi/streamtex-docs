"""CE Manual — Part 2: Plan Versioning System."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details, show_code
except ImportError:
    from streamtex import show_explanation, show_details, show_code


class BlockStyles:
    """Plan Versioning styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Plan versioning: naming, change log, auto-detection, and task integration."""

    st_space("v", 1)
    st_write(bs.heading, "Plan Versioning",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "CE uses an ",
             (s.bold, "incremental versioning"),
             " strategy for production plans. Each modification creates a "
             "new file rather than overwriting the previous one. This preserves "
             "the full history of structural decisions and makes it possible "
             "to compare any two versions or roll back if needed.")
    st_space("v", 1)

    st_write(s.large,
             "Incremental versioning was chosen over append-only logs because "
             "plans are ", (s.bold, "living documents"),
             " that agents read as a whole. An agent processing the current "
             "plan should see a single, coherent file — not a base document "
             "plus a chain of patches to mentally reconstruct.")
    st_space("v", 1)

    # ── Naming Convention ─────────────────────────────────────────
    st_write(bs.sub, "Naming Convention", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "Plan files follow a strict naming pattern that encodes the "
             "creation date, a sequence number, and a human-readable name.")
    st_space("v", 1)

    show_code("""\
        docs/plans/
        ├── 2026-03-20-001-structure-plan.md     # Initial plan
        ├── 2026-03-22-002-structure-plan.md     # After interactive refinement
        ├── 2026-03-28-003-structure-plan.md     # After task added a block
        └── 2026-04-01-004-structure-plan.md     # After session resumption fix

        Format: YYYY-MM-DD-NNN-<name>.md
          YYYY-MM-DD  = creation date
          NNN         = sequence number (monotonically increasing)
          <name>      = plan type (structure-plan, task-sequence)
    """, language="text", line_numbers=False)
    st_space("v", 1)

    # ── Change Log Format ─────────────────────────────────────────
    st_write(bs.sub, "Change Log Format", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "Every plan version after the first includes a ",
             (s.project.titles.concept_kw, "Change Log"),
             " header that documents what changed and why.")
    st_space("v", 1)

    show_code("""\
        ---
        template: structure_plan
        project: stx_manual_ce
        date: 2026-03-28
        version: 003
        previous: 2026-03-22-002-structure-plan.md
        ---

        ## Change Log

        ### v003 <- v002 (2026-03-28)
        - **Added:** bck_ce_task (Part 2) — ad-hoc task documentation
        - **Added:** bck_ce_continue (Part 2) — session resumption
        - **Moved:** bck_ce_faq from Part 4 to Part 5
        - **Reason:** /stx-ce:task produce added 2 blocks mid-cycle

        ### v002 <- v001 (2026-03-22)
        - **Revised:** block ordering in Part 3 for better flow
        - **Removed:** bck_ce_deprecated_agents (content merged)
        - **Reason:** interactive plan refinement at Gate 2

        ## Structure
        ...
    """, language="markdown", line_numbers=False)
    st_space("v", 1)

    # ── Auto-Detection ────────────────────────────────────────────
    st_write(bs.sub, "Auto-Detection", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Latest by date + sequence = current plan

    CE agents never hardcode a plan filename. Instead, they scan the
    `docs/plans/` directory and select the file with the highest
    sequence number as the current plan.

    **Resolution algorithm:**
    1. List all files matching `YYYY-MM-DD-NNN-*.md` in `docs/plans/`
    2. Parse the sequence number (NNN) from each filename
    3. Select the file with the highest NNN value
    4. If two files share the same NNN (should not happen), use the
       latest date as tiebreaker

    This means you can safely keep old plan versions in the directory.
    They serve as history but never interfere with current operations.
    Agents always read exactly one plan: the latest.
    """)

    st_space("v", 1)

    # ── How Tasks Create Versions ─────────────────────────────────
    st_write(bs.sub, "How Tasks Create Versions", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Workflow when a task modifies the plan

    When a `/stx-ce:task` of archetype `produce` or `plan-update`
    needs to modify the plan, it follows this sequence:

    1. **Read** the current plan (highest sequence number)
    2. **Copy** the full content into a new file with NNN+1
    3. **Apply** the modification (add block, reorder, remove)
    4. **Prepend** a Change Log entry describing the delta
    5. **Update** the frontmatter (new date, new version, previous link)
    6. **Validate** that the new plan is internally consistent
       (all referenced blocks exist, no circular dependencies)
    7. **Save** the new version — it immediately becomes the current plan

    The old version remains untouched. If the task is later undone
    (e.g., the user rejects the gate), the old version is still
    available and can be restored by deleting the newer file.

    **Important:** Only `produce` and `plan-update` archetypes create
    new plan versions. Read-only archetypes (`review`, `analyze`,
    `coverage`, `capitalize`) never modify the plan.
    """)

    st_space("v", 1)

    # ── Comparison table ──────────────────────────────────────────
    show_details("""\
    ### Append-Only vs Incremental Versioning

    | Aspect | Append-Only | Incremental (CE approach) |
    |--------|-------------|--------------------------|
    | **File count** | 1 (grows over time) | N (one per version) |
    | **Reading cost** | Must replay all changes | Read one file |
    | **Agent complexity** | High (reconstruct state) | Low (read latest) |
    | **History** | Inline (scroll to find) | Explicit (file per version) |
    | **Diff** | Parse change entries | `diff` any two files |
    | **Rollback** | Undo last entries | Delete latest file |
    | **Merge conflicts** | Likely (single file) | Unlikely (new file) |
    | **Disk usage** | Lower (no duplication) | Higher (full copy per version) |

    The trade-off is disk usage vs simplicity. Since plans are small
    text files (typically under 10 KB), the duplication cost is
    negligible compared to the clarity gains.
    """)

    st_space("v", 1)
