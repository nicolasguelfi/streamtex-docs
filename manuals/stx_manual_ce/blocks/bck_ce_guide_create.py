"""CE Manual — Part 4: Guide — Create a New Document (Pathway C)."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Create Guide styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Guide: Create a new document — Pathway C walkthrough."""

    st_space("v", 1)
    st_write(bs.heading, "Guide: Create a New Document (Pathway C)",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             (s.project.titles.pathway_kw, "Pathway C"),
             (" starts from a blank canvas. You have an idea for a document "
              "but no existing material to import or improve. This pathway replaces "
              "the gap-analyst with the "),
             (s.bold, "angle-generator"),
             ", which proposes creative structural approaches before any content is written.")
    st_space("v", 1)

    show_explanation("""
    ### Step 1: COLLECT — Gather Context

    ```
    /stx-ce:collect --brief "Description of your document goals"
    ```

    In Pathway C, COLLECT works differently. There are no files to scan,
    so the **source-scanner** instead collects contextual information:

    - Existing projects in the workspace (for reference and reuse)
    - Available solution templates from prior COMPOUND phases
    - Producer profile preferences and conventions
    - Any reference materials you point it to (optional)

    This lightweight collection gives the ASSESS phase enough context
    to make informed recommendations.
    """)

    show_explanation("""
    ### Step 2: ASSESS — Define Objectives and Explore Angles

    ```
    /stx-ce:assess
    ```

    This is the most creative step in Pathway C. Four agents collaborate:

    - **audience-analyst** profiles your target readers based on the brief.
    - **content-strategist** maps themes and learning objectives.
    - **format-explorer** recommends StreamTeX features suited to the content.
    - **angle-generator** (unique to Pathway C) proposes 3-5 structural
      approaches.

    The angle-generator is the key differentiator. It might propose:

    1. **Tutorial angle** — step-by-step, building complexity gradually
    2. **Reference angle** — organized by topic, each section self-contained
    3. **Narrative angle** — story-driven, following a real-world scenario
    4. **Problem-solution angle** — each section presents a problem then solves it
    5. **Comparative angle** — contrasts approaches, helping readers choose

    Each angle comes with a skeleton (parts and blocks), estimated effort,
    and trade-off analysis.
    """)

    show_details("""
    ### Angle Selection Criteria

    | Criterion | Tutorial | Reference | Narrative | Problem-Solution |
    |-----------|----------|-----------|-----------|------------------|
    | Audience: beginners | Excellent | Poor | Good | Good |
    | Audience: experts | Poor | Excellent | Fair | Good |
    | Maintainability | Good | Excellent | Poor | Good |
    | Reuse potential | Fair | Excellent | Poor | Good |
    | Engagement | Good | Poor | Excellent | Good |
    | Production effort | Medium | Low | High | Medium |

    You pick one angle or combine elements from multiple angles.
    The choice is recorded in the assessment brief and guides the
    entire PLAN and PRODUCE phases.
    """)

    show_explanation("""
    ### Step 3: PLAN — Build the Skeleton

    ```
    /stx-ce:plan
    ```

    The **structure-planner** translates your chosen angle into a concrete
    document structure:
    - Part titles and descriptions
    - Block names, responsibilities, and estimated line counts
    - Navigation flow and cross-references
    - Required custom styles and helpers

    The **task-sequencer** orders production to maximize momentum:
    - Start with the "anchor" block (the one that defines the tone)
    - Then foundational blocks that others depend on
    - Then fill in remaining blocks in reading order
    - Custom styles and helpers scheduled before the blocks that need them
    """)

    show_explanation("""
    ### Step 4: PRODUCE — Write from Scratch

    ```
    /stx-ce:produce
    ```

    The **block-writer** is the primary agent here. For each planned block:
    - Creates the file with proper StreamTeX structure
    - Writes content following the angle's guidelines
    - Uses show_explanation() for conceptual content
    - Uses show_details() for reference and technical material
    - Integrates examples, code snippets, and visual elements

    The **style-applicator** ensures visual consistency from the start,
    applying the `custom/styles.py` definitions and recommending new
    styles where the content demands them.

    **Tip**: Pathway C production benefits greatly from a strong producer
    profile. If you have documented your preferred writing conventions
    in prior COMPOUND phases, the block-writer follows them automatically.
    """)

    show_details("""
    ### Steps 5-6: REVIEW, FIX, and COMPOUND

    **Review** in Pathway C emphasizes:
    ```
    /stx-ce:review
    ```
    - **Coherence**: does the document feel unified? (No prior material to blend with)
    - **Completeness**: are all planned blocks present and substantive?
    - **Angle fidelity**: does the content follow the chosen structural approach?

    **Fix** and **Compound** follow the standard pattern:
    ```
    /stx-ce:fix
    /stx-ce:compound
    ```

    Pathway C COMPOUND outputs are especially rich because creating from
    scratch generates the most transferable insights:
    - The chosen angle becomes a reusable solution template
    - Block patterns that worked well are documented for future projects
    - The producer profile gains new structural preferences
    """)
