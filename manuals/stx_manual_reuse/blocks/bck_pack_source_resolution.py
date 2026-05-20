"""Pack source resolution — discovery, lifecycle states, manifest format."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.comparison_table import comparison_table
from streamtex_design.components.term_definition_list import term_definition_list


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code_box = (
        s.project.containers.code_box
        if hasattr(s.project.containers, "code_box")
        else s.container.paddings.small_padding + s.container.borders.solid_border
    )


bs = BlockStyles


def build():
    """How packs are discovered, declared, and tracked across the 3 locations."""
    st_write((bs.heading, "Pack discovery & lifecycle"), tag=t.div, toc_lvl="1")
    st_space(15)

    # ---- 1) Three locations a pack can live in ----
    st_write((bs.sub, "1 — Where packs live"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "A pack is a Python package shipping components/, design_systems/, "
        "and kits/. It can live in three places, all declared in the "
        "project's stx.toml:",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
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
    st_space(20)

    # ---- 2) Discovery mechanism ----
    st_write((bs.sub, "2 — How stx finds the packs"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Discovery uses Python entry points (PEP 621). Every installed pack "
        "registers its module under the streamtex.packs entry point group. "
        "The discoverer reads stx.toml for declarations, then matches them "
        "against installed entry points.",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
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
    st_space(20)

    # ---- 3) Five lifecycle states ----
    st_write((bs.sub, "3 — Five lifecycle states"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Every discovered pack has a state reflecting its health. The "
        "validator emits a PR0xx code when the state is anything other "
        "than nominal or indirect.",
        tag=t.div,
    )
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["State", "Code", "Meaning"],
        rows=[
            ("nominal", "—",
             "Declared in stx.toml, installed, manifest OK."),
            ("drift_install", "PR002",
             "Declared but no matching entry point in the env."),
            ("indirect", "—",
             "Entry point present but not declared in stx.toml."),
            ("manifest_broken", "PR003",
             "Installed but _pack_manifest.toml fails to load."),
            ("collision", "PR004",
             "Same pack name declared by 2+ packages."),
        ],
    )
    st_space(15)
    st_write(
        bs.body,
        "Run stx pack list to see each pack's state, or stx pack info <name> "
        "for full manifest details. stx validate --strict fails the build "
        "on any PR code.",
        tag=t.div,
    )
    st_space(20)

    # ---- 4) Manifest format ----
    st_write((bs.sub, "4 — Pack manifest"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Every pack ships a _pack_manifest.toml at its package root. The "
        "format version is movable on the 0.x track — the validator "
        "accepts any 0.x.y.",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
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
    st_space(20)

    # ---- 5) Component granularity tags ----
    st_write((bs.sub, "5 — Component granularity"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Every component declares a granularity in its __component_meta__ "
        "TypedDict. It is a tag, not a constraint — the resolver doesn't "
        "filter on it, but stx component list --granularity <tier> lets "
        "users browse by tier.",
        tag=t.div,
    )
    st_space(10)
    term_definition_list(
        design_system=DS,
        items=[
            ("primitive",
             "Atomic visual element (callout, cite, inline_emphasis, "
             "slide_heading)."),
            ("composition",
             "Multiple primitives + own layout (card_grid, comparison_table, "
             "takeaways, term_definition_list, manual_section, …)."),
            ("block",
             "Full block-level template (title_slide, stat_hero, "
             "evidence_insight, exercise_flow, narrative_transition, "
             "feature_walkthrough)."),
        ],
    )
    st_space(20)

    # ---- 6) stx pack sync and dev links ----
    st_write((bs.sub, "6 — Keeping packs fresh"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Pack resolution delegates to uv. stx pack sync runs uv sync after "
        "re-reading stx.toml, so updates flow through the same dependency "
        "lockfile as the rest of the project.",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
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
