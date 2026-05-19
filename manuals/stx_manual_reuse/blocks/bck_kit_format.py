"""Kit format — TOML manifest bundling a DS + a curated component list.

Source: streamtex/cli/kit_cmd.py + streamtex-design/streamtex_design/kits/*.toml.
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
    """Document the kit TOML format and the install / show / new commands."""
    with st_block(s.center_txt):
        st_write(("Kit format", bs.heading))
        st_space(15)
        st_write(
            "A kit is a TOML manifest packaged inside a pack at "
            "`<pack>/kits/<name>.toml`. It bundles **one design system "
            "reference** + **a curated subset of components** the user "
            "is expected to start with. Installing a kit writes "
            "`[design_system].use` and `[kit].use` into the project's "
            "`stx.toml`.",
            bs.body,
        )
        st_space(15)

    # ---- Manifest schema ----
    st_write(("Manifest schema", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# streamtex_design/kits/slides-modern-dark.toml

name = "slides-modern-dark"
description = "Dark presentation kit — atoms + slide-oriented blocks."
since = "2026-05-19"

[design_system]
ref = "modern_dark"            # local DS name OR <pack>:<name>

[components]
include = [
    "slide_heading",
    "cite",
    "callout",
    "card_grid",
    "stat_hero",
    "title_slide",
    "evidence_insight",
    "feature_walkthrough",
    "narrative_transition",
]

# Optional — bundle a CLI template the kit installs alongside
[cli_template]
ref = "slides-template"

# Optional — bundle project blueprints (AI-agent .md instructions)
[blueprints]
include = ["presentation-default.md"]

# Optional — sample blocks copied verbatim into ./blocks/
[samples]
include = ["bck_title_demo.py", "bck_card_grid_demo.py"]
""",
            language="toml",
        )
    st_space(15)

    # ---- Required vs optional ----
    st_write(("Required vs optional fields", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 1fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Section", bs.cell_head))
        with g.cell():
            st_write(("Status", bs.cell_head))
        with g.cell():
            st_write(("Meaning", bs.cell_head))

        for section, status, meaning in [
            ("name / description / since", "required",
             "Identity metadata; `since` is an ISO date string."),
            ("[design_system].ref", "required",
             "Active DS to record in stx.toml. Same-pack DSs use the "
             "bare name; cross-pack uses `<pack>:<name>`."),
            ("[components].include", "required",
             "List of component names the kit recommends. The resolver "
             "does not enforce this list — it's a curated subset."),
            ("[cli_template].ref", "optional",
             "Identifier of a CLI template bundled with the kit "
             "(scaffold copied by `stx project new --kit`)."),
            ("[blueprints].include", "optional",
             "Project blueprints (.md AI-agent instructions) shipped "
             "into the project."),
            ("[samples].include", "optional",
             "Sample block files copied verbatim into `./blocks/` to "
             "give the user a starting point."),
        ]:
            with g.cell():
                st_write(section, bs.body)
            with g.cell():
                st_write(status, bs.body)
            with g.cell():
                st_write(meaning, bs.body)
    st_space(15)

    # ---- CLI ----
    st_write(("CLI surface", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# List available kits across all installed packs
stx kit list

# Inspect a kit's content
stx kit show streamtex-design:slides-modern-dark

# Apply a kit (records design_system + kit reference in stx.toml)
stx kit install streamtex-design:slides-modern-dark

# Scaffold a new kit inside a pack
stx kit new my-kit --pack mypack --design-system default

# Validate one or every kit
stx kit validate streamtex-design:slides-modern-dark
stx kit validate
""",
            language="bash",
        )
    st_space(15)

    st_write(
        "Validation emits `KV001`-`KV005` for kit-level issues "
        "(missing DS, unknown component, malformed TOML). See the "
        "validation block for the full code table.",
        bs.body,
    )
