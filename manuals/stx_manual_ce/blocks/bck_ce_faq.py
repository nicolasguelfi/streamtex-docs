"""CE Manual — Part 5: Frequently Asked Questions."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Frequently Asked Questions styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """FAQ: common questions about Compound Document Engineering."""

    st_space("v", 1)
    st_write(bs.heading, "Frequently Asked Questions",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "Answers to the most common questions about using the "
             "Compound Document Engineering methodology in practice.")
    st_space("v", 1)

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

    st_space("v", 1)

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

    st_space("v", 1)

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

    st_space("v", 1)

    show_explanation("""
    ### How does CE interact with stx-block?

    CE and stx-block are **complementary tools** that operate at
    different levels:

    - **stx-block** focuses on the *technical* level: creating blocks,
      applying styles, auditing code quality, and fixing implementation
      issues. It works with individual blocks and StreamTeX code.
    - **CE** focuses on the *content* level: analyzing what to write,
      planning document structure, reviewing content quality, and
      capitalizing learnings. It works with the document as a whole.

    **Typical combined workflow:**
    1. Use CE to plan and assess (COLLECT, ASSESS, PLAN phases).
    2. Use `/stx-block:init` or `/stx-block:update` to implement
       the plan at the block level (CE's PRODUCE phase).
    3. Use CE to review and capitalize (REVIEW, COMPOUND phases).
    4. Use `/stx-block:audit` and `/stx-block:fix` for technical
       quality issues found during CE review.

    The tools do not interfere with each other. CE writes to `docs/`,
    stx-block works in `blocks/` and `custom/`.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Can I use CE for presentations?

    **Yes.** CE works with any StreamTeX project type, including
    presentations created with the stx-block presentation profile.

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

    st_space("v", 1)

    show_explanation("""
    ### How do I add bibliography and citations to my CE project?

    Bibliography support is built into the CE workflow across multiple phases:

    1. **ASSESS**: Requirements R19-R21 cover citation presence, BibTeX
       validity, and reference completeness. The assessment will flag
       missing citations as gaps.
    2. **PLAN**: Include a `BibConfig` section in your plan with the
       citation style (APA, IEEE, etc.) and the path to your `.bib` file.
       The structure plan template has dedicated fields for bibliography
       setup.
    3. **PRODUCE**: Use `cite("key")` for inline citations and
       `st_bibliography()` to render the reference list. The PRODUCE
       agents will insert citations according to the plan.
    4. **REVIEW**: The editorial reviewer checks citation consistency
       and completeness against the bibliography file.

    **Quick start**: add a `references.bib` file to your project root,
    then mention bibliography in your `/stx-ce:plan` description.
    """)

    st_space("v", 1)

    show_explanation("""
    ### Can CE generate AI images?

    **Yes.** CE supports AI image generation through requirements R22-R24
    and the `AIImageConfig` configuration object.

    **Setup:**
    1. Install AI dependencies: `uv add streamtex[ai]` (or a specific
       provider: `streamtex[ai-openai]`, `streamtex[ai-google]`,
       `streamtex[ai-fal]`).
    2. Set the appropriate API key environment variable (`STX_OPENAI_API_KEY`,
       `STX_GOOGLE_AI_KEY`, or `STX_FAL_KEY`).
    3. In your PLAN, include `AIImageConfig` with your preferred provider,
       default image size, and quality settings.

    **During PRODUCE:** Use `st_ai_image(prompt)` in your blocks. Images
    are cached by a deterministic hash of the prompt, provider, size,
    quality, and seed, so regeneration only happens when parameters change.

    **During REVIEW:** R22-R24 check that the AI provider is configured,
    prompts are descriptive, and caching is used effectively.
    """)

    st_space("v", 1)

    show_explanation("""
    ### How do I check my CE cycle progress?

    Use the `/stx-ce:status` command. It displays a dashboard showing:

    - Which phases are completed, in progress, or pending
    - Block-by-block production progress (during PRODUCE)
    - Review findings summary by severity level
    - Producer profile state and last update date

    For a detailed breakdown, use `/stx-ce:status --verbose`.

    **Example:**
    ```
    /stx-ce:status
    ```
    ```
    CE Cycle Status
    ===============
    Pathway: B (Improve)
    Current phase: REVIEW
    Inventory: 8 sources | Assessment: 3 gaps | Plan: 6 blocks
    Production: 6/6 blocks done
    Review: 1 CRITICAL, 3 MAJOR, 5 MINOR
    Profile: exists (2026-03-20)
    ```

    Run `/stx-ce:status` at any time — it reads the `docs/` artifacts
    and reports the current state without modifying anything.
    """)

    st_space("v", 1)

    show_explanation("""
    ### How do I do a quick task without the full cycle?

    Use `/stx-ce:task` with a free-text description:
    ```
    /stx-ce:task "Compare source lines 524-600 with produced blocks"
    /stx-ce:task "Review danger blocks on citation accuracy"
    /stx-ce:task "Add a block on AI ethics from source lines 402-410"
    ```

    The system auto-detects what you need (compare, review, produce, etc.)
    and executes it while keeping lifecycle artifacts in sync. No need to
    run the full COLLECT → COMPOUND pipeline.
    """)

    st_space("v", 1)

    show_explanation("""
    ### I'm coming back after a 2-week break. Where do I start?

    Run `/stx-ce:continue`. It will:
    1. **Brief you** on the project state (last activity, progress, plan version)
    2. **Detect drift** (source changes, manual edits, stale reviews)
    3. **Propose** prioritized next steps with executable commands
    4. Let you **choose** a proposal or describe your own task

    This is the recommended first command after any session break.
    """)

    st_space("v", 1)

    show_explanation("""
    ### How does plan versioning work?

    When a task modifies the plan, the current plan is kept as-is and a
    **new version** is created with all modifications integrated inline.
    The new version includes a Change Log header documenting what changed.

    **Naming**: `YYYY-MM-DD-NNN-<name>-plan.md` — latest by date+sequence is current.
    **No amendments**: Each version is a complete, self-contained document.
    **Auto-detection**: `/stx-ce:produce` always uses the latest plan version.
    """)

    st_space("v", 1)

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
    | Can I use CE without stx-block? | Yes. They are independent tools. |
    """)

    st_space("v", 1)
