"""The 9 terms of the reuse architecture glossary."""

from streamtex import st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_design.components.term_definition_list import term_definition_list


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large + s.center_txt


bs = BlockStyles


TERMS = [
    (
        "Pack",
        "A Python package shipping components, design systems, CLI templates, "
        "project blueprints, and kits. Declares an entry point under "
        "streamtex.packs. Local (in-project) or external (git / pypi).",
    ),
    (
        "Component",
        "A Python module with a structured docstring (Visual / Structure / "
        "Styling rules / Extrapolation rules / When to use / When NOT to use "
        "/ Design system bundles required) and a __component_meta__ dict. "
        "Granularity is a tag: primitive, composition, or block.",
    ),
    (
        "Design system",
        "A Python class implementing DesignSystemProtocol — a bag of Style "
        "bundles (colors, titles, callouts, body, ...).",
    ),
    (
        "CLI template",
        "A scaffold (book.py, blocks/, custom/) packaged inside a pack and "
        "copied into new projects by stx project new --kit.",
    ),
    (
        "Project blueprint",
        "A markdown file (instructions for the AI agent) living inside a "
        "pack — the only non-Python artefact.",
    ),
    (
        "Kit",
        "A TOML manifest gluing 1 design system + a curated component list "
        "(+ optionally a CLI template + samples). Installed by "
        "stx kit install <pack>:<kit_name>.",
    ),
    (
        "Primary local pack",
        "The single [[packs]] type=\"local\" primary=true entry in stx.toml "
        "— the default destination for CE capture flows. Created as ./mypack/ "
        "by stx project new.",
    ),
    (
        "stx.toml",
        "The project-level configuration declaring active packs, design "
        "system, resolution preference, and active kit.",
    ),
    (
        "Granularity",
        "A tag on a component, not a constraint: primitive (atomic primitive "
        "like callout or slide_heading), composition (combination of "
        "primitives like card_grid), or block (a full self-contained block "
        "like title_slide).",
    ),
]


def build():
    """List the 9 glossary terms of the reuse architecture."""
    st_write((bs.heading, "Vocabulary"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "Nine terms cover the reuse architecture. Each artefact has a "
        "narrow definition — overlap is intentionally minimal.",
        tag=t.div,
    )
    st_space(20)
    term_definition_list(design_system=DS, items=TERMS)
