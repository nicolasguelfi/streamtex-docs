"""CE Principles — Core philosophy behind Compound Document Engineering."""

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """CE Philosophy styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Render the CE principles page."""
    st_space("v", 1)
    st_write(bs.heading, "Principles",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Principle 1: Bottom-up ────────────────────────────────────
    st_write(bs.sub, "Bottom-up: material first, not ideas", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Classical document authoring starts with an outline and fills it in.
        CE reverses this: you start from **what you already have** — files,
        notes, slides, code, screenshots — and let the structure emerge
        from the material.

        This is more honest about how knowledge work actually happens.
        You rarely begin with nothing; you begin with too much unorganized
        material. CE gives you a systematic way to tame it.
    """)
    st_space("v", 2)

    # ── Principle 2: Iterative ────────────────────────────────────
    st_write(bs.sub, "Iterative: cycles, not waterfall", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A single CE cycle takes your material from raw to refined.
        But one cycle is rarely enough for a complex document.

        CE is designed for **multiple passes**: a first cycle produces
        a rough draft, a second cycle improves structure and style,
        a third polishes for the target audience.

        Each cycle is short (minutes to hours, not days) because
        the AI handles the mechanical work while you make decisions
        at the validation gates.
    """)
    st_space("v", 2)

    # ── Principle 3: Capitalization ───────────────────────────────
    st_write(bs.sub, "Capitalization: learn from every cycle", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The COMPOUND phase is what makes CE different from a simple
        checklist. After every cycle, you capture three things:

        1. **Production learnings** — what worked, what did not,
           timing data, quality metrics.
        2. **Ecosystem feedback** — missing features, style gaps,
           tool improvements to report upstream.
        3. **Governance** — updated templates, checklists, and
           best practices for your team.

        These artifacts live in `docs/` and accumulate over time,
        making each subsequent project faster and better.
    """)
    st_space("v", 2)

    # ── Principle 4: Three pathways ───────────────────────────────
    st_write(bs.sub, "Three pathways for three situations", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "CE recognizes that not all projects start the same way. "
             "The ASSESS phase automatically detects which pathway fits:")
    st_space("v", 1)

    with st_list(list_type=lt.unordered, li_style=s.large, align="center") as l:
        with l.item():
            st_write((s.bold, "Pathway A — Import"), ": you have external material "
                     "(HTML, PDF, Marp, Markdown) to bring into StreamTeX.")
        with l.item():
            st_write((s.bold, "Pathway B — Improve"), ": you have an existing "
                     "StreamTeX project that needs restructuring or polish.")
        with l.item():
            st_write((s.bold, "Pathway C — Create"), ": you start from a description "
                     "or outline and build a new document from scratch.")
    st_space("v", 1)

    show_details("""\
        The pathway determines which phases are emphasized:

        - **Pathway A** spends most time in COLLECT and PRODUCE
          (scanning and converting files).
        - **Pathway B** focuses on ASSESS and REVIEW (understanding
          what exists and what to improve).
        - **Pathway C** emphasizes PLAN and PRODUCE (designing
          structure and generating content).

        You can override the detected pathway with explicit flags
        like `--import`, `--improve`, or `--create`.
    """)
    st_space("v", 1)
