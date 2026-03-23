"""CE Quick Start — Common usage patterns and first cycle tutorial."""

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details, show_code
except ImportError:
    from streamtex import show_explanation, show_details, show_code


class BlockStyles:
    """CE Quick Start styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Render the CE quick start page."""
    st_space("v", 1)
    st_write(bs.heading, "Quick Start",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── 3 common patterns ─────────────────────────────────────────
    st_write(bs.sub, "3 common usage patterns", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "CE adapts to your situation. Here are the three most "
             "common ways to start a cycle:")
    st_space("v", 1)

    # Pattern 1: Full cycle
    st_write(s.large + s.bold, "1. Full cycle — all 7 phases")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:go "Create a training manual about Docker deployment"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)
    show_explanation("""\
        Runs all phases: COLLECT, ASSESS, PLAN, PRODUCE, REVIEW, FIX,
        COMPOUND. Three validation gates pause for your approval
        (after ASSESS, after PLAN, after REVIEW). Best for new projects
        where you want full control.
    """)
    st_space("v", 1)

    # Pattern 2: Quick mode
    st_write(s.large + s.bold, "2. Quick mode — skip collect and assess")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:go --quick "Add a security chapter to the deploy manual"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)
    show_explanation("""\
        Skips COLLECT and ASSESS, starts directly at PLAN.
        Use this when you already know what you want and the project
        context is clear. Only one gate (after PLAN).
    """)
    st_space("v", 1)

    # Pattern 3: Import
    st_write(s.large + s.bold, "3. Import pathway — bring in external files")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:go --import ~/sources/ "Convert the HTML course to StreamTeX"
    """, language="bash", line_numbers=False)
    st_space("v", 0.5)
    show_explanation("""\
        Forces Pathway A. COLLECT scans the source directory, classifies
        every file, and evaluates importability. PRODUCE converts each
        file using stx-import commands. Ideal when you have a folder
        of existing material.
    """)
    st_space("v", 2)

    # ── Validation gates ──────────────────────────────────────────
    st_write(bs.sub, "What happens at each gate", toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type=lt.ordered, li_style=s.large, align="center") as l:
        with l.item():
            st_write((s.bold, "Gate 1 — After "), (s.project.titles.phase_kw, "ASSESS"),
                     (s.bold, ": "),
                     "CE shows the detected pathway, objectives, and "
                     "constraints. You approve or adjust before planning.")
        with l.item():
            st_write((s.bold, "Gate 2 — After "), (s.project.titles.phase_kw, "PLAN"),
                     (s.bold, ": "),
                     "CE shows the block list, structure, and style choices. "
                     "You approve or revise before production starts.")
        with l.item():
            st_write((s.bold, "Gate 3 — After "), (s.project.titles.phase_kw, "REVIEW"),
                     (s.bold, ": "),
                     "CE shows review findings from 5 perspectives. "
                     "You decide which issues to fix and which to accept.")
    st_space("v", 2)

    # ── 5-minute tutorial ─────────────────────────────────────────
    st_write(bs.heading, "Your first CE cycle in 5 minutes",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large + s.bold, "Step 1: Start the cycle")
    st_space("v", 0.5)
    show_code("""\
        /stx-ce:go "Create a one-page project summary about StreamTeX"
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    st_write(s.large + s.bold, "Step 2: Approve the assessment")
    st_space("v", 0.5)
    st_write(s.large,
             "CE detects Pathway C (create), proposes objectives, "
             "and shows Gate 1. Type ", (s.bold, "approve"),
             " to continue.")
    st_space("v", 1)

    st_write(s.large + s.bold, "Step 3: Approve the plan")
    st_space("v", 0.5)
    st_write(s.large,
             "CE proposes a block list (e.g., bck_summary_intro, "
             "bck_summary_features). Gate 2 appears. Type ",
             (s.bold, "approve"), " to start production.")
    st_space("v", 1)

    st_write(s.large + s.bold, "Step 4: Review and finish")
    st_space("v", 0.5)
    st_write(s.large,
             "CE produces all blocks, runs the review, and shows "
             "findings at Gate 3. Fix any issues or accept the result. "
             "The COMPOUND phase logs what was done.")
    st_space("v", 1)

    show_details("""\
        After the cycle, check `docs/` for the generated artifacts:
        - `docs/assessment.md` — assessment report
        - `docs/plan.md` — production plan
        - `docs/review.md` — review findings
        - `docs/solutions/` — reusable solution packages

        These files are reusable references for future cycles.
        Run `stx run` to see your new project live.
    """)
    st_space("v", 1)
