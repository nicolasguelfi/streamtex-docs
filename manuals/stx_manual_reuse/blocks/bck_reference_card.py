"""Reference card — CLI cheatsheet for the reuse architecture."""

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
    code_box = s.container.paddings.small_padding + s.container.borders.solid_border


bs = BlockStyles


COMMANDS = """\
# ---- packs ----
# REF formats: git:<url>[@rev] | local:<path> | pypi:<name>[@spec] | <plain-path>
stx pack add <ref> [--dev]
stx pack remove <name>
stx pack list [--trace]
stx pack sync
stx pack info <name>
stx pack validate [<name>]
stx pack new <name> [--path <path>]
stx pack set-primary <name>

# ---- components ----
stx component list [--pack <p>]
stx component show <name>
stx component find <query>
stx component new <name> [--pack <p>] [--granularity primitive|composition|block]
stx component validate [<name>]      # no arg = validate every component
stx component promote <name> --to <pack> [--no-commit]

# ---- design systems ----
stx ds list
stx ds show <ref>
stx ds switch <ref>
stx ds new <name> [--pack <p>]
stx ds validate [<ref>]

# ---- kits ----
stx kit list
stx kit show <ref>
stx kit install <ref>                # ref = <pack>:<kit_name>
stx kit new <name> [--pack <p>] [--design-system <ds>]
stx kit validate [<ref>]

# ---- aggregate ----
stx validate [--strict]              # exit 0=ok, 1=warnings, 2=errors

# ---- project ----
stx project new <name>
       [--profile <p>] [--collection]
       [--kit <pack>:<kit_name>] [--pack <ref>]
       [--pack-name <name>] [--no-mypack]
       [--no-git] [--no-sync] [--no-claude]
stx project validate [<path>]        # default path = "."
"""


ERROR_CODES = [
    ("PR001", "Promotion to a pypi pack refused (see promotion flow, branch 4)."),
    ("PR002", "Pack declared in stx.toml but not installed (drift install)."),
    ("PR003", "Manifest _pack_manifest.toml unreadable (broken manifest)."),
    ("PR004", "Entry-point collision on the pack name."),
    ("PV001-PV010", "Pack manifest validation failed (format, semver, compat)."),
    ("CV001-CV011", "Component validation failed (docstring / meta)."),
    ("DV001-DV006", "Design system validation failed (Protocol)."),
    ("KV001-KV005", "Kit validation failed."),
    ("BV001-BV002", "Bundle required by a component absent from the active DS."),
]


def build():
    """Quick reference for the reuse architecture CLI + error codes."""
    st_write((bs.heading, "Reference card"), toc_lvl="1", tag=t.div)
    st_space(15)

    st_write((bs.sub, "CLI surface"), toc_lvl="+1", tag=t.div)
    st_space(10)
    with st_block(bs.code_box):
        st_code(code=COMMANDS, language="bash")
    st_space(20)

    st_write((bs.sub, "Error codes"), toc_lvl="+1", tag=t.div)
    st_space(10)
    comparison_table(
        design_system=DS,
        columns=["Code", "Meaning"],
        rows=ERROR_CODES,
    )
