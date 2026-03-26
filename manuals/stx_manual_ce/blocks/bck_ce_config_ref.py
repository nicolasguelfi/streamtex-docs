"""CE Manual — Part 5: Configuration Reference."""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details


class BlockStyles:
    """Configuration Reference styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Configuration reference: directory structure, naming, severity levels,
    producer profile format, git preferences."""

    st_space("v", 1)
    st_write(bs.heading, "Configuration Reference",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    st_write(s.large,
             "Compound Document Engineering relies on conventions rather than "
             "configuration files. This reference documents the directory "
             "structure, naming rules, severity levels, and other conventions "
             "that CE ", (s.project.titles.concept_kw, "agents"), " expect.")
    st_space("v", 1)

    show_details("""
    ### Project Directory Structure

    CE artifacts live in the `docs/` directory within your StreamTeX project:

    ```
    my-project/
    +-- blocks/                  # StreamTeX block files
    |   +-- bck_intro.py
    |   +-- bck_chapter1.py
    +-- custom/
    |   +-- styles.py            # Project styles
    +-- docs/                    # CE artifacts directory
    |   +-- inventory.md         # Source inventory (COLLECT)
    |   +-- assessment.md        # Assessment brief (ASSESS)
    |   +-- plan.md              # Structure plan (PLAN)
    |   +-- review.md            # Review findings (REVIEW)
    |   +-- profile.md           # Producer profile (COMPOUND)
    |   +-- solutions/           # Reusable solution packages
    |   |   +-- sol_api_ref_structure.md
    |   |   +-- sol_tutorial_progression.md
    |   +-- feedback/            # Ecosystem feedback drafts
    |       +-- fb_001_missing_feature.md
    +-- book.py                  # StreamTeX book definition
    +-- pyproject.toml
    ```

    The `docs/` directory is created automatically by `/stx-ce:collect`
    if it does not exist. All CE commands read from and write to this
    directory.
    """)

    st_space("v", 1)

    show_details("""
    ### File Naming Conventions

    | Artifact | Pattern | Example |
    |----------|---------|---------|
    | Inventory | `inventory.md` | `docs/inventory.md` |
    | Assessment | `assessment.md` | `docs/assessment.md` |
    | Plan | `plan.md` | `docs/plan.md` |
    | Review | `review.md` | `docs/review.md` |
    | Profile | `profile.md` | `docs/profile.md` |
    | Solution | `sol_<description>.md` | `docs/solutions/sol_api_ref_structure.md` |
    | Feedback | `fb_<number>_<description>.md` | `docs/feedback/fb_001_missing_feature.md` |
    | Block files | `bck_<name>.py` | `blocks/bck_intro_welcome.py` |

    **Naming rules:**
    - Use lowercase with underscores (snake_case)
    - Solution files start with `sol_`
    - Feedback files start with `fb_` followed by a sequential number
    - Block files always start with `bck_`
    """)

    st_space("v", 1)

    show_details("""
    ### Severity Levels

    CE uses a consistent 4-level severity scale across all phases:

    | Level | Code | Meaning | Action |
    |-------|------|---------|--------|
    | CRITICAL | `CRITICAL` | Prevents the document from being usable | Must fix before any release |
    | MAJOR | `MAJOR` | Significantly impacts quality | Should fix in current cycle |
    | MINOR | `MINOR` | Small improvement opportunity | Fix if time permits |
    | SUGGESTION | `SUGGESTION` | Stylistic or optional improvement | Consider for next cycle |

    **Severity is used in:**
    - Gap reports (ASSESS phase): gaps rated by impact on document goals
    - Review findings (REVIEW phase): issues rated by impact on reader experience
    - Fix prioritization (FIX phase): `--severity` flag filters what gets fixed

    **Escalation rule**: if a `MINOR` issue appears in 3+ blocks, it is
    automatically escalated to `MAJOR` (systemic problem).
    """)

    st_space("v", 1)

    show_explanation("""
    ### Producer Profile Format

    The producer profile in `docs/profile.md` follows a structured format
    that CE agents can read and update programmatically:

    ```
    ---
    template: producer_profile
    author: <name>
    last_updated: <date>
    cycles_completed: <count>
    ---

    ## Writing Style
    - Tone: <formal|semi-formal|informal>
    - Sentence length: <short|medium|varied>
    - Example frequency: <every-concept|key-concepts|minimal>

    ## Structural Preferences
    - Max block length: <lines>
    - Preferred block types: <list>
    - Part size: <number of blocks per part>

    ## Quality Standards
    - Minimum review pass: <severity level>
    - Required perspectives: <list of reviewers>
    - Auto-fix threshold: <severity>

    ## Lessons Learned
    - <date>: <insight from a specific cycle>
    ```

    The profile is optional but strongly recommended. A project without
    a profile gets default agent behavior; a project with a detailed
    profile gets tailored recommendations.
    """)

    st_space("v", 1)

    show_details("""
    ### Configuration Objects

    CE agents recognize the following configuration objects when they appear
    in plan templates or project code. These extend the base StreamTeX
    configuration with CE-specific settings:

    | Object | Purpose | Typical Location |
    |--------|---------|------------------|
    | `BibConfig` | Bibliography setup: sources, citation style, BibTeX file path | `docs/plan.md`, `book.py` |
    | `AIImageConfig` | AI image generation: provider, default size, quality, cache | `docs/plan.md`, `book.py` |
    | `SpacingConfig` | Section spacing: vertical space between parts, blocks, elements | `docs/plan.md`, `custom/styles.py` |
    | `ProfileConfig` | Presentation profile: layout mode, slide dimensions, transitions | `docs/plan.md`, `book.py` |
    | `GSheetConfig` | Google Sheets integration: sheet ID, credentials, sync options | `docs/plan.md`, `book.py` |
    | `ExportConfig` | Export settings: PDF format, page size, `AssetMode` (inline/linked) | `docs/plan.md`, `book.py` |

    **`AssetMode`** (used by `ExportConfig`):
    - `AssetMode.INLINE` — embed images as base64 in exported HTML/PDF
    - `AssetMode.LINKED` — reference images as external files

    These objects are documented in the plan template so that PRODUCE agents
    can apply them consistently across all blocks.
    """)

    st_space("v", 1)

    show_details("""
    ### Requirements Coverage (R1-R26)

    CE assessment covers 26 requirements organized by category:

    | Range | Category | Examples |
    |-------|----------|---------|
    | R1-R8 | Content quality | Accuracy, completeness, clarity, audience fit |
    | R9-R14 | Structure | Navigation, hierarchy, block organization, flow |
    | R15-R18 | Visual & style | Consistency, readability, theme compliance |
    | R19-R21 | Bibliography | Citation presence, BibTeX validity, reference completeness |
    | R22-R24 | AI images | Provider config, prompt quality, cache usage |
    | R25-R26 | Export | PDF rendering, asset mode consistency |

    The ASSESS phase evaluates all 26 requirements. The REVIEW phase
    checks compliance. The FIX phase addresses violations by severity.
    """)

    st_space("v", 1)

    show_details("""
    ### Git Preferences

    CE integrates with git for versioning artifacts:

    | Convention | Format | Example |
    |------------|--------|---------|
    | Collect commit | `ce(collect): <summary>` | `ce(collect): inventory 12 HTML sources` |
    | Assess commit | `ce(assess): <summary>` | `ce(assess): 5 critical gaps identified` |
    | Plan commit | `ce(plan): <summary>` | `ce(plan): 8 blocks across 3 parts` |
    | Produce commit | `ce(produce): <block>` | `ce(produce): bck_intro_welcome` |
    | Review commit | `ce(review): <summary>` | `ce(review): 2 CRITICAL, 5 MAJOR` |
    | Fix commit | `ce(fix): <summary>` | `ce(fix): resolve 2 CRITICAL` |
    | Compound commit | `compound(<axis>): <desc>` | `compound(solution): API ref structure` |

    **Git behavior is opt-in**: CE commands do not auto-commit unless you
    pass `--commit` or have `auto_commit = true` in your profile.
    """)

    st_space("v", 1)
