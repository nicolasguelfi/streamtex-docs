"""CE Manual — Part 2: /stx-ce:pause Session Checkpoint."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details, show_code
except ImportError:
    from streamtex import show_explanation, show_details, show_code


class BlockStyles:
    """/stx-ce:pause styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """/stx-ce:pause — session checkpoint before pausing work."""

    st_space("v", 1)
    st_write(bs.heading, "Session Checkpoint",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "When working on a CE cycle across multiple sessions, "
             "the conversational context — decisions made, blocks in progress, "
             "pending issues — is lost between sessions. The ",
             (s.project.titles.tool_kw, "/stx-ce:pause"),
             " command creates a ",
             (s.bold, "checkpoint file"),
             " that captures this ephemeral context, enabling effective "
             "resumption via ",
             (s.project.titles.tool_kw, "/stx-ce:continue"),
             ".")
    st_space("v", 1)

    st_write(s.large,
             "Without a checkpoint, ",
             (s.project.titles.tool_kw, "/stx-ce:continue"),
             " can detect ",
             (s.italic, "what"),
             " changed (drift detection), but not ",
             (s.italic, "why"),
             " it changed or what was being worked on. The checkpoint "
             "bridges this gap.")
    st_space("v", 1)

    show_code("""\
        /stx-ce:pause
        /stx-ce:pause --message "Focus was on LLM blocks 6-12"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    # ── The Pause/Continue Cycle ─────────────────────────────────
    st_write(bs.sub, "The Pause / Continue Cycle", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
    ### Workflow

    ```
    Session 1:                     Session 2:
    ┌─────────────────────┐       ┌──────────────────────┐
    │ Work on CE cycle... │       │ /stx-ce:continue     │
    │ /stx-ce:produce     │       │   ↓                  │
    │ /stx-ce:task "..."  │       │ Checkpoint restored   │
    │ manual edits        │       │ from 2026-04-04       │
    │   ↓                 │       │   ↓                  │
    │ /stx-ce:pause       │──────>│ Briefing + drift     │
    │   ↓                 │       │   ↓                  │
    │ docs/ce-checkpoint.md│      │ Proposals (with       │
    │   ↓                 │       │  checkpoint items)    │
    │ git commit (optional)│      │   ↓                  │
    └─────────────────────┘       │ Resume work          │
                                  └──────────────────────┘
    ```

    The checkpoint is **archived** after restoration (renamed to
    `ce-checkpoint-YYYY-MM-DD.md`), preventing stale checkpoints
    from being loaded in future sessions.
    """)

    st_space("v", 1)

    # ── What the Checkpoint Captures ─────────────────────────────
    st_write(bs.sub, "What the Checkpoint Captures", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
    ### Checkpoint Contents

    | Section | Purpose |
    |---------|---------|
    | **Active Work Items** | Blocks being worked on, their state, what remains |
    | **Decisions Log** | Design choices, scope decisions, plan deviations |
    | **Pending Issues** | Known problems, blockers, missing assets |
    | **Uncommitted Changes** | Summary of git status at checkpoint time |
    | **Context for Next Session** | Free-text briefing for the next session |

    The **Decisions Log** is the most valuable section — it captures
    reasoning that is not present in the code or artifacts. For example:
    "Chose 2-column grid instead of 3 because the content is too dense"
    or "Skipped bibliography for now, will add in next pass."
    """)

    st_space("v", 1)

    show_code("""\
        # CE Session Checkpoint
        ---
        project: ai4se6d_genai_intro
        checkpoint_date: 2026-04-04T17:30:00
        current_plan: docs/plans/2026-04-04-001-C-session1-plan.md
        current_phase: PRODUCE
        phase_progress: PRODUCE 8/12 blocks
        ---

        ## Active Work Items
        - [ ] bck_llm_training.py — IN PROGRESS: refactoring to 3-col grid
        - [ ] bck_llm_embeddings.py — INCOMPLETE: mermaid diagram TODO
        - [x] bck_glossary.py — DONE this session (out-of-plan)

        ## Decisions Log
        1. Chose blue/violet palette (cohérence with existing slides)
        2. Glossary added at end of book.py (not in original plan)
        3. Simplified bck_llm_attention — removed math formulas

        ## Pending Issues
        - bck_llm_layers.py: AI image generation failed, prompt needs rework
        - Review partial: 3/5 perspectives completed

        ## Context for Next Session
        Focus was on the LLM section (blocks 6-12). First 5 blocks are
        finalized. Glossary is an out-of-plan addition that should be
        integrated into the next plan version.
    """, language="markdown", line_numbers=False)
    st_space("v", 1)

    # ── Best practices ────────────────────────────────────────────
    show_explanation("""\
    ### Best Practices

    **1. Pause before every session end** — Even short sessions benefit
    from a checkpoint. The command takes seconds and the context it
    preserves can save minutes of re-orientation.

    **2. Commit the checkpoint** — `docs/ce-checkpoint.md` should be
    committed to git. This ensures it survives workspace changes and
    gives `/stx-ce:continue` a reliable file to read.

    **3. Use `--message` for quick annotations** — If you know what to
    say, pass it directly: `/stx-ce:pause --message "stopped mid-review,
    visual perspective done, 2 remaining"`.

    **4. Review the draft** — The checkpoint captures decisions from the
    conversation, but may miss nuances. Review the proposed decisions
    and add anything important before confirming.

    **5. One checkpoint per project** — The checkpoint file is per-project
    (`docs/ce-checkpoint.md`). Running pause again overwrites the previous
    checkpoint.
    """)

    st_space("v", 1)
