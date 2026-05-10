"""Patterns vs Blueprints — where the frontier sits.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Frontier page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )
    head_cell = s.bold + s.project.colors.accent_teal


bs = BlockStyles


def build():
    """Define the frontier between patterns and blueprints."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Patterns vs Blueprints",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- Definition gap ----
    st_write(bs.sub, "Two kinds of reusable artifacts", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX projects reuse content at two levels:

        - **Patterns** — small visual primitives (a callout, a stat
          hero, a manual section). One markdown file, one
          recipe. Lives in `streamtex-patterns/`.
        - **Blueprints** — entire project skeletons (a presentation
          template, a manual template, a course template). A whole
          directory tree with `book.py`, `blocks/`, `custom/`,
          configuration. Lives in `streamtex-docs/templates/` or in a
          dedicated blueprint repo.

        They serve different needs and live in different places.
    """)
    st_space("v", 2)

    # ---- Comparison ----
    st_write(bs.sub, "Side-by-side comparison", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The table below summarises the practical differences. Use it
        to decide where a new piece of reusable content belongs.
    """)
    st_space("v", 1)

    with st_grid(cols="2fr 3fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(bs.body, (s.bold, "Aspect"))
        with g.cell():
            st_write(bs.body, (bs.head_cell, "Pattern"))
        with g.cell():
            st_write(bs.body, (bs.head_cell, "Blueprint"))

        with g.cell():
            st_write(bs.body, (s.bold, "Granularity"))
        with g.cell():
            st_write(bs.body, "One visual primitive (atom or molecule).")
        with g.cell():
            st_write(bs.body, "Entire project skeleton.")

        with g.cell():
            st_write(bs.body, (s.bold, "Format"))
        with g.cell():
            st_write(bs.body, "Single markdown file (Format A2).")
        with g.cell():
            st_write(bs.body, "Directory tree with code, "
                              "config, assets.")

        with g.cell():
            st_write(bs.body, (s.bold, "Consumer"))
        with g.cell():
            st_write(bs.body, "Claude Code, at block-generation time.")
        with g.cell():
            st_write(bs.body, "`stx project init`, at project-creation "
                              "time.")

        with g.cell():
            st_write(bs.body, (s.bold, "Lifetime"))
        with g.cell():
            st_write(bs.body, "Lives forever in the catalog; updated "
                              "via `stx patterns update`.")
        with g.cell():
            st_write(bs.body, "Spawned once into a project; the project "
                              "evolves independently.")

        with g.cell():
            st_write(bs.body, (s.bold, "Drift handling"))
        with g.cell():
            st_write(bs.body, "Drift detection per pattern; explicit "
                              "promote-back path.")
        with g.cell():
            st_write(bs.body, "No drift detection — once spawned, "
                              "you own it.")

        with g.cell():
            st_write(bs.body, (s.bold, "Composition"))
        with g.cell():
            st_write(bs.body, "Patterns combine inside one block "
                              "(e.g. `evidence_insight` uses "
                              "`stat_hero` + `takeaways`).")
        with g.cell():
            st_write(bs.body, "A blueprint may *embed* patterns by "
                              "calling `stx patterns install --preset` "
                              "in its bootstrap.")
    st_space("v", 2)

    # ---- Decision rule ----
    st_write(bs.sub, "When to use which", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The simple decision rule:

        - You want to reuse a **rendered shape** inside many blocks
          (across many projects) → write a **pattern**.
        - You want to spawn a **new project of a known type**
          (e.g. "a 60-slide course on X") → write or use a
          **blueprint**.

        A blueprint that ships with patterns pre-installed is fine
        — that's the **happy path** for new courses, manuals, and
        presentations.
    """)
    st_space("v", 1)

    show_code("""\
# A blueprint's bootstrap script can pre-install a pattern preset
stx project init --template course-presentation my-course
cd my-course
stx patterns install --preset slides   # blueprint-recommended preset
""", language="bash")
    st_space("v", 2)

    # ---- Common mistake ----
    st_write(bs.sub, "Common mistake — the over-grown pattern",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        A frequent anti-pattern is to grow a pattern until it
        prescribes the **whole page** (header, footer, navigation,
        background, sidebar). That's not a pattern any more — it's a
        page template, which belongs to a blueprint.

        **Rule of thumb**: if a pattern's `Code skeleton` is longer
        than ~80 lines, or it touches `book.py` or `custom/`, split
        it into multiple patterns or move the orchestration into a
        blueprint.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Watch the boundary")
        st_space("v", 0.5)
        st_write(bs.body,
                 "Blueprints orchestrate; patterns render. If your "
                 "pattern starts orchestrating, that's the signal it "
                 "should become a blueprint instead.")
    st_space("v", 2)

    show_details("""\
        **Future direction** — the catalog will likely grow a
        `recipes/` scope for short multi-pattern combos that fall
        between a single pattern and a full blueprint (e.g. "a
        section header + 3 cards + a takeaway"). Until then, those
        live as inline guidance in `_pattern_library.md`.
    """)
    st_space("v", 1)
