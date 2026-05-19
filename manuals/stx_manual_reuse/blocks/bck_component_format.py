"""Anatomy of a Python component (PLAN §4.1).

Source: adapted from bck_format_spec.py — replaces the legacy A2 markdown
spec with the Python module + docstring contract.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    section = s.bold + s.large


bs = BlockStyles

EXAMPLE_COMPONENT = '''
"""Boxed inline notice — primitive component.

## Visual

A bordered box with an icon-coloured title row and a body. Four kinds:
info, warn, error, success. Inline width by default.

## Structure

- 1 title row (kind icon + bolded title)
- 1 body row (paragraph)
- 1 outer container with the kind's border colour

## Styling rules

| Element | Bundle attribute       |
|---------|------------------------|
| Title   | callouts.title         |
| Body    | callouts.body          |
| Border  | callouts.<kind>        |

## Extrapolation rules

### INVARIANTS

- Exactly one title and one body.
- Border colour matches the kind.

### PARAMS

- kind: info | warn | error | success
- title: str
- body: str

### INTERDITS

- Multiple titles or bodies inside a single callout.
- Custom kind values (use a new component instead).

## When to use

- Highlight a side-note in a block.
- Flag a warning, error, or success outcome inline.

## When NOT to use

- For multi-paragraph editorial content (use a manual_section).
- For a hero stat (use stat_hero).

## Design system bundles required

callouts.info, callouts.warn, callouts.error, callouts.success,
callouts.title, callouts.body, inline_emphasis.strong, body.paragraph
"""

from streamtex import st_block, st_write
from streamtex.core.discovery import get_bundle_attr
from streamtex.core.contracts import ComponentMeta

__component_meta__: ComponentMeta = {
    "name": "callout",
    "description": "Boxed inline notice with a kind.",
    "tags": ["primitive", "callout"],
    "extrapolable": True,
    "since": "2026-05-19",
    "bundles_required": [
        "callouts.info", "callouts.warn", "callouts.error",
        "callouts.success", "callouts.title", "callouts.body",
        "inline_emphasis.strong", "body.paragraph",
    ],
    "granularity": "primitive",
}


def callout(*, kind: str, title: str, body: str) -> None:
    border = get_bundle_attr(__ds__.callouts, kind, "callout")
    with st_block(border):
        st_write((title, __ds__.callouts.title))
        st_write(body, __ds__.body.paragraph)
'''


def build():
    """Detail the anatomy of a Python component."""
    with st_block(s.center_txt):
        st_write(("Anatomy of a component", bs.heading))
        st_space(15)
        st_write(
            "A component is a Python module exposing a public kwargs-only "
            "function + a structured docstring + a __component_meta__ "
            "TypedDict. The docstring is canonical: it documents Visual, "
            "Structure, Styling rules, Extrapolation rules (INVARIANTS / "
            "PARAMS / INTERDITS), When to use, When NOT to use, and Design "
            "system bundles required.",
            bs.body,
        )
        st_space(15)
        st_write(("Example: streamtex_design.components.callout", bs.section))
        with st_block(bs.code):
            st_code(EXAMPLE_COMPONENT, language="python")

        st_space(15)
        st_write(("Why a Python module?", bs.section))
        st_write(
            "The component is real, importable Python — so a block can do "
            "from streamtex_design.components import callout and call it "
            "directly. git diff works on it. Pytest tests it. Static "
            "analysis (basedpyright, ruff) covers it. There is no separate "
            "scan-time parser.",
            bs.body,
        )
        st_write(
            "INVARIANTS, PARAMS, INTERDITS are kept as natural-language "
            "rules inside the docstring (decision D9 — the best idea from "
            "the legacy A2 spec) so the AI agent that consumes the docstring "
            "still gets the extrapolation contract.",
            bs.body,
        )
