"""CE capture flow — turn a recurring visual idiom into a captured component.

Source: streamtex/cli/component_cmd.py new_cmd + streamtex-claude CE skills.
"""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
    )


bs = BlockStyles


def build():
    """Walk through capturing a recurring visual idiom as a new component."""
    with st_block(s.center_txt):
        st_write(("CE capture flow", bs.heading))
        st_space(15)
        st_write(
            "When a project's blocks repeat the same visual idiom — "
            "an info banner, a numbered list of milestones, a stat "
            "card — the right move is to **capture** it as a "
            "component in the project's primary local pack. The "
            "component then becomes addressable by name, reusable "
            "across blocks, and eligible for promotion later.",
            bs.body,
        )
        st_space(15)

    # ---- Step 1: spot ----
    st_write(("Step 1 — Spot the recurrence", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Three signals that warrant a capture: (a) the same "
        "structure appears in three or more blocks; (b) the "
        "structure has its own params worth naming; (c) the AI "
        "agent keeps regenerating slightly inconsistent variants. "
        "Run `stx component list` first — the idiom may already be "
        "covered by an installed pack.",
        bs.body,
    )
    st_space(15)

    # ---- Step 2: scaffold ----
    st_write(("Step 2 — Scaffold into the primary local pack", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# Scaffold into ./mypack/components/my_widget.py
stx component new my_widget --granularity composition

# Or into a named pack (must be local)
stx component new my_widget --pack mypack --granularity primitive
""",
            language="bash",
        )
    st_space(10)
    st_write(
        "The scaffold writes a module skeleton with the docstring "
        "sections in place (Visual / Structure / Styling rules / "
        "INVARIANTS / PARAMS / INTERDITS / When to use / NOT to use "
        "/ Bundles required), the `__component_meta__` TypedDict "
        "stub, and a placeholder function body.",
        bs.body,
    )
    st_space(15)

    # ---- Step 3: fill the contract ----
    st_write(("Step 3 — Fill the docstring contract", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "The docstring is canonical. Two rules to internalise:\n\n"
        "- **`INVARIANTS`** describes what the component will never "
        "break — they protect the visual identity.\n"
        "- **`PARAMS`** describes the public API surface — "
        "everything outside this list is `INTERDITS` (refused by "
        "the AI agent for extrapolation).\n\n"
        "Pick the right granularity tag:",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        for tag, desc in [
            ("primitive",
             "Atomic visual element (callout, cite, slide_heading)."),
            ("composition",
             "Multiple primitives + own layout (card_grid, "
             "comparison_table, term_definition_list)."),
            ("block",
             "Full block-level template (title_slide, stat_hero, "
             "evidence_insight)."),
        ]:
            with g.cell():
                st_write(tag, bs.body + s.bold)
            with g.cell():
                st_write(desc, bs.body)
    st_space(15)

    # ---- Step 4: use it ----
    st_write(("Step 4 — Use the captured component from a block", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
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
    st_space(15)

    # ---- Step 5: validate ----
    st_write(("Step 5 — Validate", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# After every contract change
stx component validate my_widget

# Before commit / push
stx validate --strict
""",
            language="bash",
        )
    st_space(15)

    st_write(
        "The captured component now lives with the project's git "
        "history. When it proves reusable across projects, the next "
        "step is to **promote** it to a shared pack — see the "
        "promotion block.",
        bs.body,
    )
