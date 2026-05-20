"""Troubleshooting — common error codes and how to recover from them.

Uses comparison_table for the recipes-by-code 3-column index.
"""

from streamtex import st_block, st_code, st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.comparison_table import comparison_table


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


CASES = [
    ("PR001",
     "stx component promote refuses with 'PyPI destination is read-only'.",
     "Promote to the upstream git pack of the same project instead, "
     "then bump the PyPI release manually."),
    ("PR002",
     "stx pack list shows state drift_install — declared but no matching entry point.",
     "Run stx pack sync. If still missing, check the pack's "
     "pyproject.toml [project.entry-points.\"streamtex.packs\"]."),
    ("PR003",
     "State manifest_broken — installed but _pack_manifest.toml fails to load.",
     "Re-validate the manifest. Common issues: TOML syntax, missing "
     "[manifest] / [pack] / [entrypoint], invalid streamtex_compat."),
    ("PR004",
     "State collision — two installed packs declare the same name.",
     "Pick one and stx pack remove the other, or rename one in its "
     "_pack_manifest.toml + pyproject.toml entry point."),
    ("PV002",
     "Pack validation fails: entry point not registered.",
     "Add [project.entry-points.\"streamtex.packs\"] <name>=\"<module>\" "
     "to the pack's pyproject.toml. Reinstall with uv sync."),
    ("CV001-CV004",
     "Component module fails to import, missing docstring section, or "
     "__component_meta__ malformed.",
     "Run stx component show <name> to see the failure. The scaffold "
     "from stx component new is always valid — diff against it."),
    ("CV007",
     "Docstring INVARIANTS / PARAMS / INTERDITS block is empty or missing.",
     "Fill the three sub-sections under Extrapolation rules. Empty "
     "INTERDITS is allowed but must be the literal string '(none)'."),
    ("CV010",
     "Design system bundles required references a bundle that doesn't "
     "exist on the active DS.",
     "Either add the bundle to the DS or remove the reference. "
     "stx ds show <ref> lists available bundles."),
    ("DV001-DV003",
     "DS class doesn't implement DesignSystemProtocol, or a required "
     "bundle attribute is missing.",
     "The DS must expose every bundle declared as required by the "
     "components in the active kit."),
    ("KV002",
     "Kit references a component not present in the host pack.",
     "Add the missing component (stx component new) or remove the "
     "name from [components].include."),
    ("KV003",
     "Kit references a design system that doesn't resolve.",
     "Check [design_system].ref. Same-pack DSs use the bare name; "
     "cross-pack DSs use <pack>:<name>."),
]


def build():
    """Common error codes + recovery recipes."""
    st_write((bs.heading, "Troubleshooting"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "Cookbook of the most common error codes raised by the discoverer "
        "(PR0xx) and the validators (PV/CV/DV/KV/BV0xx), with one-line fixes.",
        tag=t.div,
    )
    st_space(20)

    # ---- Recipes ----
    st_write((bs.sub, "Recipes by code"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Code", "Symptom", "Fix"],
        rows=CASES,
    )
    st_space(20)

    # ---- General workflow ----
    st_write((bs.sub, "General debugging workflow"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code):
        st_code(
            code="""
# 1) Inspect declared vs installed
stx pack list --trace

# 2) Per-pack deep dive
stx pack info <pack-name>

# 3) Aggregate validation
stx validate --strict

# 4) For a specific component
stx component show <component>
stx component validate <component>

# 5) For an unexpected runtime error in a block, run with --debug
stx run --debug
""",
            language="bash",
        )
