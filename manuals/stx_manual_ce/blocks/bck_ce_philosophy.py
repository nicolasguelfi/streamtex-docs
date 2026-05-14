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

    # ── Principle 2: Iterative + Incremental ──────────────────────
    st_write(bs.sub, "Iterative and incremental: cycles + scope, not waterfall", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A single CE cycle takes your material from raw to refined.
        But one cycle is rarely enough for a complex document, and the
        scope of each cycle does not have to be the whole document.

        CE supports two orthogonal axes of progress:

        - **Iterative**: a first cycle produces a rough draft, a second
          improves structure and style, a third polishes for the target
          audience. Each cycle leaves the document in a coherent state.
        - **Incremental**: a cycle can cover the **full document** or just
          an **increment** — a part, a section, a single block. The scope
          is determined by contextual dialogue at the start of each cycle,
          not by flags. Increments accumulate into the **master plan**, a
          git-independent living reference paired across
          `docs/master-plan.yaml` (orchestration) and
          `docs/master-plan.md` (content).

        Each cycle is short (minutes to hours, not days) because the AI
        handles the mechanical work while you make decisions at the four
        fundamental validation gates (post-PLAN, post-REVIEW, post-FIX,
        post-INTEGRATE).
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
            st_write((s.project.titles.pathway_kw, "Pathway A — Import"), ": you have external material "
                     "(HTML, PDF, Marp, Markdown) to bring into StreamTeX.")
        with l.item():
            st_write((s.project.titles.pathway_kw, "Pathway B — Improve"), ": you have an existing "
                     "StreamTeX project that needs restructuring or polish.")
        with l.item():
            st_write((s.project.titles.pathway_kw, "Pathway C — Create"), ": you start from a description "
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
        like `--import`, `--improve`, or `--create`. Each pathway
        is compatible with both full-document and incremental scopes.
    """)
    st_space("v", 2)

    # ── Principle 5: Universal QCM with escape hatches ────────────
    st_write(bs.sub, "Universal QCM with two escape hatches", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Every user-facing decision in CE goes through a single QCM
        contract — no free-text prompts, no hidden flag combinations.

        - **Option 1** is suffixed `(Recommandé)` and reflects the LLM's
          contextual reasoning about the best default for your project.
        - **0 to 2 business alternatives** follow.
        - **`Discutons-en`** opens a free dialogue if the proposed
          choices do not fit.
        - **`Autre`** is auto-injected by the QCM tool and accepts
          arbitrary user input.

        This format never changes. Only its **frequency** is tunable,
        via the `dialog_level` field of `docs/solutions/producer-profile.md`:

        - `minimal` — QCM only at the 4 fundamental gates.
        - `guided` — QCM at all structuring decisions (default).
        - `exhaustive` — QCM on every choice, even minor.

        The contract is documented as the canonical reference in the
        `ce-conventions` skill that every CE skill reads before
        surfacing any question. The principle is **anti-sur-engineering**:
        the LLM uses the context, the user always retains two escape
        hatches, and process overhead never accumulates.
    """)
    st_space("v", 1)
