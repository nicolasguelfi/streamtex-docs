"""3-layer architecture diagram (PLAN §3)."""

from streamtex import *
from custom.styles import Styles as s


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large
    layer = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.center_txt
    )
    title = s.bold + s.large


bs = BlockStyles


def build():
    """Render the 3-layer architecture: lib → packs → consumer projects."""
    with st_block(s.center_txt):
        st_write(("Three layers", bs.heading))
        st_space(15)
        st_write(
            "The architecture separates contracts (the library) from "
            "catalogues (the packs) from active configuration (the consumer "
            "project). Each layer has its own release cadence and can be "
            "evolved independently.",
            bs.body,
        )
        st_space(20)

        with st_grid(3, gap=10):
            with st_block(bs.layer):
                st_write(("Layer 1 — Library", bs.title))
                st_write("streamtex (PyPI)", s.bold)
                st_write(
                    "Contracts only. DesignSystemProtocol, ComponentMeta, "
                    "KitManifest, PackManifest, validate_* functions, "
                    "discover_packs.",
                    bs.body,
                )
                st_write(
                    "Cadence: ~weekly patch releases on 0.6.x; 0.7.0 is the "
                    "consolidation milestone.",
                    bs.body + s.italic,
                )
            with st_block(bs.layer):
                st_write(("Layer 2 — Packs", bs.title))
                st_write("streamtex-design, mypack, ...", s.bold)
                st_write(
                    "Catalogues. Components, design systems, kits. "
                    "Distributed via git, local path, or PyPI. Composable: a "
                    "project can declare N packs.",
                    bs.body,
                )
                st_write(
                    "Cadence: each pack owns its release rhythm.",
                    bs.body + s.italic,
                )
            with st_block(bs.layer):
                st_write(("Layer 3 — Consumer project", bs.title))
                st_write("your project + stx.toml", s.bold)
                st_write(
                    "Active configuration. Declares packs, design system, "
                    "kit, resolution preference. Hosts the local primary "
                    "pack (mypack) for CE capture.",
                    bs.body,
                )
                st_write(
                    "Cadence: whenever the user codes.",
                    bs.body + s.italic,
                )

        st_space(20)
        st_write(
            "Decision D6 (PLAN §13) — the library exposes contracts only. "
            "Catalogues never live inside the library; packs never depend "
            "on each other; the consumer project never modifies the library "
            "or the packs in place.",
            bs.body,
        )
