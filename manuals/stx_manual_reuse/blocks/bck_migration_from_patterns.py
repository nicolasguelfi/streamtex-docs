"""Migration guide — from the legacy patterns flow (≤ 0.6.x) to packs (≥ 0.7.x).

Source: CHANGELOGs Wave 1-4 + PLAN.md §22 (Migration).
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
    """Map legacy concepts/commands onto the new reuse architecture."""
    with st_block(s.center_txt):
        st_write(("Migration from the patterns flow", bs.heading))
        st_space(15)
        st_write(
            "The legacy `streamtex-patterns` sibling repo + "
            "`.claude/custom/streamtex-patterns/` install path is "
            "removed in 0.7.x. Every reusable artefact now ships "
            "inside a Python pack discovered via the "
            "`streamtex.packs` entry point. This block maps the "
            "old vocabulary onto the new one.",
            bs.body,
        )
        st_space(15)

    # ---- Vocabulary ----
    st_write(("Vocabulary mapping", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 2fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Legacy (≤ 0.6.x)", bs.cell_head))
        with g.cell():
            st_write(("New (≥ 0.7.x)", bs.cell_head))

        for old, new in [
            ("Pattern", "Component (Python module with docstring "
                        "contract + `__component_meta__`)"),
            ("Pattern catalogue (.md files)",
             "Pack — Python package shipping components, design "
             "systems, kits"),
            ("Preset (slides / docs / core / ai4se6d)",
             "Kit (TOML manifest bundling 1 DS + a curated "
             "component list)"),
            ("Blueprint (block type)",
             "Block template (visual layout pattern, still relevant "
             "for AI block generation — see the AI manual)"),
            ("Project blueprint (was conflated with blueprint)",
             "Project blueprint — .md file with AI-agent "
             "instructions, lives inside a pack"),
            ("Capture (copy into "
             "`.claude/custom/streamtex-patterns/`)",
             "Capture (scaffold into the primary local pack, "
             "`./mypack/components/`, via `stx component new`)"),
            ("Promote (PR to streamtex-patterns)",
             "Promote (four-branch routing — `stx component "
             "promote --to=<pack>`)"),
        ]:
            with g.cell():
                st_write(old, bs.body)
            with g.cell():
                st_write(new, bs.body)
    st_space(15)

    # ---- CLI mapping ----
    st_write(("CLI mapping", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 2fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Legacy command", bs.cell_head))
        with g.cell():
            st_write(("New equivalent", bs.cell_head))

        for old, new in [
            ("stx patterns list", "stx component list"),
            ("stx patterns presets", "stx kit list"),
            ("stx patterns install --preset slides",
             "stx kit install streamtex-design:slides-modern-dark"),
            ("stx patterns install --pattern ptn_callout",
             "(no equivalent — install the pack via "
             "`stx pack add`; components are then importable)"),
            ("stx patterns update / sync",
             "stx pack sync (delegates to `uv sync`)"),
            ("stx patterns status",
             "stx pack list --trace (lifecycle states + transitions)"),
            ("stx patterns diff <name>",
             "git diff (components are real Python modules)"),
            ("stx patterns validate",
             "stx validate [--strict] (aggregate) or "
             "stx component validate"),
            ("stx patterns promote <name>",
             "stx component promote <name> --to=<pack>"),
            ("stx patterns remove <name>",
             "stx pack remove <name> (removes the whole pack — "
             "individual components are not separately removable)"),
        ]:
            with g.cell():
                st_write(old, bs.body)
            with g.cell():
                st_write(new, bs.body)
    st_space(15)

    # ---- Step-by-step migration ----
    st_write(("Step-by-step migration", bs.sub), toc_lvl="+1")
    st_space(10)
    st_write(
        "For an existing project tracked at 0.6.x:",
        bs.body,
    )
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
# 1) Update streamtex
uv add 'streamtex[cli]>=0.7.0'

# 2) Install the reference design pack (replaces the streamtex-patterns docs scope)
stx pack add git:github.com/nicolasguelfi/streamtex-design@v0.2.0
stx pack sync

# 3) Install a kit matching the legacy preset you used
#    - slides preset       → streamtex-design:slides-modern-dark
#    - docs preset         → streamtex-design:manual-default
#    - core preset         → streamtex-design:core
stx kit install streamtex-design:manual-default

# 4) Delete the obsolete folder
rm -rf .claude/custom/streamtex-patterns/

# 5) Validate
stx validate --strict
""",
            language="bash",
        )
    st_space(15)

    st_write(
        "Captured patterns from the old system (under "
        "`.claude/custom/streamtex-patterns/<name>.md`) have no "
        "automatic migration — the format is different. For each "
        "captured pattern, scaffold a fresh component "
        "(`stx component new <name>`), translate the markdown "
        "spec into the docstring contract, then delete the .md.",
        bs.body,
    )
