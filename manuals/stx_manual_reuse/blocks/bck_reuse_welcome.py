"""Welcome — introduce the reuse architecture and its four artefacts."""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    grid_cell = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Introduce the reuse architecture (packs, components, design systems, kits)."""
    with st_block(s.center_txt):
        st_write((bs.heading, "StreamTeX — Reuse Architecture"), toc_lvl="1")
        st_write(
            (bs.sub, "Packs, components, design systems, kits"),
        )
        st_space(20)

        st_write(
            bs.body,
            "The reuse layer of the library ships every reusable artefact "
            "(component, design system, CLI template, project blueprint, "
            "kit) as part of a Python package — a pack — discovered at "
            "runtime via the streamtex.packs entry point (PEP 621).",
        )
        st_space(15)
        st_write(
            bs.body,
            "The official reference pack is streamtex-design. A project "
            "declares its packs in stx.toml, picks an active design system, "
            "and uses kits to bootstrap a coherent starter (e.g. "
            "slides-modern-dark, project-default, manual-default).",
        )
        st_space(15)
        st_write(
            bs.body + s.bold,
            "What changed at a glance:",
        )
        with st_grid(2, gap=10):
            with st_block(bs.grid_cell):
                st_write((s.bold, "Reusable artefacts"))
                st_write(
                    "- Components — Python modules with a docstring contract "
                    "(Visual / Structure / Styling / INVARIANTS / PARAMS / "
                    "INTERDITS / When to use / NOT to use).\n"
                    "- Design systems — Python classes implementing "
                    "DesignSystemProtocol.\n"
                    "- Kits — TOML manifests bundling a DS + a curated "
                    "component subset.\n"
                    "- CLI templates + project blueprints — optional scaffolds.",
                )
            with st_block(bs.grid_cell):
                st_write((s.bold, "Distribution model"))
                st_write(
                    "- Multi-pack: declare one or many packs in stx.toml.\n"
                    "- Three sources, one command: stx pack add "
                    "git:<url>[@rev] / local:<path> / pypi:<name>[@spec].\n"
                    "- Editable dev: stx pack add <path> --dev.\n"
                    "- Local mypack is created by stx project new — default "
                    "capture destination for stx component new.",
                )
