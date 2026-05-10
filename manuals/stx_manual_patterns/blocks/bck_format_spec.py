"""Format A2 specification — frontmatter + structured sections.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Format spec page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    keyword = s.bold + s.project.colors.primary_violet
    accent = s.bold + s.project.colors.accent_teal


bs = BlockStyles


def build():
    """Document the Format A2 spec a pattern file must follow."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Format Spec — A2",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- Frontmatter ----
    st_write(bs.sub, "YAML Frontmatter", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Every pattern file opens with a YAML frontmatter block declaring
        its identity and metadata. This is the only machine-parsed part
        of the file — the rest is human-readable markdown.
    """)
    st_space("v", 1)

    show_code("""\
---
name: manual_section
type: pattern
description: Documentation section — heading + sub + explanation + code snippet + live demo
tags: [docs, manual, demo, code]
extrapolable: true
since: 2026-05-10
---""", language="yaml")
    st_space("v", 1)

    show_details("""\
        **Required keys**:
        - `name` — unique slug, used by `stx patterns install --pattern <name>`.
        - `type` — always `pattern` for now (reserved for future
          discriminations like `blueprint`, `recipe`).
        - `description` — one line shown in `_pattern_library.md`.
        - `tags` — flat list, used for search and filtering.
        - `extrapolable` — true if Claude is allowed to adapt the
          skeleton; false for "use as-is" templates.
        - `since` — ISO date the pattern entered the catalog.
    """)
    st_space("v", 2)

    # ---- Required sections ----
    st_write(bs.sub, "Required markdown sections", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        After the frontmatter, the markdown body must contain a fixed
        sequence of H2 sections. CI validates their presence on every
        PR (see `manifest.toml [ci] required_sections`).
    """)
    st_space("v", 1)

    show_code("""\
# <Pattern name in Title Case>

<one-paragraph teaser>

## Visual            # ASCII mockup or short description of the rendered output

## Structure        # logical grammar — what parts compose the pattern

## Styling rules    # exact reproducibility table (Element / Property / Value)

## Code skeleton    # concrete StreamTeX starting point (Python)

## Extrapolation rules
### INVARIANTS (never change)
### PARAMS (adjustable)
### INTERDITS (forbidden)

## When to use      # short bullet list

## When NOT to use  # short bullet list

## Examples         # optional — paths to real consumer blocks

## Related patterns # optional — cross-references""", language="markdown")
    st_space("v", 2)

    # ---- A minimal example ----
    st_write(bs.sub, "Minimal valid pattern", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Here is the smallest pattern that passes CI validation. Real
        patterns flesh out each section, but this is the floor.
    """)
    st_space("v", 1)

    show_code("""\
---
name: hello_box
type: pattern
description: A trivial framed box demonstrating the format A2
tags: [demo, atom]
extrapolable: true
since: 2026-05-10
---

# Hello Box

A one-line, framed message.

## Visual
A border around a single line of text.

## Structure
- One `st_block` with a `bs.box` style.
- One `st_write(bs.body, "...")` inside.

## Styling rules
| Element | Property | Value |
|---|---|---|
| box | composition | `s.container.borders.solid_border + small_padding` |
| body | size | `s.large` |

## Code skeleton
```python
class BlockStyles:
    box = s.container.borders.solid_border + s.container.paddings.small_padding
    body = s.large
bs = BlockStyles

def build():
    with st_block(bs.box):
        st_write(bs.body, "Hello!")
```

## Extrapolation rules
### INVARIANTS
- One block, one line.
### PARAMS
- The text content.
### INTERDITS
- No nested containers.

## When to use
- Throwaway examples.

## When NOT to use
- Production content (use `callout`).""", language="markdown")
    st_space("v", 2)

    # ---- Why "A2" ----
    st_write(bs.sub, "Why this is called A2", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        "A2" is the second iteration of the pattern format
        (`spec_version = "A2"` in `manifest.toml`). A1 was the
        prototype used internally during the catalog bootstrap; A2 is
        the first version with stable required sections and CI
        enforcement.

        Future revisions (A3, B1, ...) will require a manifest bump
        and a migration window for in-flight patterns.
    """)
    st_space("v", 1)
