"""Welcome — why the reuse architecture replaces the legacy patterns flow."""

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
        st_write(("StreamTeX — Reuse Architecture", bs.heading))
        st_write(
            ("Packs, components, design systems, kits", bs.sub),
        )
        st_space(20)

        st_write(
            "Since streamtex 0.7.x, the reuse layer of the library no longer "
            "lives in markdown files inside a sibling repo. Instead, every "
            "reusable artefact (component, design system, CLI template, "
            "project blueprint, kit) is shipped as part of a Python package "
            "— a pack — discovered at runtime via the streamtex.packs entry "
            "point (PEP 621).",
            bs.body,
        )
        st_space(15)
        st_write(
            "The official reference pack is streamtex-design. A project "
            "declares its packs in stx.toml, picks an active design system, "
            "and uses kits to bootstrap a coherent starter (e.g. "
            "slides-modern-dark, project-default, manual-default).",
            bs.body,
        )
        st_space(15)
        st_write(
            "What changed at a glance:",
            bs.body + s.bold,
        )
        with st_grid(2, gap=10):
            with st_block(bs.grid_cell):
                st_write(("Before — patterns flow", s.bold))
                st_write(
                    "- Markdown catalogue in a sibling repo "
                    "(streamtex-patterns).\n"
                    "- Manual install / sync into "
                    ".claude/custom/streamtex-patterns/.\n"
                    "- AI agent reads .md files to generate blocks.\n"
                    "- One central repo, no composition.",
                )
            with st_block(bs.grid_cell):
                st_write(("After — reuse architecture", s.bold))
                st_write(
                    "- Python packs with entry points; multi-pack natively.\n"
                    "- stx pack add ... — same UX for git / local / pypi.\n"
                    "- Components are real Python modules — importable, "
                    "diffable, testable.\n"
                    "- Local 'mypack' is the default capture destination.",
                )
