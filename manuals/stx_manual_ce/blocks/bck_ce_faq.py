"""CE Manual — Part 5: Frequently Asked Questions."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the FAQ block."""

    title = s.section_title
    table = s.reference_table


def build():
    """FAQ: common questions about the Capitalization Engine."""

    st_write("""
    ## Frequently Asked Questions

    Answers to the most common questions about using the Capitalization
    Engine in practice.
    """)

    show_explanation("""
    ### Can I skip phases?

    **Short answer**: Yes, but with trade-offs.

    You can jump directly to any phase using its command (e.g.,
    `/stx-ce:produce` without running COLLECT or ASSESS first). The agents
    will work with whatever information is available, but their output
    quality degrades without prior phase artifacts.

    **Recommended shortcuts:**
    - Skip COLLECT for small, well-understood projects where you already
      know what you have.
    - Skip ASSESS when making minor edits to an existing project (quick
      Pathway B cycle).
    - Never skip REVIEW — it catches issues that are invisible during
      production.

    **Not recommended:**
    - Skipping PLAN for large projects — leads to inconsistent structure.
    - Skipping COMPOUND habitually — you lose the long-term learning benefit.
    """)

    show_explanation("""
    ### How do I resume an interrupted cycle?

    Use `/stx-ce:status` to see where you left off. CE tracks progress
    in the `docs/` artifacts — each completed phase leaves a dated file.

    To resume:
    1. Run `/stx-ce:status` to check the current state.
    2. Run the command for the next incomplete phase.
    3. Agents will read existing artifacts and continue from where you stopped.

    For PRODUCE phase interruptions, use `/stx-ce:produce --block <name>`
    to produce individual blocks without restarting the entire phase.

    **There is no time limit** on cycles. You can pause for days or weeks
    and resume without losing context — everything is in the `docs/` files.
    """)

    show_explanation("""
    ### What if I don't have any sources?

    Use **Pathway C** (Create from scratch). Run:
    ```
    /stx-ce:collect --brief "Description of what you want to create"
    ```

    The COLLECT phase will gather context from your workspace (existing
    projects, solution library, producer profile) instead of scanning
    source files. The ASSESS phase then uses the **angle-generator**
    to propose structural approaches.

    Pathway C works well even with a completely empty workspace. The
    agents use their built-in knowledge of document patterns and
    StreamTeX capabilities to guide you.
    """)

    show_explanation("""
    ### How does CE interact with stx-designer?

    CE and stx-designer are **complementary tools** that operate at
    different levels:

    - **stx-designer** focuses on the *technical* level: creating blocks,
      applying styles, auditing code quality, and fixing implementation
      issues. It works with individual blocks and StreamTeX code.
    - **CE** focuses on the *content* level: analyzing what to write,
      planning document structure, reviewing content quality, and
      capitalizing learnings. It works with the document as a whole.

    **Typical combined workflow:**
    1. Use CE to plan and assess (COLLECT, ASSESS, PLAN phases).
    2. Use `/stx-designer:init` or `/stx-designer:update` to implement
       the plan at the block level (CE's PRODUCE phase).
    3. Use CE to review and capitalize (REVIEW, COMPOUND phases).
    4. Use `/stx-designer:audit` and `/stx-designer:fix` for technical
       quality issues found during CE review.

    The tools do not interfere with each other. CE writes to `docs/`,
    stx-designer works in `blocks/` and `custom/`.
    """)

    show_explanation("""
    ### Can I use CE for presentations?

    **Yes.** CE works with any StreamTeX project type, including
    presentations created with the stx-designer presentation profile.

    **Pathway adjustments for presentations:**
    - COLLECT scans slide-based content (Marp files map naturally to
      presentation blocks).
    - ASSESS considers presentation-specific concerns: slide count,
      speaking time, visual density per slide.
    - PLAN structures by presentation sections rather than document parts.
    - REVIEW includes presentation-specific checks: slide readability,
      information per slide limits, visual consistency.

    Use `/stx-ce:collect --brief "presentation about..."` for Pathway C
    or point to existing Marp/HTML slides for Pathway A.
    """)

    show_details("""
    ### Quick Answers

    | Question | Answer |
    |----------|--------|
    | Can I run multiple cycles in parallel? | Not on the same project. One cycle at a time per project. |
    | Where are CE artifacts stored? | In the `docs/` directory of your project. |
    | Can I edit CE artifacts manually? | Yes. They are plain Markdown. Agents will read your edits. |
    | Do I need git for CE? | No, but git integration is recommended for tracking changes. |
    | Can I share my producer profile? | Yes. Copy `docs/profile.md` to another project's `docs/`. |
    | How do I reset a cycle? | Delete the `docs/` directory and start fresh. |
    | Does CE work offline? | Yes. All agents run locally through Claude. |
    | Can I customize severity levels? | No. The 4-level scale is fixed for consistency. |
    | How many solutions should I have? | Quality over quantity. 5 good solutions beat 50 vague ones. |
    | Can I use CE without stx-designer? | Yes. They are independent tools. |
    """)
