"""CE Manual — Part 2: INTEGRATE Phase."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """INTEGRATE phase styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """INTEGRATE phase: route solutions to operational destinations."""

    st_space("v", 1)
    st_write(bs.heading, "INTEGRATE — Route Solutions to Operations",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "The ",
             (s.project.titles.phase_kw, "INTEGRATE"),
             " phase closes the loop opened by COMPOUND. Where COMPOUND "
             "captures learnings as solution files, INTEGRATE routes them "
             "to their operational destinations so they take effect in "
             "future sessions.")
    st_space("v", 1)

    st_write(s.large,
             "Without INTEGRATE, solutions remain inert files in "
             "`docs/solutions/`. With it, they become rules, tickets, "
             "and patterns that improve every future cycle.")
    st_space("v", 1)

    show_explanation("""\
    ### The Routing Table

    Each solution is classified by destination:

    | Destination | Target | Method |
    |-------------|--------|--------|
    | **streamtex** (lib) | Library bugs or features | `/stx-issue:feature` or `/stx-issue:bug` |
    | **streamtex-claude** (plugin) | Skill, command, template changes | `/stx-issue:feature` or `/stx-issue:bug` |
    | **streamtex-docs** (docs) | Documentation improvements | `/stx-issue:docs` |
    | **Author custom** | `.claude/custom/references/` | Direct file update |
    | **Design guideline** | `custom/design-guideline.md` | Direct pattern update |

    Classification is based on content analysis:
    - Solutions mentioning `st_*` functions → streamtex
    - Solutions mentioning skills, commands → streamtex-claude
    - Solutions about coding conventions → author custom
    - Solutions about visual patterns → design guideline
    """)

    st_space("v", 1)

    show_explanation("""\
    ### How It Works

    ```
    /stx-ce:integrate
    ```

    1. **Load**: Scan `docs/solutions/` for files where `integrated: false`
    2. **Classify**: Determine destination for each solution
    3. **GATE**: Present routing table to user for validation
    4. **Execute**:
       - Repos → create GitHub issues via `/stx-issue:*`
       - Author → update `.claude/custom/references/` files
       - Guideline → update `custom/design-guideline.md` patterns
    5. **Mark**: Set `integrated: true` in solution frontmatter

    **Options:**
    - `--dry-run` — preview routing without applying
    - `--target <file>` — integrate a single solution

    Solutions can have **multiple destinations** (e.g., a rule for the
    author + a ticket for the plugin).
    """)

    st_space("v", 1)

    show_details("""\
    ### Solution Frontmatter (after integration)

    ```yaml
    ---
    title: Factorize duplicate styles
    category: style
    scope: collection
    tags: [styles, DRY, refactoring]
    integrated: true
    integrated_date: 2026-04-05
    integrated_to: .claude/custom/references/style-rules.md
    ---
    ```

    The `integrated_to` field tracks where the solution was routed:
    - `streamtex#42` — lib issue number
    - `streamtex-claude#18` — plugin issue number
    - `.claude/custom/references/style-rules.md` — author custom file
    - `skipped` — user chose to skip this solution
    """)
