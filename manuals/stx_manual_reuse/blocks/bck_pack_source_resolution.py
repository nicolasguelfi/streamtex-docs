"""Pack source resolution — discovery, lifecycle states, manifest format.

Port of the legacy `bck_scan_rule` block from `stx_manual_patterns`,
updated for the 0.7.x reuse architecture (packs / components / DS / kits).
"""

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
        st_write(("Pack discovery & lifecycle", bs.heading), tag=t.div, toc_lvl="1")
        st_space(15)

    # ---- 1) Three locations a pack can live in ----
    st_write(("1 — Where packs live", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "A pack is a Python package shipping `components/`, "
        "`design_systems/`, and `kits/`. It can live in three places, "
        "all declared in the project's `stx.toml`:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_write(("2 — How `stx` finds the packs", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "Discovery uses **Python entry points** (PEP 621). Every "
        "installed pack registers its module under the "
        "`streamtex.packs` entry point group. The discoverer reads "
        "`stx.toml` for declarations, then matches them against "
        "installed entry points.",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_write(("3 — Five lifecycle states", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "Every discovered pack has a `state` reflecting its health. "
        "The validator emits a `PR0xx` code when the state is anything "
        "other than `nominal` or `indirect`.",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("State", bs.cell_head))
        with g.cell():
            st_write(("Code", bs.cell_head))
        with g.cell():
            st_write(("Meaning", bs.cell_head))

        with g.cell():
            st_write("nominal", bs.body)
        with g.cell():
            st_write("—", bs.body)
        with g.cell():
            st_write("declared in stx.toml, installed, manifest OK", bs.body)

        with g.cell():
            st_write("drift_install", bs.body)
        with g.cell():
            st_write("PR002", bs.body)
        with g.cell():
            st_write("declared but no matching entry point in the env", bs.body)

        with g.cell():
            st_write("indirect", bs.body)
        with g.cell():
            st_write("—", bs.body)
        with g.cell():
            st_write("entry point present but not declared in stx.toml", bs.body)

        with g.cell():
            st_write("manifest_broken", bs.body)
        with g.cell():
            st_write("PR003", bs.body)
        with g.cell():
            st_write("installed but `_pack_manifest.toml` fails to load", bs.body)

        with g.cell():
            st_write("collision", bs.body)
        with g.cell():
            st_write("PR004", bs.body)
        with g.cell():
            st_write("same pack name declared by 2+ packages", bs.body)
    st_space(15)

    st_write(
        "Run `stx pack list` to see each pack's state, or "
        "`stx pack info <name>` for full manifest details. "
        "`stx validate --strict` fails the build on any PR code.",
        bs.body,
    )
    st_space(15)

    # ---- 4) Manifest format ----
    st_write(("4 — Pack manifest", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "Every pack ships a `_pack_manifest.toml` at its package root. "
        "The format version is mouvant on the `0.x` track (Q16) — the "
        "validator accepts any `0.x.y`.",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
    st_write(("5 — Component granularity", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "Every component declares a `granularity` in its "
        "`__component_meta__` TypedDict. It is **a tag, not a "
        "constraint** — the resolver doesn't filter on it, but `stx "
        "component list --granularity <tier>` lets users browse by "
        "tier.",
        bs.body,
    )
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("primitive", bs.cell_head))
        with g.cell():
            st_write(
                "Atomic visual element (callout, cite, inline_emphasis, "
                "slide_heading).",
                bs.body,
            )
        with g.cell():
            st_write(("composition", bs.cell_head))
        with g.cell():
            st_write(
                "Multiple primitives + own layout "
                "(card_grid, comparison_table, takeaways, "
                "term_definition_list, manual_section, …).",
                bs.body,
            )
        with g.cell():
            st_write(("block", bs.cell_head))
        with g.cell():
            st_write(
                "Full block-level template (title_slide, stat_hero, "
                "evidence_insight, exercise_flow, narrative_transition, "
                "feature_walkthrough).",
                bs.body,
            )
    st_space(15)

    # ---- 6) `stx pack sync` and dev links ----
    st_write(("6 — Keeping packs fresh", bs.sub), toc_lvl="+1")
    st_space(10)

    st_write(
        "Where the legacy system had `stx patterns update` driven by "
        "per-pattern SHA bookkeeping, the new system delegates to **uv** "
        "for resolution. `stx pack sync` runs `uv sync` after re-reading "
        "`stx.toml`, so updates flow through the same dependency lockfile.",
        bs.body,
    )
    st_space(10)

    with st_block(bs.cell):
        st_code(
            """
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
