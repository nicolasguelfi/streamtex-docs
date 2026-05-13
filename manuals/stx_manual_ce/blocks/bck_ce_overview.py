"""What is Compound Document Engineering? — CE methodology overview."""

from streamtex import *
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """CE Overview styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Render the CE overview page."""
    st_space("v", 1)
    st_write(bs.heading, "What is Compound Document Engineering?",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Why CE exists ─────────────────────────────────────────────
    st_write(bs.sub, "Why CE exists", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Most document projects do not start from a blank page.
        You have slides from a previous talk, notes from a meeting,
        a PDF from a colleague, or HTML from a website.

        Traditional approaches assume top-down authoring: outline first,
        then write. CE takes the opposite approach — **bottom-up** — because
        that matches how real work happens: you start from existing material
        and shape it into a coherent document.
    """)
    st_space("v", 1)

    # ── Ad-hoc vs CE ─────────────────────────────────────────────
    st_write(bs.sub, "Ad-hoc production vs CE", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             (s.bold, "Ad-hoc production"), " copies, pastes, and reformats "
             "material by hand. It works for small tasks but does not scale: "
             "lessons are lost, quality is inconsistent, and every project "
             "starts from scratch.")
    st_space("v", 1)
    st_write(s.large,
             (s.bold, "CE"), " adds structure with a repeatable 7-phase cycle. "
             "Each cycle produces a better document ", (s.italic, "and"),
             " captures what you learned for next time.")
    st_space("v", 2)

    # ── The 8-phase cycle ─────────────────────────────────────────
    st_write(bs.sub, "The 8-phase cycle", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A CE cycle has eight phases executed in order.
        Each phase has a clear input, output, and validation gate.

        **COLLECT** — Inventory and classify existing material.
        **ASSESS** — Evaluate material and define document objectives. Initializes the master plan on first iteration.
        **PLAN** — Design the production plan (structure, blocks, styles, patterns mapping).
        **PROTOTYPE** — Validate styles by example with a pilot block; capture reusable patterns into the local catalog.
        **PRODUCE** — Execute the plan using stx-block and stx-import; apply validated patterns.
        **REVIEW** — Multi-perspective quality review (5 lenses).
        **FIX** — Correct issues; propose ré-application of new patterns to prior blocks.
        **COMPOUND** — Capitalize learnings; promote emergent patterns to local catalog.
        **INTEGRATE** — Route solutions to operational destinations; propose promotion of local patterns to the shared catalog.
    """)
    st_space("v", 1)

    with st_list(list_type=lt.ordered, li_style=s.large, align="center") as l:
        with l.item(): st_write((s.project.titles.phase_kw, "COLLECT"), " — scan files, classify formats, evaluate importability")
        with l.item(): st_write((s.project.titles.phase_kw, "ASSESS"), " — detect pathway (A/B/C), define objectives, initialize the master plan")
        with l.item(): st_write((s.project.titles.phase_kw, "PLAN"), " — structure, block list, style choices, production order, patterns mapping")
        with l.item(): st_write((s.project.titles.phase_kw, "PROTOTYPE"), " — pilot block, validate styles, capture patterns")
        with l.item(): st_write((s.project.titles.phase_kw, "PRODUCE"), " — create or import blocks, wire book.py, apply patterns")
        with l.item(): st_write((s.project.titles.phase_kw, "REVIEW"), " — audience, pedagogy, visual, style, editorial checks")
        with l.item(): st_write((s.project.titles.phase_kw, "FIX"), " — correct automatable issues, ré-apply patterns to prior blocks")
        with l.item(): st_write((s.project.titles.phase_kw, "COMPOUND"), " — production log, ecosystem feedback, pattern catalog enrichment")
        with l.item(): st_write((s.project.titles.phase_kw, "INTEGRATE"), " — route solutions to lib issues, skill updates, shared catalog")
    st_space("v", 2)

    # ── Iterative and incremental cycle ──────────────────────────
    st_write(bs.sub, "Iterative and incremental — scope chosen by dialogue", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The eight phases can cover the **full document** or an **increment**:
        a part, a section, or even a single block. Each session, the
        orchestrator reads the master plan and proposes the appropriate scope
        via QCM:

        - First iteration of a new document → recommend `Document complet`.
        - Partial production already on the way → recommend `Continuer l'incrément courant`.
        - Document complete → propose new improvements or close the project.

        You never type a scope flag — the LLM detects the right scope and
        confirms with you. Two escape options are always available in any QCM:
        `Discutons-en` (free dialogue) and `Autre` (free text input).
    """)
    st_space("v", 1)

    # ── Iterative nature ──────────────────────────────────────────
    st_write(bs.sub, "Iterative, not waterfall", toc_lvl="+1")
    st_space("v", 1)

    show_details("""\
        The REVIEW and FIX phases form a tight inner loop: review
        findings feed directly into fixes, and you can re-review
        until quality gates pass.

        The COMPOUND phase captures learnings as solutions.
        The INTEGRATE phase routes them to operational destinations
        (lib issues, skill updates, custom rules). Together, they
        close the outer loop: every cycle improves the next.

        You can run a full cycle with `/stx-ce:go "description"`
        or execute phases individually for fine-grained control.
    """)
    st_space("v", 1)

    # ── Extended capabilities ────────────────────────────────────
    st_write(bs.sub, "Extended capabilities", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large,
             "Beyond the sequential pipeline, CE provides ",
             (s.bold, "ad-hoc task execution"),
             " via ", (s.project.titles.tool_kw, "/stx-ce:task"),
             " for punctual work (coverage audits, targeted reviews, plan amendments), "
             "and ", (s.project.titles.tool_kw, "/stx-ce:continue"),
             " for session resumption with drift detection and prioritized proposals.")

    st_space("v", 1)

    show_details("""\
        The CE cycle integrates several advanced StreamTeX features
        that enrich document production:

        - **Bibliography management** — cite sources with `st_bibliography`,
          load `.bib`, `.ris`, and CSL-JSON files, multiple citation styles.
        - **AI image generation** — multi-provider support (OpenAI, Google,
          fal.ai) with caching and version control.
        - **Presentation profiles** — responsive layouts with multi-device
          preview and audience-specific rendering.
        - **Section spacing configuration** — fine-grained vertical rhythm
          tuning across parts and blocks.
        - **LaTeX import** — `/stx-import:latex` converts LaTeX documents
          into StreamTeX blocks.
        - **Google Sheets integration** — live data from spreadsheets as
          tables, charts, or block content.
    """)
    st_space("v", 1)
