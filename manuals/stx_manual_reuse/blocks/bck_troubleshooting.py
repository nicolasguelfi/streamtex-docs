"""Troubleshooting — common error codes and how to recover from them.

Source: streamtex/core/validation.py + streamtex/core/discovery.py + pack_cmd.py.
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


CASES = [
    # (code, symptom, fix)
    ("PR001",
     "`stx component promote` refuses with 'PyPI destination is "
     "read-only'.",
     "Promote to the upstream **git** pack of the same project "
     "instead, then bump the PyPI release manually."),
    ("PR002",
     "`stx pack list` shows state `drift_install` — the pack is "
     "declared in stx.toml but no matching entry point is found.",
     "Run `stx pack sync`. If still missing, check that the pack's "
     "`pyproject.toml` declares `[project.entry-points.\"streamtex."
     "packs\"]`."),
    ("PR003",
     "State `manifest_broken` — installed but `_pack_manifest."
     "toml` fails to load.",
     "Re-validate the manifest. Common issues: TOML syntax error, "
     "missing `[manifest]` / `[pack]` / `[entrypoint]` section, "
     "invalid `streamtex_compat` constraint."),
    ("PR004",
     "State `collision` — two installed packs declare the same "
     "name.",
     "Pick one and `stx pack remove` the other, or rename one in "
     "its `_pack_manifest.toml` + `pyproject.toml` entry point."),
    ("PV002",
     "Pack validation fails: entry point not registered.",
     "Add `[project.entry-points.\"streamtex.packs\"]\\n<name> = "
     "\"<module>\"` to the pack's `pyproject.toml`. Reinstall with "
     "`uv sync`."),
    ("CV001-CV004",
     "Component module fails to import, missing docstring section, "
     "or `__component_meta__` malformed.",
     "Run `stx component show <name>` to see the exact failure. "
     "The scaffold from `stx component new` is always valid — diff "
     "against it if unsure."),
    ("CV007",
     "Docstring `INVARIANTS` / `PARAMS` / `INTERDITS` block is "
     "empty or missing.",
     "Fill the three sub-sections under `Extrapolation rules`. "
     "Empty `INTERDITS` is allowed but must be the literal string "
     "'(none)'."),
    ("CV010",
     "`Design system bundles required` references a bundle that "
     "doesn't exist on the active DS.",
     "Either add the bundle to the DS (`stx ds new` or edit) or "
     "remove the reference. `stx ds show <ref>` lists available "
     "bundles."),
    ("DV001-DV003",
     "DS class doesn't implement `DesignSystemProtocol`, or a "
     "required bundle attribute is missing.",
     "The DS class must expose every bundle declared as required "
     "by the components in the active kit. Add the missing "
     "attribute or remove the offending component from the kit."),
    ("KV002",
     "Kit references a component not present in the host pack.",
     "Add the missing component to the pack (`stx component new`) "
     "or remove the name from `[components].include`."),
    ("KV003",
     "Kit references a design system that doesn't resolve.",
     "Check `[design_system].ref`. Same-pack DSs use the bare "
     "name; cross-pack DSs use `<pack>:<name>`."),
]


def build():
    """Common error codes + recovery recipes."""
    with st_block(s.center_txt):
        st_write(("Troubleshooting", bs.heading))
        st_space(15)
        st_write(
            "Cookbook of the most common error codes raised by the "
            "discoverer (`PR0xx`) and the validators (`PV/CV/DV/KV/"
            "BV0xx`), with one-line fixes.",
            bs.body,
        )
        st_space(15)

    # ---- Recipes ----
    st_write(("Recipes by code", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 3fr 3fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write(("Code", bs.cell_head))
        with g.cell():
            st_write(("Symptom", bs.cell_head))
        with g.cell():
            st_write(("Fix", bs.cell_head))

        for code, symptom, fix in CASES:
            with g.cell():
                st_write(code, bs.body + s.bold)
            with g.cell():
                st_write(symptom, bs.body)
            with g.cell():
                st_write(fix, bs.body)
    st_space(15)

    # ---- General workflow ----
    st_write(("General debugging workflow", bs.sub), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            """
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
