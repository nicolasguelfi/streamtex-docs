"""Welcome — introduce the reuse architecture and its four artefacts.

Uses three components from the streamtex-manuals pack to render an
attractive overview: a pitch_hero opening, then a column_features
grid that contrasts "Reusable artefacts" with "Distribution model".
"""

from streamtex import st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_manuals.components.column_features import column_features
from streamtex_manuals.components.pitch_hero import pitch_hero


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    cta = s.bold + s.large + s.center_txt


bs = BlockStyles


def build():
    """Introduce the reuse architecture (packs, components, design systems, kits)."""
    st_write(
        (bs.heading, "StreamTeX — Reuse Architecture"),
        toc_lvl="1", tag=t.div,
    )
    st_write(
        (bs.sub + s.center_txt, "Packs, components, design systems, kits"),
        tag=t.div,
    )
    st_space(15)

    pitch_hero(
        design_system=DS,
        lead="Every reusable visual artefact ships as part of a Python pack.",
        body=(
            "Components, design systems, CLI templates, project "
            "blueprints, and kits are discovered at runtime via the "
            "streamtex.packs entry point (PEP 621). A project declares "
            "its packs in stx.toml, picks an active design system, and "
            "uses kits to bootstrap a coherent starter."
        ),
        gradient_start_rgba=(46, 204, 113),
        gradient_end_rgba=(46, 196, 182),
    )

    st_space(20)
    st_write(bs.cta, "What changed at a glance", toc_lvl="+1", tag=t.div)
    st_space(10)

    column_features(
        design_system=DS,
        columns=[
            (
                "Reusable artefacts",
                "success",
                [
                    "Components — Python modules with a docstring contract "
                    "(Visual / Structure / Styling / INVARIANTS / PARAMS / "
                    "INTERDITS / When to use / NOT to use).",
                    "Design systems — Python classes implementing "
                    "DesignSystemProtocol.",
                    "Kits — TOML manifests bundling a DS + a curated "
                    "component subset.",
                    "CLI templates + project blueprints — optional scaffolds.",
                ],
            ),
            (
                "Distribution model",
                "info",
                [
                    "Multi-pack: declare one or many packs in stx.toml.",
                    "Three sources, one command: stx pack add "
                    "git:<url>[@rev] / local:<path> / pypi:<name>[@spec].",
                    "Editable dev: stx pack add <path> --dev.",
                    "Local mypack is created by stx project new — default "
                    "capture destination for stx component new.",
                ],
            ),
        ],
        min_col_width="320px",
    )
