"""Validation — codes by family, severity, exit codes, --strict.

Uses comparison_table (streamtex-design) for the exit-codes and
families tables, callout for the severity note.
"""

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


FAMILIES = [
    ("PR0xx", "pack resolution",
     "Pack declared in stx.toml but not installed, duplicate "
     "registration, manifest unreadable, name collision."),
    ("PV0xx", "pack",
     "Manifest present + parseable, entry point registered, "
     "streamtex_compat satisfied, layout sane."),
    ("CV0xx", "component",
     "Module importable, docstring sections present, "
     "__component_meta__ complete, public function exists."),
    ("DV0xx", "design system",
     "Class implements DesignSystemProtocol, required bundle "
     "attributes present, no missing references."),
    ("KV0xx", "kit",
     "TOML parseable, design_system.ref resolves, every "
     "components.include name exists in the pack."),
    ("BV0xx", "blueprint",
     "Markdown valid and references known components / kits."),
]


def build():
    """Document validation families, severities, exit codes, --strict mode."""
    st_write((bs.heading, "Validation"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body + s.center_txt,
        "`stx validate` aggregates validators across every artefact in "
        "the project (pack / component / DS / kit / blueprint) and exits "
        "with a code reflecting the highest severity found.",
        tag=t.div,
    )
    st_space(20)

    # ---- CLI surface ----
    st_write((bs.sub, "CLI surface"), toc_lvl="+1", tag=t.div)
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
    st_space(20)

    # ---- Exit codes ----
    st_write((bs.sub, "Exit codes"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Code", "Meaning"],
        rows=[
            ("0", "No issues — every artefact OK."),
            ("1", "Warnings only. With --strict, this becomes 2."),
            ("2", "At least one error. Build should fail."),
        ],
    )
    st_space(20)

    # ---- Code families ----
    st_write((bs.sub, "Code families"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Family", "Scope", "Checks"],
        rows=FAMILIES,
    )
    st_space(20)

    # ---- Severities ----
    st_write((bs.sub, "Severity model"), toc_lvl="+1", tag=t.div)
    st_space(10)
    callout(
        design_system=DS,
        variant="info",
        title="error vs. warning",
        body=(
            "Each Issue has a severity (error or warning) and a code "
            "(e.g. CV007). Errors are conditions that would break "
            "runtime behaviour; warnings flag practices the system "
            "tolerates but actively discourages. --strict treats every "
            "warning as an error."
        ),
    )
    st_space(20)

    # ---- Typical CI usage ----
    st_write((bs.sub, "Typical CI usage"), toc_lvl="+1", tag=t.div)
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
