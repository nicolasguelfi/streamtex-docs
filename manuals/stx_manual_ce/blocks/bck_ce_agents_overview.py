"""CE Manual — Part 3: Overview of All 17 Agents."""

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
             ("The Capitalization Engine orchestrates ",
              (s.bold, "17 specialized agents"),
              " across the five CE phases. Each agent has a focused responsibility "
              "and communicates through structured artifacts — templates, checklists, "
              "and reports — that flow from one phase to the next."))
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
    | 8 | PLAN | **structure-planner** | Designs document skeleton: parts, blocks, navigation flow |
    | 9 | PLAN | **task-sequencer** | Orders production tasks, estimates effort, flags dependencies |
    | 10 | PRODUCE | **block-writer** | Generates StreamTeX block code from plan specifications |
    | 11 | PRODUCE | **style-applicator** | Applies custom styles, themes, and visual consistency |
    | 12 | PRODUCE | **content-migrator** | Converts legacy HTML/Marp/PDF content into StreamTeX blocks |
    | 13 | REVIEW | **audience-advocate** | Reviews from the reader's perspective: clarity, accessibility |
    | 14 | REVIEW | **pedagogy-analyst** | Checks learning flow, progression, and explanation quality |
    | 15 | REVIEW | **visual-reviewer** | Evaluates layout, spacing, visual hierarchy, and responsiveness |
    | 16 | REVIEW | **style-consistency-checker** | Verifies adherence to project style guide and conventions |
    | 17 | REVIEW | **content-editor** | Proofreads text, checks accuracy, suggests rewording |
    """)

    show_explanation("""
    ### How Agents Collaborate

    Agents do not communicate directly. Instead, they follow a **relay pattern**:

    - **COLLECT** agents produce a **source inventory** and **complexity report**.
    - **ASSESS** agents read those reports and produce an **assessment brief**.
    - **PLAN** agents consume the brief and emit a **structured plan**.
    - **PRODUCE** agents execute the plan, generating blocks and content.
    - **REVIEW** agents evaluate the output against the assessment criteria.

    Two **COMPOUND** agents — **feedback-detector** and **dev-governance** — operate
    outside this linear flow. They harvest insights from any phase and channel them
    into the three capitalization axes: solutions, profiles, and ecosystem feedback.
    """)

    show_details("""
    ### Agent Activation by Pathway

    | Agent | Pathway A (Import) | Pathway B (Improve) | Pathway C (Create) |
    |-------|--------------------|---------------------|--------------------|
    | source-scanner | Yes | Yes | -- |
    | import-assessor | Yes | -- | -- |
    | audience-analyst | Yes | Yes | Yes |
    | content-strategist | Yes | Yes | Yes |
    | gap-analyst | Yes | Yes | -- |
    | format-explorer | Yes | Yes | Yes |
    | angle-generator | -- | -- | Yes |
    | structure-planner | Yes | Yes | Yes |
    | task-sequencer | Yes | Yes | Yes |
    | block-writer | Yes | Yes | Yes |
    | style-applicator | Yes | Yes | Yes |
    | content-migrator | Yes | -- | -- |
    | Review agents (5) | Yes | Yes | Yes |
    | Compound agents (2) | Yes | Yes | Yes |
    """)
