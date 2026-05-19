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
        st_write((bs.heading, "Three layers"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "The architecture separates contracts (the library) from "
            "catalogues (the packs) from active configuration (the consumer "
            "project). Each layer has its own release cadence and can be "
            "evolved independently.",
        )
        st_space(20)

        with st_grid(3, gap=10):
            with st_block(bs.layer):
                st_write((bs.title, "Layer 1 — Library"))
                st_write(s.bold, "streamtex (PyPI)")
                st_write(
                    bs.body,
                    "Contracts only. DesignSystemProtocol, ComponentMeta, "
                    "KitManifest, PackManifest, validate_* functions, "
                    "discover_packs.",
                )
                st_write(
                    bs.body + s.italic,
                    "Cadence: regular patch releases on the lib's "
                    "current minor; the API of this layer is contract-stable.",
                )
            with st_block(bs.layer):
                st_write((bs.title, "Layer 2 — Packs"))
                st_write(s.bold, "streamtex-design, mypack, ...")
                st_write(
                    bs.body,
                    "Catalogues. Components, design systems, kits. "
                    "Distributed via git, local path, or PyPI. Composable: a "
                    "project can declare N packs.",
                )
                st_write(
                    bs.body + s.italic,
                    "Cadence: each pack owns its release rhythm.",
                )
            with st_block(bs.layer):
                st_write((bs.title, "Layer 3 — Consumer project"))
                st_write(s.bold, "your project + stx.toml")
                st_write(
                    bs.body,
                    "Active configuration. Declares packs, design system, "
                    "kit, resolution preference. Hosts the local primary "
                    "pack (mypack) for CE capture.",
                )
                st_write(
                    bs.body + s.italic,
                    "Cadence: whenever the user codes.",
                )

        st_space(20)
        st_write(
            bs.body,
            "Decision D6 (PLAN §13) — the library exposes contracts only. "
            "Catalogues never live inside the library; packs never depend "
            "on each other; the consumer project never modifies the library "
            "or the packs in place.",
        )
