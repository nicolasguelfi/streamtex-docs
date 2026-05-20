"""FAQ — the recurring questions about packs / components / DS / kits.

Each Q&A is rendered as an info callout from streamtex-design.
"""

from streamtex import st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.callout import callout


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large + s.center_txt


bs = BlockStyles


QA = [
    ("Why Python packs instead of a markdown catalogue?",
     "Components are real Python modules — `from streamtex_design.components "
     "import callout` works the same way as any other import. git diff shows "
     "actual changes, pytest tests it, basedpyright covers it, ruff lints it. "
     "No separate scan-time parser, no drift bookkeeping. The "
     "structured-docstring contract inside each component module replaces "
     "a markdown spec."),
    ("Can a project consume more than one pack?",
     "Yes. The reuse architecture is multi-pack by default. Declare each "
     "pack as a [[packs]] entry in stx.toml. Components from any installed "
     "pack are importable; stx component list enumerates them all."),
    ("What's the difference between a kit and a design system?",
     "A design system is the visual palette (a Python class implementing "
     "DesignSystemProtocol). A kit bundles one DS with a curated subset of "
     "components — it's a starter selection, not a constraint. Installing a "
     "kit writes [design_system].use and [kit].use into stx.toml; you can "
     "later change the DS without re-installing the kit (stx ds switch)."),
    ("Is the component granularity enforced?",
     "No — it's a tag, not a constraint. The resolver doesn't filter on it. "
     "The granularity is set at creation time "
     "(stx component new my_widget --granularity composition) and documents "
     "intent."),
    ("Can I capture a component into a non-primary pack?",
     "Yes — stx component new my_widget --pack <name> accepts any local "
     "pack. Without --pack, the scaffold lands in the primary local pack "
     "(the one with primary = true in stx.toml). Capturing into a remote "
     "git or PyPI pack is refused — promotion goes through "
     "stx component promote."),
    ("Is the preset vocabulary used elsewhere in the CLI?",
     "Yes — stx install --preset standard|user|developer|… selects the "
     "workspace preset (repos cloned, extras installed). That preset is "
     "unrelated to kits — kits live inside packs and bundle a DS with a "
     "curated component list."),
    ("Why do I see extrapolable=True in __component_meta__?",
     "It signals to the AI agent that the component accepts extrapolation "
     "within PARAMS (e.g. adapting kind= to a different design language). "
     "extrapolable=False means the component is rigid — the AI must use it "
     "as-is or scaffold a new one."),
    ("Where does mypack come from? Why is it the default?",
     "stx project new scaffolds ./mypack/ as a sub-folder with "
     "primary = true — the default destination for capture. It's installed "
     "editable via uv pip install -e ./mypack so edits are immediate. You "
     "can opt out with --no-mypack (typical for projects that only consume "
     "external packs)."),
    ("Do I need streamtex-design to do anything useful?",
     "No — streamtex-design is the official reference pack but the "
     "architecture itself doesn't require it. You can ship a project with "
     "only ./mypack/ and a local DS. In practice, streamtex-design covers "
     "the universal primitives (callouts, headings, cards, comparison "
     "tables…) so most projects pull it as a starting point."),
]


def build():
    """Render the FAQ as info callouts."""
    st_write((bs.heading, "FAQ"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Recurring questions about packs, components, design systems, and kits.",
        tag=t.div,
    )
    st_space(20)
    for question, answer in QA:
        callout(
            design_system=DS,
            variant="info",
            title=question,
            body=answer,
        )
        st_space(10)
