"""Kit format — TOML manifest bundling a DS + a curated component list."""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


def build():
    """Document the kit TOML format and the install / show / new commands."""
    st_write((bs.heading, "Kit format"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "A kit is a TOML manifest packaged inside a pack at "
        "<pack>/kits/<name>.toml. It bundles one design system reference "
        "+ a curated subset of components. Installing a kit writes "
        "[design_system].use and [kit].use into the project's stx.toml.",
        tag=t.div,
    )
    st_space(20)

    # ---- Manifest schema ----
    st_write((bs.sub, "Manifest schema"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code):
        st_code(
            code="""
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
    st_space(20)

    # ---- Required vs optional ----
    st_write((bs.sub, "Required vs optional fields"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Section", "Status", "Meaning"],
        rows=[
            ("name / description / since", "required",
             "Identity metadata; since is an ISO date string."),
            ("[design_system].ref", "required",
             "Active DS to record in stx.toml. Same-pack uses the bare "
             "name; cross-pack uses <pack>:<name>."),
            ("[components].include", "required",
             "List of component names the kit recommends. The resolver "
             "doesn't enforce this list — it's a curated subset."),
            ("[cli_template].ref", "optional",
             "Identifier of a CLI template bundled with the kit (scaffold "
             "copied by stx project new --kit)."),
            ("[blueprints].include", "optional",
             "Project blueprints (.md AI-agent instructions)."),
            ("[samples].include", "optional",
             "Sample block files copied verbatim into ./blocks/."),
        ],
    )
    st_space(20)

    # ---- CLI ----
    st_write((bs.sub, "CLI surface"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code):
        st_code(
            code="""
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
    callout(
        design_system=DS,
        variant="info",
        title="Validation",
        body=(
            "Kit validation emits KV001-KV005 for kit-level issues "
            "(missing DS, unknown component, malformed TOML). See the "
            "validation block for the full code table."
        ),
    )
