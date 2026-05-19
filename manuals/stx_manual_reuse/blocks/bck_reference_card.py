"""Reference card — CLI cheatsheet for the reuse architecture (PLAN §7)."""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large
    code = s.container.paddings.small_padding + s.container.borders.solid_border
    section = s.bold + s.large


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
    ("PR001", "Promotion vers un pack pypi refusée (cf. §8.3 branche 4)."),
    ("PR002", "Pack déclaré dans stx.toml mais pas installé (Drift install)."),
    ("PR003", "Manifest _pack_manifest.toml illisible (Manifest cassé)."),
    ("PR004", "Collision d'entry-points sur le nom du pack."),
    ("PV001-PV010", "Échec validation du manifest pack (format, semver, compat)."),
    ("CV001-CV011", "Échec validation d'un component (docstring / meta)."),
    ("DV001-DV006", "Échec validation d'un design system (Protocol)."),
    ("KV001-KV005", "Échec validation d'un kit."),
    ("BV001-BV002", "Bundle requis par un component absent du design system actif."),
]


def build():
    """Quick reference for the reuse architecture CLI + error codes."""
    with st_block(s.center_txt):
        st_write(("Reference card", bs.heading))
        st_space(15)
        st_write(("CLI surface", bs.section))
        with st_block(bs.code):
            st_code(COMMANDS, language="bash")

        st_space(20)
        st_write(("Error codes", bs.section))
        for code, description in ERROR_CODES:
            st_write(
                (code + " — ", s.bold),
                description,
                bs.body,
            )
            st_space(4)
