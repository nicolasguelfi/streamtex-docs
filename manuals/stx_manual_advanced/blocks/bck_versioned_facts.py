"""Versioned Facts — streamtex.facts: facts/<source>.toml, fact(), stale facts (0.7.40)."""

from pathlib import Path

from blocks.helpers import show_code, show_details, show_explanation
from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.facts import fact

# The manual's own facts/ folder (this file: <manual>/blocks/bck_versioned_facts.py)
MANUAL_ROOT = Path(__file__).resolve().parent.parent


class BlockStyles:
    """Versioned facts chapter styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Versioned Facts", tag=t.div, toc_lvl="1")
        st_space("v", 2)

        show_explanation("""\
            A course about a method, a tool or a library states facts that
            come from it: a number of agents, a list of commands, a path, a
            default value. When the source releases a new version, every
            slide that copied a fact by hand has to be found and re-checked.

            `streamtex.facts` keeps such facts in ONE data file per source,
            together with the source version they were read from. Blocks
            read them with `fact()`, and `stx validate` warns when the
            source has moved on since.
        """)
        st_space("v", 2)

        # --- 1. The data file ---
        st_write(bs.sub, "One file per source — facts/<source>.toml", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# facts/gse-one.toml — next to the project's stx.toml
[source]
name = "GSE-One"
version = "0.85.0"                 # the version these facts were read from
current = "../gensem/VERSION"      # optional: where the CURRENT version is
                                   # (a text file, or a pyproject.toml)
[facts]
agents = 23
commands = 41
paths.registry = ".gse/registry"   # nested keys: fact("gse-one", "paths.registry")
""", language="toml", line_numbers=False)
        st_space("v", 2)

        # --- 2. Reading a fact ---
        st_write(bs.sub, "Reading a fact — fact()", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            `fact(source, key)` returns one value; a dotted key reaches a
            nested table. An unknown source or key raises `KeyError`: a fact
            never silently disappears from a slide. The file is found in the
            `facts/` folder next to the nearest `stx.toml` (or under `root=`),
            and re-read when it changes. `fact` is NOT in the star import:
            import it explicitly.
        """)
        st_space("v", 1)

        show_code("""\
from streamtex.facts import fact

def build():
    st_write(s.large, f"{fact('gse-one', 'agents')} specialised agents")
    st_write(s.medium, "Registry: ", fact("gse-one", "paths.registry"))""")
        st_space("v", 1)

        show_explanation("""\
            Live — this manual keeps a few facts about streamtex itself in
            `facts/streamtex.toml` (read here with `root=` pointing at the
            manual folder):
        """)
        st_space("v", 1)

        show_code("""\
from pathlib import Path
from streamtex.facts import fact

MANUAL_ROOT = Path(__file__).resolve().parent.parent

fact("streamtex", "book_defaults.keys", root=MANUAL_ROOT)
fact("streamtex", "slides.container_min_height", root=MANUAL_ROOT)
fact("streamtex", "scale.amphi_base_pt", root=MANUAL_ROOT)""")
        st_space("v", 1)

        with st_block(s.project.containers.explanation_box):
            st_write(s.medium, (bs.param_label, "book_defaults.keys = "),
                     str(fact("streamtex", "book_defaults.keys", root=MANUAL_ROOT)))
            st_write(s.medium, (bs.param_label, "slides.container_min_height = "),
                     str(fact("streamtex", "slides.container_min_height", root=MANUAL_ROOT)))
            st_write(s.medium, (bs.param_label, "scale.amphi_base_pt = "),
                     str(fact("streamtex", "scale.amphi_base_pt", root=MANUAL_ROOT)))
        st_space("v", 2)

        # --- 3. Staleness in stx validate ---
        st_write(bs.sub, "When the source moves on — stx validate", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When `[source] current` points to a file holding the source's
            current version (first line of a text file such as VERSION, or
            `[project].version` of a pyproject.toml), `stx validate` compares
            it with `[source] version`. A difference is a warning, with the
            number of facts to re-check. Without `current`, nothing is
            compared.
        """)
        st_space("v", 1)

        show_code("""\
$ stx validate
Facts
  stale facts/gse-one.toml: read from 0.85.0, the source is now 0.86.0 — re-check its 3 fact(s), then update [source].version
""", language="text", line_numbers=False)
        st_space("v", 1)

        show_details("""\
            The workflow on a new version of the source: open
            `facts/<source>.toml`, re-check each fact against the new
            version, correct the values, then set `[source] version` to the
            new version — the warning disappears, and every slide that reads
            the facts shows the new values.

            `stale_facts(root)` (in `streamtex.facts`) returns the same list
            for scripts: source, recorded version, current version, number
            of facts.
        """)
        st_space("v", 2)
