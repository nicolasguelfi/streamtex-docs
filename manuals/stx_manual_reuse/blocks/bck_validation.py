"""Validation — codes by family, severity, exit codes, --strict.

Source: streamtex/core/validation.py + streamtex/cli/validate_cmd.py.
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


# (family, count, what it checks)
FAMILIES = [
    ("PR0xx", "pack resolution",
     "Pack declared in stx.toml but not installed, duplicate "
     "registration, manifest unreadable, name collision. Emitted by "
     "the discoverer (not the validator itself), but bubbles up."),
    ("PV0xx", "pack",
     "Pack-level checks: manifest present and parseable, entry "
     "point registered, streamtex_compat satisfied, layout sane "
     "(`components/`, `design_systems/`, `kits/` reachable)."),
    ("CV0xx", "component",
     "Component-level checks: module importable, docstring "
     "sections present (Visual / Structure / Styling rules / "
     "INVARIANTS / PARAMS / INTERDITS / When to use / NOT to use / "
     "Bundles required), `__component_meta__` complete, public "
     "function exists with the documented PARAMS."),
    ("DV0xx", "design system",
     "DS-level checks: class implements `DesignSystemProtocol`, "
     "required bundle attributes present, no missing references "
     "to undefined bundles."),
    ("KV0xx", "kit",
     "Kit-level checks: TOML parseable, [design_system].ref "
     "resolves, every [components].include name exists in the "
     "pack, optional [cli_template].ref resolves."),
    ("BV0xx", "blueprint",
     "Project blueprint-level checks (when present): file is "
     "valid markdown and references known components / kits."),
]


def build():
    """Document validation families, severities, exit codes, --strict mode."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Validation"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "`stx validate` aggregates validators across every "
            "artefact in the project (pack / component / DS / kit / "
            "blueprint) and exits with a code reflecting the "
            "highest severity found.",
        )
        st_space(15)

    # ---- CLI surface ----
    st_write((bs.sub, "CLI surface"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# Per-family
stx pack validate [<name>]
stx component validate [<name>]
stx ds validate [<ref>]
stx kit validate [<ref>]

# Aggregate (all families)
stx validate

# CI-grade gate (promotes warnings to errors)
stx validate --strict
""",
            language="bash",
        )
    st_space(15)

    # ---- Exit codes ----
    st_write((bs.sub, "Exit codes"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.cell_head, "Code"))
        with g.cell():
            st_write((bs.cell_head, "Meaning"))

        for code, meaning in [
            ("0", "No issues — every artefact OK."),
            ("1", "Warnings only (no errors). With `--strict`, "
                  "this becomes 2."),
            ("2", "At least one error. Build should fail."),
        ]:
            with g.cell():
                st_write(bs.body + s.bold, code)
            with g.cell():
                st_write(bs.body, meaning)
    st_space(15)

    # ---- Code families ----
    st_write((bs.sub, "Code families"), toc_lvl="+1")
    st_space(10)

    with st_grid(cols="1fr 1fr 4fr", gap="8px", cell_styles=bs.cell) as g:
        with g.cell():
            st_write((bs.cell_head, "Family"))
        with g.cell():
            st_write((bs.cell_head, "Scope"))
        with g.cell():
            st_write((bs.cell_head, "Checks"))

        for fam, scope, checks in FAMILIES:
            with g.cell():
                st_write(bs.body + s.bold, fam)
            with g.cell():
                st_write(bs.body, scope)
            with g.cell():
                st_write(bs.body, checks)
    st_space(15)

    # ---- Severities ----
    st_write((bs.sub, "Severity model"), toc_lvl="+1")
    st_space(10)
    st_write(
        bs.body,
        "Each `Issue` has a `severity` (`error` or `warning`) and a "
        "`code` (e.g. `CV007`). Errors are conditions that would "
        "break runtime behaviour; warnings flag practices the "
        "system tolerates but actively discourages. `--strict` "
        "treats every warning as an error.",
    )
    st_space(15)

    # ---- Typical CI usage ----
    st_write((bs.sub, "Typical CI usage"), toc_lvl="+1")
    st_space(10)

    with st_block(bs.code):
        st_code(
            code="""
# .github/workflows/test.yml
- name: Validate reuse-architecture artefacts
  run: uv run stx validate --strict
""",
            language="yaml",
        )
