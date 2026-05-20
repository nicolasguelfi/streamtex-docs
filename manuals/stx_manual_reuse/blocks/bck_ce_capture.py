"""CE capture flow — turn a recurring visual idiom into a captured component."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout
from streamtex_design.components.term_definition_list import term_definition_list


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """Walk through capturing a recurring visual idiom as a new component."""
    st_write((bs.heading, "CE capture flow"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "When a project's blocks repeat the same visual idiom — an info "
        "banner, a numbered list of milestones, a stat card — the right "
        "move is to capture it as a component in the project's primary "
        "local pack. The component then becomes addressable by name, "
        "reusable across blocks, and eligible for promotion later.",
        tag=t.div,
    )
    st_space(20)

    # ---- Step 1 ----
    st_write((bs.sub, "Step 1 — Spot the recurrence"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="Three signals warrant a capture",
        body=(
            "(a) the same structure appears in three or more blocks; "
            "(b) the structure has its own params worth naming; "
            "(c) the AI agent keeps regenerating slightly inconsistent "
            "variants. Run stx component list first — the idiom may "
            "already be covered by an installed pack."
        ),
    )
    st_space(20)

    # ---- Step 2 ----
    st_write((bs.sub, "Step 2 — Scaffold into the primary local pack"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# Scaffold into ./mypack/components/my_widget.py
stx component new my_widget --granularity composition

# Or into a named pack (must be local)
stx component new my_widget --pack mypack --granularity primitive
""",
            language="bash",
        )
    st_space(10)
    st_write(
        bs.body,
        "The scaffold writes a module skeleton with the docstring sections "
        "in place (Visual / Structure / Styling rules / INVARIANTS / "
        "PARAMS / INTERDITS / When to use / NOT to use / Bundles "
        "required), the __component_meta__ TypedDict stub, and a "
        "placeholder function body.",
        tag=t.div,
    )
    st_space(20)

    # ---- Step 3 ----
    st_write((bs.sub, "Step 3 — Fill the docstring contract"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="warn",
        title="The docstring is canonical",
        body=(
            "INVARIANTS describes what the component will never break — "
            "they protect the visual identity. PARAMS describes the "
            "public API surface — everything outside this list is "
            "INTERDITS (refused by the AI agent for extrapolation)."
        ),
    )
    st_space(15)
    st_write(bs.body, "Pick the right granularity tag:", tag=t.div)
    st_space(10)
    term_definition_list(
        design_system=DS,
        items=[
            ("primitive",
             "Atomic visual element (callout, cite, slide_heading)."),
            ("composition",
             "Multiple primitives + own layout (card_grid, "
             "comparison_table, term_definition_list)."),
            ("block",
             "Full block-level template (title_slide, stat_hero, "
             "evidence_insight)."),
        ],
    )
    st_space(20)

    # ---- Step 4 ----
    st_write((bs.sub, "Step 4 — Use the captured component from a block"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# blocks/bck_dashboard.py
from streamtex import *
from custom.styles import Styles as s
from mypack.components import my_widget

def build():
    my_widget(
        design_system=s.project.design_system,
        title="Throughput",
        body="142 jobs / day",
    )
""",
            language="python",
        )
    st_space(20)

    # ---- Step 5 ----
    st_write((bs.sub, "Step 5 — Validate"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# After every contract change
stx component validate my_widget

# Before commit / push
stx validate --strict
""",
            language="bash",
        )
    st_space(15)
    callout(
        design_system=DS,
        variant="success",
        title="Next step: promote",
        body=(
            "The captured component now lives with the project's git "
            "history. When it proves reusable across projects, the next "
            "step is to promote it to a shared pack — see the promotion block."
        ),
    )
