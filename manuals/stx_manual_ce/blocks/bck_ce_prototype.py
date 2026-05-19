"""CE Manual — PROTOTYPE phase (validation par l'exemple, capture des patterns)."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """PROTOTYPE phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """PROTOTYPE phase: validate styles by example, capture reusable patterns."""

    st_space("v", 1)
    st_write(bs.heading, "PROTOTYPE — Validate by Example, Capture Patterns",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "PROTOTYPE"),
             " phase sits between ",
             (s.project.titles.phase_kw, "PLAN"),
             " and ",
             (s.project.titles.phase_kw, "PRODUCE"),
             ". It validates visual decisions by producing a pilot block and "
             "captures emergent patterns into the local catalog before mass production.")
    st_space("v", 1)

    show_explanation("""\
    ### Why a PROTOTYPE phase

    Defining styles on paper before producing any block is brittle. Compositions
    that look right in a planning document may not work once rendered. PROTOTYPE
    inverts the order:

    1. Produce **one** representative block (the pilot).
    2. Show it rendered to the user.
    3. Iterate styles until validated.
    4. Capture the validated compositions as **named patterns** in the catalog.
    5. Then run PRODUCE on the remaining blocks with the validated patterns.

    Subsequent iterations of the same visual territory can skip PROTOTYPE — the
    patterns are already validated and applied automatically.
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Auto-trigger rule

    PROTOTYPE runs when at least one of the following is true:

    - First iteration of the document (no patterns validated yet).
    - The current increment introduces a new visual territory (new palette,
      new presentation profile, new layout class).
    - The user explicitly requested validation of styles before production.

    In all other cases, PROTOTYPE is skipped silently — `ce-go` makes the
    decision and confirms via a QCM in `dialog_level: guided` and `exhaustive`.
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Pilot selection

    The `prototype-designer` agent picks the pilot block. Two strategies:

    | Strategy | When | Output |
    |---|---|---|
    | Single pilot *(recommandé par défaut)* | Small increment, homogeneous content | 1 block |
    | Set covering archetypes | Heterogeneous increment with several archetypes | 1 block per archetype |

    The agent presents its choice with rationale via QCM. You can always
    select `Discutons-en` to refine.
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Pattern strategy

    For each visual component of the pilot, the agent classifies its plan:

    - **reuse_as_is** — a pattern from the catalog fits exactly.
    - **reuse_adapted** — a pattern fits if specific `PARAMS` are tuned.
    - **create_new** — no pattern fits, propose a candidate name and capture.
    - **ad_hoc** — one-shot composition not worth pattern-izing.

    The QCM presents the recommendation with all four columns visible, plus
    `Discutons-en` and `Autre` as escapes.
    """)
    st_space("v", 1)

    show_details("""\
    ### Command reference

    ```bash
    # Run PROTOTYPE on the current iteration's scope
    /stx-ce:prototype

    # Within /stx-ce:go, PROTOTYPE is auto-triggered between PLAN and PRODUCE.
    ```

    The phase generates a report in `docs/prototypes/YYYY-MM-DD-NNN-<scope>-prototype.md`.
    Captured components are written into the project's **primary local pack**
    (`./mypack/components/` by default — cf. PLAN §8.1, streamtex 0.7.x).
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Three-level component catalog

    | Level | Location | Captured from | Promoted via |
    |---|---|---|---|
    | `draft` | `docs/solutions/style/components/` | extraction in PROTOTYPE or COMPOUND | automatic |
    | `local` | `./mypack/components/` (primary local pack) | draft | QCM in PROTOTYPE or COMPOUND |
    | `shared` | a `git` or `pypi` pack declared in `stx.toml` | local | `stx component promote <name> --to=<pack>` (QCM in INTEGRATE) |

    Components capture by name (`callout`, `evidence_insight`, ...) become
    reusable across blocks and across projects via the reuse architecture.
    """)
    st_space("v", 1)
