"""Authoring a new pattern — end-to-end walkthrough.

# @pattern: ptn_feature_walkthrough
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Authoring walkthrough styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Walk a pattern author through creating, validating, and
    submitting a new pattern."""
    st_space("v", 1)
    st_write(bs.heading, "Authoring — Add a New Pattern",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ---- Step 1 ----
    st_write(bs.sub, "Step 1: Decide the scope", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Before writing anything, choose where the pattern lives:

        - `core/` — universal atom or molecule, useful in any
          StreamTeX project.
        - `slides/` — only useful in slide-based courses or talks.
        - `docs/` — only useful in documentation manuals.
        - `projects/<X>/` — ultra-specific to one project.

        If unsure, start in `projects/<X>/` and promote later if it
        proves general.
    """)
    st_space("v", 1)

    show_code("""\
# Workspace tree
streamtex-patterns/
├── core/      <-- universal
├── slides/    <-- presentations only
├── docs/      <-- manuals only
└── projects/<X>/  <-- one specific project
""", language="text")
    st_space("v", 2)

    # ---- Step 2 ----
    st_write(bs.sub, "Step 2: Create the pattern file", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Create `<scope>/<name>.md` and paste the Format A2 skeleton.
        Fill in each required section — Visual, Structure, Styling
        rules, Code skeleton, Extrapolation rules (INVARIANTS / PARAMS
        / INTERDITS), When to use, When NOT to use.

        Use an existing pattern as a starting point — copying
        `core/callout.md` or `docs/manual_section.md` is a good
        habit.
    """)
    st_space("v", 1)

    show_code("""\
# core/my_new_pattern.md
---
name: my_new_pattern
type: pattern
description: <one-line description>
tags: [<tag1>, <tag2>]
extrapolable: true
since: 2026-05-10
---

# <Pattern Name>

<one-paragraph teaser>

## Visual
...
## Structure
...
## Styling rules
...
## Code skeleton
...
## Extrapolation rules
### INVARIANTS
### PARAMS
### INTERDITS
## When to use
## When NOT to use
""", language="markdown")
    st_space("v", 2)

    # ---- Step 3 ----
    st_write(bs.sub, "Step 3: Validate locally", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Run the validation script on your draft. It checks:

        - Frontmatter keys present and well-formed.
        - All required H2 sections present (per `manifest.toml`).
        - INVARIANTS / PARAMS / INTERDITS subsections present under
          `## Extrapolation rules`.
        - No broken cross-references (`Related patterns` resolve to
          existing files).
    """)
    st_space("v", 1)

    show_code("""\
cd streamtex-patterns
uv run python scripts/validate.py core/my_new_pattern.md

# Or validate the whole catalog
uv run python scripts/validate.py --all
""", language="bash")
    st_space("v", 2)

    # ---- Step 4 ----
    st_write(bs.sub, "Step 4: Add to the right preset", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        If the pattern belongs to an existing preset (`core`,
        `slides`, `docs`, `minimal`, `ai4se6d`), add a line to the
        corresponding `presets/<name>.toml` so consumers get it on
        their next `stx patterns update`.
    """)
    st_space("v", 1)

    show_code("""\
# presets/docs.toml — append the new pattern
[patterns]
include = [
  "docs/manual_section.md",
  "docs/feature_walkthrough.md",
  "docs/api_reference_card.md",
  "docs/composite_block.md",
  "docs/my_new_pattern.md",   # <-- new
]
""", language="toml")
    st_space("v", 2)

    # ---- Step 5 ----
    st_write(bs.sub, "Step 5: Update `_pattern_library.md`", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The global index is auto-generated. Run `stx patterns reindex`
        in any project that has the catalog wired in, or use the
        helper script in the catalog repo.
    """)
    st_space("v", 1)

    show_code("""\
cd streamtex-patterns
uv run python scripts/reindex.py
git diff _pattern_library.md   # review the new row
""", language="bash")
    st_space("v", 2)

    # ---- Step 6 ----
    st_write(bs.sub, "Step 6: Test by dogfooding", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Before opening the PR, **use** the pattern in a real block.
        The friction of writing the consumer block is the best test
        for the pattern's clarity and ergonomics.
    """)
    st_space("v", 1)

    show_code("""\
# In a consumer project (e.g. ai4se6d or this manual)
stx patterns install --preset <preset>
# Then ask Claude:
#   "/stx-block:new bck_demo using my_new_pattern"
# Inspect the generated file. Iterate on the pattern markdown.
""", language="bash")
    st_space("v", 2)

    # ---- Step 7 ----
    st_write(bs.sub, "Step 7: Open a PR", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Push a branch on `streamtex-patterns` and open a PR. CI re-runs
        validation. Once merged, consumer projects pick up the new
        pattern via `stx patterns update`.
    """)
    st_space("v", 1)

    show_code("""\
git checkout -b add-my-new-pattern
git add core/my_new_pattern.md presets/docs.toml _pattern_library.md
git commit -m "feat(patterns): add my_new_pattern"
git push -u origin add-my-new-pattern
gh pr create --title "Add my_new_pattern" \\
    --body "Adds a new pattern in the docs scope."
""", language="bash")
    st_space("v", 2)

    show_details("""\
        **Promotion shortcut** — if you already drafted the pattern
        inside a consumer project (e.g. by editing the local copy
        after `stx patterns install`), you can push it back with
        `stx patterns promote <name>` instead of recreating it in the
        catalog repo by hand.
    """)
    st_space("v", 1)
