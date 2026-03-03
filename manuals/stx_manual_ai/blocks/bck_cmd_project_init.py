"""Command: project-init — Create a StreamTeX project from natural language."""

import textwrap

from streamtex import st_write, st_space, st_block
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """project-init block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step_label = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Render the project-init command documentation."""
    st_space("v", 1)
    st_write(bs.heading, "Command: project-init", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Purpose ────────────────────────────────────────────────────
    show_explanation(textwrap.dedent("""\
        /project:project-init creates a complete, ready-to-run
        StreamTeX project from a simple natural language description.
        It generates the directory structure, styles, starter blocks,
        and the orchestration file (book.py) in one pass.
    """))
    st_space("v", 2)

    # ── Step-by-step demo ──────────────────────────────────────────
    st_write(bs.sub, "Step-by-Step Demo", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    # Step 1
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label, "Step 1 — Launch the command", tag=t.div)
        st_space("v", 1)
        st_write(
            s.large,
            "Type the slash command in your Claude Code session:",
        )
    st_space("v", 1)

    show_code("/project:project-init", language="bash", line_numbers=False)
    st_space("v", 2)

    # Step 2
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 2 — Describe your project",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "The AI asks what you want to build. Be specific:",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        > A 10-slide course on machine learning basics.
          Target audience: university students.
          Include: title page, table of contents, 8 content slides,
          summary slide. Use a blue/purple tech theme."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # Step 3
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 3 — Review the generated structure",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "The AI creates four artefacts in your project directory:",
        )
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        my_ml_course/
        ├── book.py                  # Orchestration
        ├── blocks/
        │   ├── __init__.py          # Block registry
        │   ├── helpers.py           # Project helpers
        │   ├── bck_01_title.py      # Title page
        │   ├── bck_02_toc.py        # Table of contents
        │   ├── bck_03_what_is_ml.py # Content slide
        │   ├── ...                  # 5 more content blocks
        │   └── bck_10_summary.py    # Summary slide
        ├── custom/
        │   └── styles.py            # Blue/purple tech theme
        └── .streamlit/
            └── config.toml          # Streamlit configuration"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # Step 4
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.step_label,
            "Step 4 — Run and iterate",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            "Launch the project and refine individual blocks:",
        )
    st_space("v", 1)

    show_code(
        "uv run streamlit run my_ml_course/book.py",
        language="bash", line_numbers=False,
    )
    st_space("v", 2)

    # ── Example generated book.py ──────────────────────────────────
    st_write(bs.sub, "Example: Generated book.py", tag=t.div, toc_lvl="2")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        \"\"\"Machine Learning Basics — 10-slide course.\"\"\"

        from streamtex import st_book

        blocks = [
            "bck_01_title",
            "bck_02_toc",
            "bck_03_what_is_ml",
            "bck_04_supervised",
            "bck_05_unsupervised",
            "bck_06_neural_nets",
            "bck_07_training",
            "bck_08_evaluation",
            "bck_09_applications",
            "bck_10_summary",
        ]

        st_book(blocks, paginate=True)"""), language="python")
    st_space("v", 2)

    # ── Tip ────────────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Tip: the more specific your description, the better the result.
        Include audience, number of slides, theme preferences, and any
        special requirements (diagrams, code examples, quizzes). Vague
        prompts like "make a presentation" produce generic scaffolding.
    """))
    st_space("v", 1)
