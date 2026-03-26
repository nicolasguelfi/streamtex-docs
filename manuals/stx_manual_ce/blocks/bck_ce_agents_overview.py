"""CE Manual — Part 3: Overview of All 17 Agents and Command-Driven PRODUCE."""

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
    """Overview of all 17 agents: table listing by phase, role, and collaboration."""

    st_space("v", 1)
    st_write(bs.heading, "Agents Overview",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "Compound Document Engineering orchestrates ",
              (s.bold, "17 specialized agents"),
              " across the five CE phases. Each agent has a focused responsibility "
              "and communicates through structured artifacts — templates, checklists, "
              "and reports — that flow from one phase to the next.")
    st_space("v", 1)

    show_explanation("""
    ### Agent Design Principles

    Every CE agent follows three core principles:

    1. **Single Responsibility** — each agent handles exactly one concern
       (e.g., scanning sources, evaluating pedagogy, detecting feedback).
    2. **Template-Driven Output** — agents produce structured documents using
       the 12 CE templates, ensuring consistency across projects.
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
    | 11 | PRODUCE | *(command-driven)* | Delegates to `/stx-designer:*`, `/stx-import:*`, `/stx-export:*`, `/stx-deploy:*` |
    | 12 | REVIEW | **audience-advocate** | Reviews from the reader's perspective: clarity, accessibility |
    | 13 | REVIEW | **pedagogy-analyst** | Checks learning flow, progression, and explanation quality |
    | 14 | REVIEW | **visual-reviewer** | Evaluates layout, spacing, visual hierarchy, and responsiveness |
    | 15 | REVIEW | **style-consistency-checker** | Verifies adherence to project style guide and conventions |
    | 16 | REVIEW | **content-editor** | Proofreads text, checks accuracy, suggests rewording |
    | 17 | COMPOUND | **feedback-detector** | Detects ecosystem issues from review findings |
    | 18 | COMPOUND | **dev-governance** | Enforces development discipline across the cycle |
    """)

    st_space("v", 1)

    show_explanation("""
    ### How Agents Collaborate

    Agents do not communicate directly. Instead, they follow a **relay pattern**:

    - **COLLECT** agents produce a **source inventory** and **complexity report**.
    - **ASSESS** agents read those reports and produce an **assessment brief**.
    - **PLAN** agents consume the brief and emit a **structured plan**.
    - **PRODUCE** is command-driven — it executes the plan via `/stx-designer:*` and `/stx-import:*` commands.
    - **REVIEW** agents evaluate the output against the assessment criteria.

    Two **COMPOUND** agents — **feedback-detector** and **dev-governance** — operate
    outside this linear flow. They harvest insights from any phase and channel them
    into the three capitalization axes: solutions, profiles, and ecosystem feedback.
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
    | *(commands)* | PRODUCE | Yes | Yes | Yes |
    | Review agents (5) | REVIEW | Yes | Yes | Yes |
    | Compound agents (2) | COMPOUND | Yes | Yes | Yes |
    """)

    st_space("v", 1)
