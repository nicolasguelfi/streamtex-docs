"""CLI template format — scaffolds packaged inside a pack."""

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
    """Document the CLI template layout and the scaffolding flow."""
    st_write((bs.heading, "CLI template format"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "A CLI template is a project scaffold packaged inside a pack at "
        "<pack>/cli_templates/<name>/. When a user runs stx project new "
        "--kit <pack>:<kit>, the kit's referenced template is copied into "
        "the new project directory, with placeholders (project name, pack "
        "list, DS reference) substituted at scaffold time.",
        tag=t.div,
    )
    st_space(20)

    # ---- Layout ----
    st_write((bs.sub, "Template directory layout"), toc_lvl="+1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Minimum viable template — same shape as a working project:",
        tag=t.div,
    )
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
my-pack/cli_templates/project-default/
├── pyproject.toml            # uv-compatible Python project
├── stx.toml                  # pack declarations + DS + kit
├── book.py                   # st_book(...) orchestration
├── blocks/
│   ├── __init__.py           # ProjectBlockRegistry(Path(...))
│   └── bck_welcome.py        # one starter block
├── custom/
│   ├── __init__.py
│   ├── styles.py             # project-specific Styles class
│   └── themes.py             # optional theme overrides
└── static/                   # optional static assets
""",
            language="text",
        )
    st_space(20)

    # ---- Placeholders ----
    st_write((bs.sub, "Placeholders substituted at scaffold time"), toc_lvl="+1", tag=t.div)
    st_space(10)
    term_definition_list(
        design_system=DS,
        items=[
            ("{{project_name}}",
             "The argument passed to stx project new <name>."),
            ("{{pack_declarations}}",
             "TOML [[packs]] blocks derived from --pack / --kit flags "
             "(and the implicit ./mypack unless --no-mypack)."),
            ("{{design_system_ref}}",
             "<pack>:<ds_name> declared by the chosen kit."),
            ("{{kit_ref}}",
             "<pack>:<kit_name> of the installed kit, or empty."),
            ("{{streamtex_constraint}}",
             "Version constraint pinned by the pack's streamtex_compat "
             "manifest field."),
        ],
    )
    st_space(20)

    # ---- Wiring in the kit ----
    st_write((bs.sub, "Wiring a CLI template to a kit"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(
            code="""
# my-pack/kits/project-default.toml

name = "project-default"
description = "Vanilla project scaffold with the core component kit."

[design_system]
ref = "default"

[components]
include = ["slide_heading", "callout", "card_grid", "manual_section"]

[cli_template]
ref = "project-default"        # → my-pack/cli_templates/project-default/
""",
            language="toml",
        )
    st_space(20)

    # ---- Authoring tips ----
    st_write((bs.sub, "Authoring tips"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="Keep templates small and opinionated",
        body=(
            "One starter block, one ruff config, one CHANGELOG stub. "
            "Users add scope with stx pack add and stx component new."
        ),
    )
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="Dependencies",
        body=(
            "The template's pyproject.toml lists streamtex[cli]>=… + the "
            "kit's pack as a dependency. Local packs are wired via "
            "[tool.uv.sources] when scaffolded with --mypack."
        ),
    )
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="stx.toml declarations",
        body=(
            "The template's stx.toml declares [[packs]] for the primary "
            "local pack and any external pack referenced by the kit. The "
            "scaffold step writes the right entries from --pack / --kit "
            "flags."
        ),
    )
    st_space(10)
    callout(
        design_system=DS,
        variant="success",
        title="Working pack from day one",
        body=(
            "Templates can ship _pack_manifest.toml placeholders for the "
            "local ./mypack/ so it is a working pack from day one."
        ),
    )
