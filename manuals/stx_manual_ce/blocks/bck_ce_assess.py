"""CE Manual — Part 2: ASSESS Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """ASSESS phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """ASSESS phase: auto-detect pathway, evaluate, dialogue."""

    st_space("v", 1)
    st_write(bs.heading, "ASSESS — Evaluate Material and Detect Pathway",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "ASSESS"),
             " phase analyzes the collect report and determines the optimal "
             "production pathway. It evaluates the quality of source material, identifies "
             "gaps, and initiates a structured dialogue with the user to clarify "
             "requirements (R1-R18).")
    st_space("v", 1)

    show_explanation("Pathway Auto-Detection", """
    ASSESS automatically selects one of three pathways based on the collect report:

    | Pathway | Trigger Condition | Behavior |
    |---------|-------------------|----------|
    | **A — Import** | >60% items are importable | Prioritize import, minimal creation |
    | **B — Improve** | Mix of importable and new content | Interleave import and creation |
    | **C — Create** | <20% importable or no sources | Focus on from-scratch production |

    The pathway determines how the PLAN and PRODUCE phases will operate.
    Pathway detection is automatic but can be overridden with `--pathway A|B|C`.
    """)

    st_space("v", 1)

    show_explanation("Material Evaluation", """
    For each collected item, ASSESS produces a quality evaluation:

    **Structural Evaluation**
    - Does the content map to StreamTeX block types?
    - Are headings, lists, and code blocks well-formed?
    - Is the content self-contained or does it depend on external context?

    **Pedagogical Evaluation**
    - Is the content appropriate for the target audience?
    - Are learning objectives clearly stated or inferable?
    - Does the content follow a logical progression?

    **Technical Evaluation**
    - Are code examples correct and runnable?
    - Are diagrams and images available in usable formats?
    - Are references and links still valid?
    """)

    st_space("v", 1)

    show_explanation("User Dialogue — Requirements R1-R18", """
    ASSESS initiates a structured dialogue to capture user requirements:

    | Req | Question Domain | Example |
    |-----|-----------------|---------|
    | R1 | Target audience | "Who is the primary audience?" |
    | R2 | Prerequisite knowledge | "What should readers already know?" |
    | R3 | Learning objectives | "What should readers be able to do after?" |
    | R4-R6 | Scope and boundaries | "What topics are in/out of scope?" |
    | R7-R9 | Style preferences | "Formal or conversational tone?" |
    | R10-R12 | Structure constraints | "Max depth? Number of parts?" |
    | R13-R15 | Content priorities | "Which topics are most important?" |
    | R16-R18 | Delivery constraints | "Timeline? Incremental delivery?" |

    In **auto mode**, ASSESS infers answers from the source material and
    confirms with the user. In **interactive mode**, each requirement is
    explicitly discussed.
    """)

    st_space("v", 1)

    show_details("Pathway-Specific Behaviors", """
    **Pathway A (Import)**
    - ASSESS focuses on mapping source items to target blocks
    - Minimal requirements dialogue (R1-R3 only, rest inferred)
    - Produces an import manifest with block-level assignments

    **Pathway B (Improve)**
    - ASSESS identifies gaps between imported and needed content
    - Medium dialogue (R1-R9 confirmed, R10-R18 inferred)
    - Produces a gap analysis alongside the import manifest

    **Pathway C (Create)**
    - ASSESS conducts full requirements elicitation (R1-R18)
    - Builds a content specification from scratch
    - Produces a creation brief with detailed block descriptions
    """)

    st_space("v", 1)

    show_details("Command Reference", """
    ```bash
    # Run ASSESS on existing collect report
    /stx-ce:assess

    # Force a specific pathway
    /stx-ce:assess --pathway B

    # Interactive mode (ask all R1-R18)
    /stx-ce:assess --interactive

    # Auto mode (infer and confirm)
    /stx-ce:assess --auto
    ```

    The assess report is saved to `docs/assessment.md`.
    """)

    st_space("v", 1)
