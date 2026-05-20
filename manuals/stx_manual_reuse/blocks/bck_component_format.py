"""Anatomy of a Python component — module shape + docstring contract."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


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


def callout(*, design_system, title: str = "", body: str = "", variant: str = "info") -> None:
    """Render a callout box. `variant` ∈ {info, warn, error, success}."""
    container = get_bundle_attr(design_system.callouts, variant, "callout")
    title_style = design_system.callouts.title
    body_style = design_system.callouts.body
    with st_block(container):
        if title:
            st_write(title_style, title)
            st_space("v", 0.5)
        if body:
            st_write(body_style, body)
'''


def build():
    """Detail the anatomy of a Python component."""
    st_write((bs.heading, "Anatomy of a component"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "A component is a Python module exposing a public kwargs-only "
        "function + a structured docstring + a __component_meta__ "
        "TypedDict. The docstring is canonical: it documents Visual, "
        "Structure, Styling rules, Extrapolation rules (INVARIANTS / "
        "PARAMS / INTERDITS), When to use, When NOT to use, and Design "
        "system bundles required.",
        tag=t.div,
    )
    st_space(20)

    st_write((bs.sub, "Example: streamtex_design.components.callout"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(code=EXAMPLE_COMPONENT, language="python")
    st_space(20)

    st_write((bs.sub, "Why a Python module?"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="success",
        title="Real, importable Python — diffable, testable, type-checked",
        body=(
            "A block can do from streamtex_design.components import callout "
            "and call it directly. git diff works on it. Pytest tests it. "
            "Static analysis (basedpyright, ruff) covers it. There is no "
            "separate scan-time parser."
        ),
    )
    st_space(15)
    callout(
        design_system=DS,
        variant="info",
        title="The docstring carries the extrapolation contract",
        body=(
            "INVARIANTS, PARAMS, INTERDITS are kept as natural-language "
            "rules inside the docstring so the AI agent that consumes the "
            "docstring still gets the extrapolation contract."
        ),
    )
