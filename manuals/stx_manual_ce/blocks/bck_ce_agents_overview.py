"""CE Manual — Part 3: Overview of All 21 Agents and Command-Driven PRODUCE."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Agents Overview styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Overview of all 21 agents: table listing by phase, role, and collaboration."""

    st_space("v", 1)
    st_write(bs.heading, "Agents Overview",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "Compound Document Engineering orchestrates ",
              (s.bold, "21 specialized agents"),
              " across the nine CE phases (with PROTOTYPE auto-triggered between PLAN and PRODUCE). "
              "Each agent has a focused responsibility "
              "and communicates through structured artifacts — templates, checklists, "
              "and reports — that flow from one phase to the next.")
    st_space("v", 1)

    show_explanation("""
    ### Agent Design Principles

    Every CE agent follows three core principles:

    1. **Single Responsibility** — each agent handles exactly one concern
       (e.g., scanning sources, evaluating pedagogy, detecting feedback).
    2. **Template-Driven Output** — agents produce structured documents using
       the 19 CE templates, ensuring consistency across projects.
    3. **Phase Boundaries** — agents only activate during their designated phase,
       reading inputs from prior phases and writing outputs for subsequent ones.

    This modular design means you can understand each agent independently, yet
    they combine into a coherent pipeline when the full cycle runs.
    """)

    st_space("v", 1)

    show_details("""
    ### Complete Agent Registry

    | # | Phase | Agent | Role |
    |---|-------|-------|------|
    | 1 | COLLECT | **source-scanner** | Detects files, extracts metadata, builds source inventory |
    | 2 | COLLECT | **import-assessor** | Evaluates import complexity, recommends conversion method |
    | 3 | ASSESS | **audience-analyst** | Profiles target audience, defines prerequisite knowledge |
    | 4 | ASSESS | **content-strategist** | Maps content scope, identifies themes and learning objectives |
    | 5 | ASSESS | **gap-analyst** | Compares current vs. desired state, lists gaps (pathways A/B) |
    | 6 | ASSESS | **format-explorer** | Surveys output formats, recommends block types and layouts |
    | 7 | ASSESS | **angle-generator** | Proposes creative angles and structural options (pathway C) |
    | 8 | PLAN | **structure-architect** | Designs document skeleton: parts, blocks, navigation flow |
    | 9 | PLAN | **domain-researcher** | Gathers domain knowledge, best practices, technical references |
    | 10 | PLAN | **learnings-researcher** | Mines past project experience, surfaces reusable patterns |
    | 11 | PLAN (continue/fix) | **plan-reconciler** | Detects divergences between `book.py` and the master plan; proposes block-by-block reconciliation |
    | 12 | PROTOTYPE | **prototype-designer** | Selects pilot block(s), proposes pattern strategy (reuse / adapt / create) |
    | 13 | PRODUCE | *(command-driven)* | Delegates to `/stx-block:*`, `/stx-import:*`, `/stx-export:*`, `/stx-deploy:*` |
    | 14 | REVIEW | **audience-advocate** | Reviews from the reader's perspective: clarity, accessibility |
    | 15 | REVIEW | **pedagogy-analyst** | Checks learning flow, progression, and explanation quality |
    | 16 | REVIEW | **visual-reviewer** | Evaluates layout, spacing, visual hierarchy, and responsiveness |
    | 17 | REVIEW | **style-consistency-checker** | Verifies adherence to project style guide and conventions |
    | 18 | REVIEW | **content-editor** | Proofreads text, checks accuracy, suggests rewording |
    | 19 | REVIEW / CONTINUE | **objective-monitor** | Judges whether the iteration's objectives are met; produces a textual judgment, not metrics |
    | 20 | COMPOUND | **feedback-detector** | Detects ecosystem issues from review findings |
    | 21 | COMPOUND | **dev-governance** | Enforces development discipline across the cycle |
    | 22 | TASK | **ad-hoc-reviewer** | Executes custom-criteria reviews on scoped blocks |

    **Extended modes** (activated by `/stx-ce:task`):
    - **gap-analyst**: bidirectional comparison (source→blocks + blocks→source)
    - **learnings-researcher**: targeted search (single topic/pattern dedup)
    """)

    st_space("v", 1)

    show_explanation("""
    ### How Agents Collaborate

    Agents do not communicate directly. Instead, they follow a **relay pattern**:

    - **COLLECT** agents produce a **source inventory** and **complexity report**.
    - **ASSESS** agents read those reports and produce an **assessment brief**; in the first iteration they also initialise the **master plan**.
    - **PLAN** agents consume the brief and emit a **structured plan**; on subsequent CE sessions, **plan-reconciler** checks alignment with `book.py` and surfaces divergences for user decision.
    - **PROTOTYPE** is led by **prototype-designer** — it selects pilot block(s) and either reuses or extracts patterns into the local catalog.
    - **PRODUCE** is command-driven — it executes the plan via `/stx-block:*` and `/stx-import:*` commands, applying the patterns mapped in the master plan.
    - **REVIEW** agents evaluate the output against the assessment criteria; **objective-monitor** consults the master plan's objectives and produces a textual judgment of whether they were met by the iteration.

    Two **COMPOUND** agents — **feedback-detector** and **dev-governance** — operate
    outside this linear flow. They harvest insights from any phase and channel them
    into the four capitalization axes: document production (including pattern catalog enrichment), ecosystem feedback, development governance, and master plan maintenance.
    """)

    st_space("v", 1)

    show_details("""
    ### Agent Activation by Pathway

    | Agent | Phase | Pathway A (Import) | Pathway B (Improve) | Pathway C (Create) |
    |-------|-------|--------------------|---------------------|--------------------|
    | source-scanner | COLLECT | Yes | Yes | -- |
    | import-assessor | COLLECT | Yes | -- | -- |
    | audience-analyst | ASSESS | Yes | Yes | Yes |
    | content-strategist | ASSESS | Yes | Yes | Yes |
    | gap-analyst | ASSESS | Yes | Yes | -- |
    | format-explorer | ASSESS | Yes | Yes | Yes |
    | angle-generator | ASSESS | -- | -- | Yes |
    | structure-architect | PLAN | Yes | Yes | Yes |
    | domain-researcher | PLAN | Yes | Yes | Yes |
    | learnings-researcher | PLAN | Yes | Yes | Yes |
    | plan-reconciler | PLAN (continue/fix) | Yes | Yes | Yes |
    | prototype-designer | PROTOTYPE | Yes | Yes | Yes |
    | *(commands)* | PRODUCE | Yes | Yes | Yes |
    | Review agents (5) | REVIEW | Yes | Yes | Yes |
    | objective-monitor | REVIEW / CONTINUE | Yes | Yes | Yes |
    | Compound agents (2) | COMPOUND | Yes | Yes | Yes |
    """)

    st_space("v", 1)
