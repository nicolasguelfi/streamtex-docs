"""Authoring a component — scaffold, docstring contract, validate.

Source: streamtex/cli/component_cmd.py + streamtex-claude
shared/skills/reuse-architecture.md + streamtex-design components.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    section = s.bold + s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
    )


bs = BlockStyles


DOCSTRING_TEMPLATE = '''
"""<one-line description> — <granularity> component.

## Visual

<What it looks like: 1-3 sentences describing the rendered output.>

## Structure

<Bulleted breakdown of the visual structure: how many rows / columns,
which Streamlit primitives are used, which design-system bundles
are pulled in.>

## Styling rules

| Element | Bundle attribute |
|---------|------------------|
| <part>  | <pack.bundle>    |

## Extrapolation rules

### INVARIANTS

- <Rules that must always hold (otherwise it stops being this component).>

### PARAMS

- <param_name>: <type — semantics>

### INTERDITS

- <Things the component refuses to do, and why.>

## When to use

- <Concrete situation where this component is the right answer.>

## When NOT to use

- <Adjacent need that should pick a different component.>

## Design system bundles required

<comma-separated list of bundle attribute paths the component reads.>
"""
'''


META_TEMPLATE = '''
__component_meta__: ComponentMeta = {
    "name": "my_widget",
    "description": "<one-line description>",
    "tags": ["primitive", "callout"],
    "extrapolable": True,
    "since": "2026-05-19",
    "bundles_required": ["callouts.info", "callouts.title"],
    "granularity": "primitive",
}
'''


def build():
    """Walk through component authoring from scaffold to validate."""
    with st_block(s.center_txt):
        st_write(("Authoring a component", bs.heading))
        st_space(15)
        st_write(
            "A component is a Python module shipped inside a pack. "
            "Three steps: scaffold, fill the docstring contract + the "
            "function body, validate.",
            bs.body,
        )
        st_space(15)

    # ---- Step 1: scaffold ----
    st_write(("Step 1 — Scaffold", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Use `stx component new` to scaffold a component into the "
        "primary local pack (or any pack with `--pack`):",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Default destination — primary local pack (./mypack/components/)
stx component new my_widget --granularity composition

# Explicit pack
stx component new my_widget --pack mypack --granularity primitive

# Three granularities: primitive | composition | block
""",
            language="bash",
        )
    st_space(15)

    # ---- Step 2: docstring contract ----
    st_write(("Step 2 — Docstring contract", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "The module docstring is the canonical specification for the "
        "AI agent. Nine sections, in order:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(DOCSTRING_TEMPLATE, language="python")
    st_space(15)

    st_write(
        "`INVARIANTS` are rules the component will never violate. "
        "`PARAMS` are the public API surface. `INTERDITS` are uses the "
        "component refuses. The AI agent reads these to decide whether "
        "to use the component as-is, extrapolate within `PARAMS`, or "
        "scaffold a new component instead.",
        bs.body,
    )
    st_space(15)

    # ---- Step 3: __component_meta__ + function ----
    st_write(("Step 3 — Meta + function", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Below the docstring, add the `__component_meta__` TypedDict "
        "(consumed by `stx component list` / `find` / `show`) and a "
        "kwargs-only public function:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(META_TEMPLATE, language="python")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
def my_widget(*, design_system, title: str = "", body: str = "") -> None:
    \"\"\"Render the widget. All params are kwargs-only.\"\"\"
    with st_block(design_system.callouts.info):
        if title:
            st_write(design_system.callouts.title, title)
        if body:
            st_write(design_system.callouts.body, body)
""",
            language="python",
        )
    st_space(15)

    # ---- Step 4: validate ----
    st_write(("Step 4 — Validate", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Validation is incremental — run it after the scaffold and "
        "again whenever the contract changes:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Validate this component only
stx component validate my_widget

# Validate every component in every installed pack
stx component validate

# CI-grade gate (errors and warnings)
stx validate --strict
""",
            language="bash",
        )
    st_space(15)

    st_write(
        "The validator emits `CV001`-`CV011` for component-level "
        "issues (missing meta, malformed docstring, missing bundle, "
        "etc.) — see the validation block for the full code table.",
        bs.body,
    )
