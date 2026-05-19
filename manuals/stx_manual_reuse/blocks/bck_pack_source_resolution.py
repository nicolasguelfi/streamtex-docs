"""Pack source resolution — discovery, lifecycle states, manifest format."""

from streamtex import *
from streamtex.enums import Tags as t
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
    cell_head = s.bold + s.large


bs = BlockStyles


def build():
    """How packs are discovered, declared, and tracked across the 3 locations."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Pack discovery & lifecycle"), tag=t.div, toc_lvl="1")
        st_space(15)

    # ---- 1) Three locations a pack can live in ----
    st_write((bs.sub, "1 — Where packs live"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "A pack is a Python package shipping `components/`, "
        "`design_systems/`, and `kits/`. It can live in three places, "
        "all declared in the project's `stx.toml`:",
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            code="""
# stx.toml — three pack locations

[[packs]]
type = "local"
name = "mypack"
path = "./mypack"            # primary local pack (project sub-folder)
primary = true

[[packs]]
type = "local"
name = "shared_pack"
path = "/Users/me/shared"    # local pack on disk (any path)

[[packs]]
type = "git"
name = "streamtex-design"
ref = "github.com/nicolasguelfi/streamtex-design"
rev = "v0.2.0"               # tag, branch, or commit SHA

[[packs]]
type = "pypi"
name = "streamtex-academic"
constraint = ">=1.0,<2.0"
""",
            language="toml",
        )
    st_space(15)

    # ---- 2) Discovery mechanism ----
    st_write((bs.sub, "2 — How `stx` finds the packs"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "Discovery uses **Python entry points** (PEP 621). Every "
        "installed pack registers its module under the "
        "`streamtex.packs` entry point group. The discoverer reads "
        "`stx.toml` for declarations, then matches them against "
        "installed entry points.",
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            code="""
# Pack's pyproject.toml
[project.entry-points."streamtex.packs"]
streamtex-design = "streamtex_design"

# Runtime discovery
from streamtex.core.discovery import discover_packs
packs = discover_packs()
for p in packs:
    print(p.name, p.state, p.entry_point_module)
""",
            language="python",
        )
    st_space(15)

    # ---- 3) Five lifecycle states ----
    st_write((bs.sub, "3 — Five lifecycle states"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "Every discovered pack has a `state` reflecting its health. "
        "The validator emits a `PR0xx` code when the state is anything "
        "other than `nominal` or `indirect`.",
    )
    st_space(10)

    with st_grid(cols="1fr 1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.cell_head, "State"))
        with g.cell():
            st_write((bs.cell_head, "Code"))
        with g.cell():
            st_write((bs.cell_head, "Meaning"))

        with g.cell():
            st_write(bs.body, "nominal")
        with g.cell():
            st_write(bs.body, "—")
        with g.cell():
            st_write(bs.body, "declared in stx.toml, installed, manifest OK")

        with g.cell():
            st_write(bs.body, "drift_install")
        with g.cell():
            st_write(bs.body, "PR002")
        with g.cell():
            st_write(bs.body, "declared but no matching entry point in the env")

        with g.cell():
            st_write(bs.body, "indirect")
        with g.cell():
            st_write(bs.body, "—")
        with g.cell():
            st_write(bs.body, "entry point present but not declared in stx.toml")

        with g.cell():
            st_write(bs.body, "manifest_broken")
        with g.cell():
            st_write(bs.body, "PR003")
        with g.cell():
            st_write(bs.body, "installed but `_pack_manifest.toml` fails to load")

        with g.cell():
            st_write(bs.body, "collision")
        with g.cell():
            st_write(bs.body, "PR004")
        with g.cell():
            st_write(bs.body, "same pack name declared by 2+ packages")
    st_space(15)

    st_write(
        bs.body,
        "Run `stx pack list` to see each pack's state, or "
        "`stx pack info <name>` for full manifest details. "
        "`stx validate --strict` fails the build on any PR code.",
    )
    st_space(15)

    # ---- 4) Manifest format ----
    st_write((bs.sub, "4 — Pack manifest"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "Every pack ships a `_pack_manifest.toml` at its package root. "
        "The format version is mouvant on the `0.x` track (Q16) — the "
        "validator accepts any `0.x.y`.",
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            code="""
# streamtex_design/_pack_manifest.toml

[manifest]
format = "0.1"

[pack]
name = "streamtex-design"
version = "0.2.0"
author = "Nicolas Guelfi"
license = "MIT"
streamtex_compat = ">=0.7.0,<1.0"

[entrypoint]
module = "streamtex_design"
""",
            language="toml",
        )
    st_space(15)

    # ---- 5) Component granularity tags ----
    st_write((bs.sub, "5 — Component granularity"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "Every component declares a `granularity` in its "
        "`__component_meta__` TypedDict. It is **a tag, not a "
        "constraint** — the resolver doesn't filter on it, but `stx "
        "component list --granularity <tier>` lets users browse by "
        "tier.",
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.cell_head, "primitive"))
        with g.cell():
            st_write(
                bs.body,
                "Atomic visual element (callout, cite, inline_emphasis, "
                "slide_heading).",
            )
        with g.cell():
            st_write((bs.cell_head, "composition"))
        with g.cell():
            st_write(
                bs.body,
                "Multiple primitives + own layout "
                "(card_grid, comparison_table, takeaways, "
                "term_definition_list, manual_section, …).",
            )
        with g.cell():
            st_write((bs.cell_head, "block"))
        with g.cell():
            st_write(
                bs.body,
                "Full block-level template (title_slide, stat_hero, "
                "evidence_insight, exercise_flow, narrative_transition, "
                "feature_walkthrough).",
            )
    st_space(15)

    # ---- 6) `stx pack sync` and dev links ----
    st_write((bs.sub, "6 — Keeping packs fresh"), toc_lvl="+1")
    st_space(10)

    st_write(
        bs.body,
        "Pack resolution delegates to **uv**. `stx pack sync` runs "
        "`uv sync` after re-reading `stx.toml`, so updates flow through "
        "the same dependency lockfile as the rest of the project.",
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            code="""
# Update a git pack to a new revision (encode rev in the ref)
stx pack add git:https://github.com/streamtex/streamtex-design@v0.2.0
stx pack sync                                # uv sync applies it

# Iterate on a pack locally (editable install)
stx pack add /Users/me/dev/my-fork --dev
# → adds [tool.uv.sources].my-fork = { path = "...", editable = true }

# Inspect what is installed vs. what is declared
stx pack list --trace                        # shows the discovery trace
""",
            language="bash",
        )
