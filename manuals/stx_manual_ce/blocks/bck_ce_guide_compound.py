"""CE Manual — Part 4: Guide — Capitalize Effectively."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the compound guide block."""

    title = s.section_title
    table = s.reference_table


def build():
    """Guide: Capitalize effectively — the three axes in practice."""

    st_write("""
    ## Guide: Capitalize Effectively

    The COMPOUND phase is what transforms the CE from a simple production
    pipeline into a **learning system**. Every cycle produces not just
    documents, but knowledge that makes future cycles faster and better.
    This guide explains how to get the most out of each capitalization axis.
    """)

    show_explanation("""
    ### Axis 1: Writing Good Solutions

    A **solution** is a reusable pattern extracted from a successful CE cycle.
    It captures what worked so that future projects can reuse it without
    rediscovering it from scratch.

    **What makes a good solution:**
    - **Specific enough to be useful** — not just "use good headings" but
      "for API reference documents, use a three-level heading structure:
      module > class > method, with each method getting its own block."
    - **General enough to transfer** — applicable beyond the single project
      where it was discovered.
    - **Self-contained** — includes all context needed to apply it: the
      pattern, when to use it, when NOT to use it, and an example.

    **How to write solutions:**
    1. During REVIEW, note techniques that the reviewers praise.
    2. During COMPOUND, the feedback-detector flags these automatically.
    3. Package each pattern using the `tpl_solution_package` template.
    4. Store in `docs/solutions/` with a descriptive filename.
    5. Reference solutions in future PLAN phases.
    """)

    show_details("""
    ### Solution Package Format

    ```
    Solution: <descriptive-title>
    ==============================
    Origin: <project-name>, cycle <date>
    Pathway: A | B | C

    Context:
      When building <type of document>, you need <situation>.

    Pattern:
      <concrete description of what to do>

    Example:
      <code or structure showing the pattern in action>

    When NOT to use:
      <situations where this pattern is inappropriate>

    Related solutions:
      <links to complementary or alternative solutions>
    ```

    Solutions accumulate in a searchable library. The PLAN phase agents
    consult this library when designing new document structures.
    """)

    show_explanation("""
    ### Axis 2: Managing Producer Profiles

    The **producer profile** is a living document that captures your
    personal conventions, preferences, and skills as a content producer.
    It evolves with every CE cycle.

    **Profile sections:**
    - **Writing style** — preferred tone, sentence length, use of examples
    - **Structural preferences** — favorite block patterns, part sizes
    - **Tool proficiency** — which StreamTeX features you are comfortable with
    - **Quality standards** — your personal bar for "good enough"
    - **Lessons learned** — mistakes to avoid, hard-won insights

    **Cross-project value**: when you start a new project, CE agents read
    your profile and adapt their suggestions accordingly. An experienced
    producer with a detailed profile gets better recommendations than a
    newcomer with a blank profile.

    **Updating the profile:**
    - The COMPOUND phase proposes profile updates automatically.
    - Review the proposals — accept, modify, or reject each one.
    - The profile is stored in `docs/profile.md` and versioned with git.
    """)

    show_explanation("""
    ### Axis 3: Submitting Ecosystem Feedback

    The third capitalization axis feeds insights back to the StreamTeX
    ecosystem itself. This is how individual experience improves the
    tools for everyone.

    **Types of ecosystem feedback:**
    - **Bug reports** — when a StreamTeX feature does not work as documented
    - **Feature requests** — when you need something that does not exist yet
    - **Documentation gaps** — when official docs miss important information
    - **Workflow improvements** — when the CE process itself could be better

    **The dev-governance agent** formats feedback following the
    `tpl_ecosystem_feedback` template, which includes:
    - Clear problem statement with reproduction steps
    - Impact assessment (how many users likely affected)
    - Proposed solution (when applicable)
    - Priority recommendation
    """)

    show_details("""
    ### Dev Governance in Practice

    Dev governance ensures that capitalization outputs are **actionable**,
    not just documented. The dev-governance agent applies these rules:

    | Output | Requires | Action |
    |--------|----------|--------|
    | Solution package | At least one concrete example | Saved to `docs/solutions/` |
    | Profile update | Diff against current profile | Merged into `docs/profile.md` |
    | Ecosystem feedback | Reproduction steps or rationale | Formatted for GitHub issue |

    **Governance quality gate**: every COMPOUND output must pass a
    self-check before being finalized:
    1. Is this actionable? (Can someone use it without asking questions?)
    2. Is this novel? (Is it not already captured elsewhere?)
    3. Is this accurate? (Does it reflect what actually happened?)

    Items that fail the quality gate are logged as "pending" and
    revisited in the next cycle. This prevents noise accumulation
    while preserving potentially valuable observations.

    **Git integration**: all COMPOUND outputs are committed with a
    conventional commit message: `compound(<axis>): <description>`.
    This makes it easy to trace the capitalization history of a project.
    """)
