"""CE Manual — Part 2: COMPOUND Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """COMPOUND phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """COMPOUND phase: capitalization, ecosystem feedback, governance."""

    st_space("v", 1)
    st_write(bs.heading, "COMPOUND — Capitalize and Feed the Ecosystem",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "COMPOUND"),
             " phase closes the iteration by extracting value from the "
             "production process itself. It operates along four axes: production "
             "capitalization (including pattern catalog enrichment), ecosystem feedback, "
             "development governance, and master plan maintenance (including partial purge of snapshots).")
    st_space("v", 1)

    st_write(s.large,
             (s.project.titles.phase_kw, "COMPOUND"),
             " ensures that every CE cycle makes the next one faster and better.")
    st_space("v", 1)

    show_explanation("""\
    ### Axis 1: Production Capitalization

    The **producer profile** captures reusable knowledge from the cycle.

    **What is capitalized:**
    - Block templates that worked well (extracted as reusable patterns)
    - Style decisions that proved effective
    - Content structures that matched the audience
    - Import mappings (source format to StreamTeX patterns)

    **The Producer Profile** (`docs/profile.md`):
    ```
    ---
    template: producer_profile
    author: <name>
    last_updated: <date>
    cycles_completed: <count>
    ---

    ## Writing Style
    - Tone: semi-formal
    - Sentence length: medium
    - Example frequency: every-concept

    ## Structural Preferences
    - Max block length: 120
    - Preferred block types: show_explanation, show_details, tabs
    - Part size: 4-6 blocks per part

    ## Lessons Learned
    - 2026-03-01: tabs-by-language pattern works well for install blocks
    - 2026-03-15: preserve-hierarchy for HTML imports
    ```

    The profile grows across cycles. After 3-5 projects, production speed
    increases measurably because the CE engine reuses proven patterns.
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Axis 2: Ecosystem Feedback

    Issues discovered during production are fed back to the StreamTeX
    ecosystem via `/stx-issue:*` ticket submission.

    **Ticket types:**

    | Type | Example | Target |
    |------|---------|--------|
    | **Bug** | Import pipeline fails on nested tables | streamtex library |
    | **Feature** | Need `st_accordion` widget | streamtex library |
    | **Doc** | Missing example for `st_tabs` nesting | streamtex-docs |
    | **Profile** | Style rule conflict in presentation mode | streamtex-claude |

    **Automatic detection:**
    - Import failures generate bug tickets automatically
    - Missing API coverage is detected during PRODUCE
    - Style conflicts found during REVIEW become profile tickets

    Tickets include full reproduction context (block file, error trace,
    environment info) so they can be acted on without back-and-forth.
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Axis 3: Dev Governance

    COMPOUND manages the development branch lifecycle for the project.

    **Branch management:**
    ```
    main  ----+-----------------------------+---> (stable)
              |                             |
              +-- ce/cycle-001 --+-- merge -+
                                 |
              COLLECT -> ... -> COMPOUND
    ```

    **What COMPOUND does:**
    1. Commits all produced and fixed blocks with structured messages
    2. Generates a cycle summary (blocks created, imported, improved)
    3. Creates a pull request (or merges directly if `--auto-merge`)
    4. Tags the release with cycle metadata
    5. Cleans up working files (`.ce/` reports, temp files)

    **Commit message format:**
    ```
    ce(cycle-001): PRODUCE bck_intro_welcome [CREATE]
    ce(cycle-001): FIX bck_start_install [CRITICAL] add BlockStyles
    ce(cycle-001): COMPOUND cycle complete (24 blocks, 3 iterations)
    ```
    """)

    st_space("v", 1)

    show_explanation("""\
    ### Axis 4: Master Plan Maintenance

    The fourth axis updates the **master plan** to reflect what was produced
    and learned during the iteration, so subsequent iterations resume from
    an accurate snapshot.

    **What happens in Axis 4:**

    1. **Iteration outcome** — append an entry under `master-plan.yaml -> iterations[<current>]`
       summarising the scope, the blocks produced, the patterns captured/promoted, and the
       reviewer findings synthesis.
    2. **Objectives status** — the `objective-monitor` agent updates the `status` of each
       objective in `master-plan.yaml -> objectives[*]` based on the iteration outcome
       (free-text judgment, not metrics).
    3. **Pattern catalog promotion** — patterns captured at the local level during PROTOTYPE
       or PRODUCE that have been validated in real blocks are confirmed in
       `master-plan.yaml -> patterns.applied` with `level: local`.
    4. **Snapshot housekeeping** — the master plan paired snapshot policy keeps every
       snapshot by default. COMPOUND surfaces a QCM proposing a partial purge if the
       number of snapshots exceeds a useful threshold (typically > 20). User decision
       via the universal QCM.

    All Axis-4 changes are captured as new entries in `master-plan.yaml -> decisions_log`.
    """)

    st_space("v", 1)

    show_details("""\
    ### Command Reference

    ```bash
    # Run full COMPOUND phase
    /stx-ce:compound

    # Capitalize only (no git operations)
    /stx-ce:compound --capitalize-only

    # Submit ecosystem tickets only
    /stx-ce:compound --feedback-only

    # Auto-merge to main
    /stx-ce:compound --auto-merge

    # Skip cleanup (keep .ce/ reports)
    /stx-ce:compound --keep-reports
    ```

    COMPOUND marks the end of the CE cycle. The project is ready for
    deployment or the next cycle iteration.
    """)

    st_space("v", 1)

    show_explanation("""\
    ### When CE captures grow beyond a single project: escalate to PE

    The COMPOUND phase captures patterns into the project's **primary
    local pack** (`./mypack/components/`). Over time, the same patterns
    tend to re-emerge across multiple projects. When this happens, the
    natural next step is **Pack Engineering (PE)** — the orchestrated
    lifecycle that takes N projects and produces (or evolves) a shared
    pack across all of them.

    **When to escalate from CE to PE:**

    - Three or more projects share the same captured pattern → run
      `/stx-pe:bootstrap projects/*` to extract a shared pack.
    - An existing upstream pack (e.g. `streamtex-design`) almost fits
      but lacks your domain specifics → run `/stx-pe:specialize <upstream>
      projects/*` to fork.
    - One project's local pack has been used for a while and new idioms
      have emerged in recent blocks → run `/stx-pe:refine` to capture
      only the new patterns.

    PE delegates to the single user-facing `pack-orchestrator` agent
    and surfaces 4 validation gates (G1-G4). See the **Reuse Architecture
    manual** (Part 5bis: Pack Engineering) for the full walkthrough, or
    `.claude/references/pe_cheatsheet_en.md` for the command reference.

    Indirect routing: `/stx-ce:task "extract a shared pack from
    projects A B C"` auto-classifies into `PACK_BOOTSTRAP` and routes to
    the orchestrator without needing to remember the `/stx-pe:*` namespace.
    """)

    st_space("v", 1)
