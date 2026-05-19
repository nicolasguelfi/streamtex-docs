"""CLI template format — scaffolds packaged inside a pack.

Source: streamtex-docs/templates/template_project/ (canonical example).
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
    cell_head = s.bold + s.large


bs = BlockStyles


def build():
    """Document the CLI template layout and the scaffolding flow."""
    with st_block(s.center_txt):
        st_write(("CLI template format", bs.heading))
        st_space(15)
        st_write(
            "A **CLI template** is a project scaffold packaged inside "
            "a pack at `<pack>/cli_templates/<name>/`. When a user "
            "runs `stx project new --kit <pack>:<kit>`, the kit's "
            "referenced template is copied into the new project "
            "directory, with placeholders (project name, pack list, "
            "DS reference) substituted at scaffold time.",
            bs.body,
        )
        st_space(15)

    # ---- Layout ----
    st_write(("Template directory layout", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "Minimum viable template — same shape as a working project:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
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
    st_space(15)

    # ---- Placeholders ----
    st_write(("Placeholders substituted at scaffold time", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Placeholder", bs.cell_head))
        with g.cell():
            st_write(("Replaced by", bs.cell_head))

        for ph, replaced in [
            ("{{project_name}}",
             "The argument passed to `stx project new <name>`."),
            ("{{pack_declarations}}",
             "TOML `[[packs]]` blocks derived from `--pack` / "
             "`--kit` flags (and the implicit `./mypack` unless "
             "`--no-mypack`)."),
            ("{{design_system_ref}}",
             "`<pack>:<ds_name>` declared by the chosen kit."),
            ("{{kit_ref}}",
             "`<pack>:<kit_name>` of the installed kit, or empty."),
            ("{{streamtex_constraint}}",
             "Version constraint pinned by the pack's "
             "`streamtex_compat` manifest field."),
        ]:
            with g.cell():
                st_write(ph, bs.body)
            with g.cell():
                st_write(replaced, bs.body)
    st_space(15)

    # ---- Wiring in the kit ----
    st_write(("Wiring a CLI template to a kit", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
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
    st_space(15)

    # ---- Authoring tips ----
    st_write(("Authoring tips", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "- Keep templates **small and opinionated** — one starter "
        "block, one ruff config, one CHANGELOG stub. Users add scope "
        "with `stx pack add` and `stx component new`.\n"
        "- The template's `pyproject.toml` lists `streamtex[cli]>=…` "
        "+ the kit's pack as a dependency. Local packs are wired via "
        "`[tool.uv.sources]` when scaffolded with `--mypack`.\n"
        "- The template's `stx.toml` declares `[[packs]]` for the "
        "primary local pack and any external pack referenced by the "
        "kit. The scaffold step writes the right entries from "
        "`--pack` / `--kit` flags.\n"
        "- Templates can ship `_pack_manifest.toml` placeholders for "
        "the local `./mypack/` so it is a working pack from day one.",
        bs.body,
    )
