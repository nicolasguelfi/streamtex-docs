"""Authoring a pack — layout, manifest, entry point, validation.

Source: streamtex/cli/pack_cmd.py + streamtex-design (canonical reference pack).
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
    """Walk through pack authoring from scaffold to entry-point registration."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Authoring a pack"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "A pack is just a Python package — same layout, same "
            "tooling — that registers itself under the "
            "`streamtex.packs` entry point. Four steps: scaffold, "
            "write the manifest, populate `components/` / "
            "`design_systems/` / `kits/`, register the entry point.",
        )
        st_space(15)

    # ---- Step 1: scaffold ----
    st_write((bs.sub, "Step 1 — Scaffold a local pack"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# Inside an existing project — scaffold ./mypack/
stx pack new mypack

# Or scaffold at an arbitrary location
stx pack new shared_pack --path /Users/me/shared/shared_pack

# Mark it primary if it's the project's capture target
stx pack set-primary mypack
""",
            language="bash",
        )
    st_space(15)

    # ---- Step 2: directory layout ----
    st_write((bs.sub, "Step 2 — Directory layout"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
mypack/
├── pyproject.toml                # Python package metadata + entry point
├── mypack/                       # importable package
│   ├── __init__.py
│   ├── _pack_manifest.toml       # pack identity + version + compat
│   ├── components/               # one .py file per component
│   ├── design_systems/           # one .py file per DS
│   ├── kits/                     # one .toml file per kit
│   ├── cli_templates/            # optional — project scaffolds
│   ├── project_blueprints/       # optional — AI-agent .md instructions
│   └── samples/                  # optional — copy-into-project blocks
└── README.md
""",
            language="text",
        )
    st_space(15)

    # ---- Step 3: manifest ----
    st_write((bs.sub, "Step 3 — Pack manifest"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "The manifest is the pack's identity. Format version is "
        "mouvant on the `0.x` track (Q16) — the validator accepts "
        "any `0.x.y` for now.",
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# mypack/mypack/_pack_manifest.toml

[manifest]
format = "0.1"

[pack]
name = "mypack"
version = "0.1.0"
author = "Your Name"
license = "MIT"
streamtex_compat = ">=0.7.0,<1.0"

[entrypoint]
module = "mypack"

# Optional — declare scopes (informational only)
[scopes]
core = "Universal primitives"
domain_x = "Domain-specific blocks"
""",
            language="toml",
        )
    st_space(15)

    # ---- Step 4: entry point ----
    st_write((bs.sub, "Step 4 — Register the entry point"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Discovery uses **Python entry points** (PEP 621). The pack "
        "must register its module under the `streamtex.packs` group "
        "in `pyproject.toml`:",
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# mypack/pyproject.toml

[project]
name = "mypack"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["streamtex>=0.7.0,<1.0"]

[project.entry-points."streamtex.packs"]
mypack = "mypack"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
""",
            language="toml",
        )
    st_space(15)

    st_write(
        bs.body,
        "The key `mypack = \"mypack\"` reads as: *the pack named "
        "`mypack` is exported at module `mypack`*. The discoverer "
        "imports the module and reads `_pack_manifest.toml` from "
        "the package root.",
    )
    st_space(15)

    # ---- Step 5: validate ----
    st_write((bs.sub, "Step 5 — Validate the pack"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# Validate this pack
stx pack validate mypack

# Validate all packs
stx pack validate

# Full project-wide gate
stx validate --strict
""",
            language="bash",
        )
    st_space(15)

    st_write(
        bs.body,
        "Pack-level issues use the `PV0xx` code family (see the "
        "validation block). The most common ones are `PV002` "
        "(missing entry point) and `PV003` (malformed manifest).",
    )
