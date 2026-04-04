"""Tutorial — Creating a complete presentation with Claude AI skills."""

from streamtex import st_write, st_space, st_block, st_list, st_slide_break
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Presentation tutorial block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step_label = s.project.colors.ai_violet + s.bold + s.large
    phase_label = s.project.colors.tech_blue + s.bold + s.large
    highlight = s.project.colors.cyber_cyan + s.bold
    file_label = s.project.colors.success_green + s.bold + s.large
    note_text = s.project.colors.warning_amber + s.large


bs = BlockStyles


def build():
    """Render the presentation creation tutorial."""
    st_space("v", 1)
    st_write(
        bs.heading,
        "Tutorial: Create a Presentation with AI",
        tag=t.div, toc_lvl="1",
    )
    st_space("v", 2)

    show_explanation("""\
        This walkthrough demonstrates the complete workflow for
        creating a StreamTeX presentation using Claude AI skills.
        We build a short 5-slide presentation about StreamTeX
        for a general, non-technical audience — from a single
        natural language prompt to a running application.
    """)
    st_space("v", 2)

    # ══════════════════════════════════════════════════════════════
    # PHASE 1 — stx-block init
    # ══════════════════════════════════════════════════════════════
    st_write(bs.sub, "Phase 1 — Generate the Project", toc_lvl="+1")
    st_space("v", 1)

    # Step 1: Launch the command
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 1 — Launch stx-block init",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Open Claude Code in your workspace and type:",
        )
    st_space("v", 1)

    show_code(
        "/stx-block:init",
        language="bash", line_numbers=False,
    )
    st_space("v", 2)

    # Step 2: Describe the presentation
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 2 — Describe your presentation",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "When Claude asks what you want to build, provide a ",
            (bs.highlight, "specific, structured description"),
            ". Include the audience, the number of slides, the theme, "
            "and the key messages for each slide.",
        )
    st_space("v", 1)

    show_code("""\
        Short presentation "Discover StreamTeX" for a general,
        non-technical audience. 5 slides, dark theme, modern style.

        1) Title — "Discover StreamTeX", subtitle "Create beautiful
           presentations with Python", author + date
        2) The Problem — Why traditional slides are limited:
           static, hard to maintain, no interactivity
        3) The Solution — StreamTeX: Python code becomes interactive
           presentations with themes, grids, navigation
        4) Live Demo — Show what a StreamTeX presentation looks like:
           responsive grid, dark theme, image + bullet points
        5) Getting Started — 3 steps to start: install, create, run.
           End with a motivating question.

        Use the L1/L2/L3 grid layout. Generate image prompts for
        slides that need visuals. Style: telegraphic keywords,
        bold colored accents.""", language="text", line_numbers=False)
    st_space("v", 2)

    # Step 3: Review the generated structure
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 3 — Review the generated project",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Claude generates the complete project structure. "
            "It creates ",
            (s.bold, "5 block files"),
            ", a ",
            (s.bold, "dark theme"),
            " in custom/styles.py, and the orchestration in book.py.",
        )
    st_space("v", 1)

    show_code("""\
        stx-discover-streamtex/
        ├── book.py                        # Orchestration
        ├── blocks/
        │   ├── __init__.py                # Block registry
        │   ├── helpers.py                 # Helper config
        │   ├── bck_title.py               # Title slide
        │   ├── bck_the_problem.py         # Why traditional slides fail
        │   ├── bck_the_solution.py        # StreamTeX to the rescue
        │   ├── bck_live_demo.py           # Visual showcase
        │   └── bck_getting_started.py     # How to start
        ├── custom/
        │   ├── __init__.py
        │   ├── styles.py                  # Dark theme + palette
        │   └── themes.py                  # Theme overrides
        ├── static/images/                 # Image placeholders
        └── .streamlit/
            └── config.toml""", language="text", line_numbers=False)
    st_space("v", 2)

    # ── Example: generated slide code ────────────────────────────
    st_write(
        bs.sub,
        "Example: Generated Slide (bck_the_solution.py)",
        toc_lvl="+1",
    )
    st_space("v", 1)

    show_explanation("""\
        Each generated block follows the L1/L2/L3 grid layout
        defined in the slide-design-rules skill. Notice the
        responsive grid, the bulleted keywords, the image
        placeholder with generation prompt, and the transition
        question at the bottom.
    """)
    st_space("v", 1)

    show_code("""\
        \"\"\"Slide: The Solution — StreamTeX.\"\"\"
        from streamtex import *
        from streamtex.enums import Tags as t, ListTypes as lt
        from custom.styles import Styles as s


        class BlockStyles:
            \"\"\"Slide: The Solution.\"\"\"
            headline = s.project.slide.headline
            body = s.project.slide.body
            keyword = s.project.slide.keyword
            question = s.project.slide.question
        bs = BlockStyles


        def build():
            with st_block(s.center_txt):
                # === L1 — Headline ===
                st_write(
                    bs.headline,
                    "StreamTeX: Python-Powered Presentations",
                    tag=t.div, toc_lvl="2",
                )
                st_space(size=2)

                # === L2 — Image + Key points ===
                with st_grid(
                    cols="repeat(auto-fit, minmax(350px, 1fr))",
                    gap="24px",
                ) as g:
                    with g.cell():
                        # TODO: generate AI image and uncomment
                        # st_image(
                        #     uri="static/images/bck_the_solution.png",
                        #     width="100%",
                        # )
                        # IMAGE PROMPT: "Minimalist flat illustration of
                        #   Python code transforming into a beautiful
                        #   presentation screen, dark bg (#1a1a2e),
                        #   accent cyan (#00d4ff), no text, 16:9"
                        # FILENAME: static/images/bck_the_solution.png
                        st_space("v", 4)
                    with g.cell():
                        with st_list(
                            l_style=bs.body, li_style=bs.body,
                            list_type=lt.unordered,
                        ) as l:
                            with l.item():
                                st_write(bs.body,
                                    (bs.keyword, "Python"), " → slides",
                                )
                            with l.item():
                                st_write(bs.body,
                                    (bs.keyword, "Themes"), " + dark mode",
                                )
                            with l.item():
                                st_write(bs.body,
                                    (bs.keyword, "Grids"), " responsive",
                                )
                            with l.item():
                                st_write(bs.body,
                                    (bs.keyword, "Navigation"), " built-in",
                                )

                st_space(size=2)

                # === L3 — Transition question ===
                st_write(
                    bs.question,
                    "What does it look like in practice?",
                    tag=t.div,
                )""", language="python")
    st_space("v", 2)

    show_details("""\
        Notice the IMAGE PROMPT comment: when no image is provided,
        the Slide Designer generates a detailed prompt you can paste
        into an image generator (DALL-E, Midjourney, etc.) to create
        a matching visual. It also suggests a filename following the
        bck_{description}.png convention.
    """)
    st_space("v", 2)

    st_slide_break(marker_label="tutorial_phase2")

    # ══════════════════════════════════════════════════════════════
    # PHASE 2 — Audit & Iterate
    # ══════════════════════════════════════════════════════════════
    st_write(bs.sub, "Phase 2 — Audit and Refine", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Once the project is generated, use the audit commands to
        validate quality and fix any issues automatically. This
        ensures every slide meets the design rules before you even
        open a browser.
    """)
    st_space("v", 2)

    # Step 4: Audit
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 4 — Audit the generated slides",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Run the slide audit to check all blocks against "
            "the design rules:",
        )
    st_space("v", 1)

    show_code(
        "/stx-block:audit",
        language="bash", line_numbers=False,
    )
    st_space("v", 1)

    show_code("""\
        # Example audit output
        bck_title ................. PASS (4/4)
        bck_the_problem ........... PASS (4/4)
        bck_the_solution .......... FAIL (3/4)
          - Formatting: line 38 exceeds 45 chars
        bck_live_demo ............. PASS (4/4)
        bck_getting_started ....... PASS (4/4)

        Result: 4/5 blocks pass — 1 fix required""",
        language="text", line_numbers=False)
    st_space("v", 2)

    # Step 5: Fix
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 5 — Auto-fix violations",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Let the AI fix the detected issues automatically:",
        )
    st_space("v", 1)

    show_code(
        "/stx-block:fix",
        language="bash", line_numbers=False,
    )
    st_space("v", 2)

    # Step 6: Add or refine individual slides
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 6 — Refine individual slides",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Need to adjust a specific slide? Use ",
            (bs.highlight, "/stx-block:update"),
            " to regenerate it with more details:",
        )
    st_space("v", 1)

    show_code("""\
        /stx-block:update "bck_live_demo — Show a responsive
        2-column grid: left column has a screenshot of a StreamTeX
        dark presentation, right column lists 4 key features as
        bold keywords. Add a wow-factor headline in L1." """,
        language="bash", line_numbers=False)
    st_space("v", 2)

    st_slide_break(marker_label="tutorial_phase3")

    # ══════════════════════════════════════════════════════════════
    # PHASE 3 — Run & Customize
    # ══════════════════════════════════════════════════════════════
    st_write(bs.sub, "Phase 3 — Run and Customize", toc_lvl="+1")
    st_space("v", 1)

    # Step 7: Run
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 7 — Launch the presentation",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Run the project and preview it in your browser:",
        )
    st_space("v", 1)

    show_code("""\
        cd projects/stx-discover-streamtex/
        stx run""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # Step 8: Customize theme
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 8 — Customize the visual theme",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Want a different color scheme or larger fonts for "
            "a conference room? Use ",
            (bs.highlight, "/stx-block:update"),
            ":",
        )
    st_space("v", 1)

    show_code("""\
        /stx-block:update "Switch to a teal/orange palette,
        increase body text to 48pt for a large auditorium." """,
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Style audit ──────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 9 — Verify style consistency",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "After theme changes, run a style audit to ensure "
            "all blocks use the updated palette consistently:",
        )
    st_space("v", 1)

    show_code("""\
        /stx-block:audit --target styles
        /stx-block:fix --target styles""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    st_slide_break(marker_label="tutorial_summary")

    # ══════════════════════════════════════════════════════════════
    # SUMMARY — Complete workflow
    # ══════════════════════════════════════════════════════════════
    st_write(
        bs.sub,
        "Summary: The Complete Workflow",
        toc_lvl="+1",
    )
    st_space("v", 1)

    with st_block(s.project.containers.ai_callout):
        st_write(
            s.project.titles.subsection_title,
            "From idea to running presentation in 9 steps",
            tag=t.div,
        )
        st_space("v", 1)
        with st_list(list_type="ol") as l:
            with l.item():
                st_write(
                    bs.phase_label, "init ",
                    (s.large, "— generate the full project from a description"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "Review ",
                    (s.large, "— check the generated structure and code"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "audit ",
                    (s.large, "— validate all blocks against design rules"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "fix ",
                    (s.large, "— auto-fix detected violations"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "update ",
                    (s.large, "— refine or add individual slides"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "Run ",
                    (s.large, "— preview in the browser"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "update ",
                    (s.large, "— customize theme, fonts, colors"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "audit --target styles ",
                    (s.large, "— ensure consistency after changes"),
                )
            with l.item():
                st_write(
                    bs.phase_label, "Iterate ",
                    (s.large, "— repeat steps 3-8 until satisfied"),
                )
    st_space("v", 2)

    # ── Key commands reference ───────────────────────────────────
    st_write(bs.sub, "Quick Reference: Key Commands", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        # Create a full project from scratch
        /stx-block:init "description..."

        # Create or refine a single slide
        /stx-block:update "bck_name — description..."

        # Audit and fix design compliance
        /stx-block:audit
        /stx-block:fix

        # Customize visual theme
        /stx-block:update "description..."

        # Ensure style consistency
        /stx-block:audit --target styles
        /stx-block:fix --target styles

        # Run the presentation
        stx run""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Final tips ───────────────────────────────────────────────
    show_details("""\
        Tips for best results:
        • Be specific in your descriptions — include audience,
          slide count, theme, and key messages per slide.
        • Always run /stx-block:audit after generation — the AI catches
          issues like line length, missing spacing, or style violations.
        • Use /stx-block:update for individual refinements — it's faster
          than regenerating the entire project.
        • The Slide Designer follows the L1/L2/L3 grid system:
          L1 = headline, L2 = image + text grid, L3 = transition question.
        • Image prompts are generated automatically when no image is
          provided — paste them into DALL-E, Midjourney, or similar tools.
    """)
    st_space("v", 1)
