"""CE Manual — Master Plan (pilotage + content reference vivante)."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Master plan block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Master plan — central living reference for the CE cycle."""

    st_space("v", 1)
    st_write(bs.heading, "The Master Plan — living reference of the cycle",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.bold, "master plan"),
             " is the single source of truth for the document being produced. "
             "It evolves across iterations and is read at the start of every CE skill.")
    st_space("v", 1)

    show_explanation("""\
    ### Two paired files

    The master plan lives as **two paired files** in the project's `docs/` directory:

    | File | Role |
    |---|---|
    | `docs/master-plan.yaml` | **Pilotage** — machine-readable metadata: identity, objectives, TOC statuses, transverse decisions, patterns mapping, iterations history, decisions log, coherence debt, pointers |
    | `docs/master-plan.md` | **Contenu détaillé** — human-readable: TOC hiérarchique avec, par nœud, intention / sources / notes de conception / propositions brutes de contenu |

    Both files are always kept in sync. Snapshots are taken as paired files in
    `docs/master-plan/archive/YYYY-MM-DD-NNN.{yaml,md}` (same timestamp prefix).
    """)
    st_space("v", 1)

    show_explanation("""\
    ### When the master plan is initialized

    - **First iteration of a new document**: ASSESS creates both files at the end of its phase, from the requirements and objectives captured in dialogue with you.
    - **Subsequent iterations**: ASSESS enriches the existing files. PLAN, PROTOTYPE, PRODUCE, REVIEW, FIX, COMPOUND, and INTEGRATE all read and update them.
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Snapshot policy

    A new paired snapshot is written when **at least one of the two files differs
    from the most recent snapshot**. This naturally enforces "at most one snapshot
    per session" without an explicit session id.

    Additional snapshots can be triggered:
    - On user demand (QCM with `Oui` recommended)
    - Before destructive operations (TOC removal, batch reconciliation)
    - At session end via "interruption douce" (QCM with `Oui` recommended)

    All snapshots are kept. COMPOUND proposes partial purge via QCM when the
    archive grows large. Snapshots do **not** reference any git commit hash —
    the archive is git-independent.
    """)
    st_space("v", 1)

    show_explanation("""\
    ### Reconciliation with book.py

    The order of `bck_*` references in `book.py` is the live state of production.
    The master plan TOC is the planned state. They can diverge — typically when
    you edit `book.py` manually between sessions.

    At the start of every session (`/stx-ce:continue`), the orchestrator runs
    the `plan-reconciler` agent. If divergence is detected, a single QCM
    proposes a global reconciliation:

    - **Appliquer la proposition globale** *(Recommandé)* — applies the LLM's reasoning
    - **Voir le détail bloc par bloc** — drills down to per-divergence QCM
    - **Discutons-en** — opens dialogue

    Refused divergences are inscribed as entries in the YAML's `coherence_debt`
    section.
    """)
    st_space("v", 1)

    show_details("""\
    ### Decisions log

    Every QCM presented to you (in any CE skill) is appended to the YAML's
    `decisions_log`:

    ```yaml
    - timestamp: 2026-05-13T14:32:11Z
      question: "Avant de produire les 8 blocs, je propose un bloc pilote..."
      options_presented: ["Oui (Recommandé)", "Non", "Discutons-en", "Autre"]
      recommendation: "Oui (Recommandé)"
      answer: "Oui (Recommandé)"
      skill: ce-prototype
    ```

    Decisions can be reopened automatically by the orchestrator when new
    information emerges. The reopening is itself a QCM that references the
    prior decision in its question text — nothing is silently overridden.
    """)
    st_space("v", 1)
