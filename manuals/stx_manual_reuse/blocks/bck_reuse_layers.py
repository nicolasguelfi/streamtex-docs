"""3-layer architecture diagram — uses column_features for the 3 layer cells."""

from streamtex import st_space, st_write
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem
from streamtex_manuals.components.column_features import column_features


DS = DesignSystem()


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    body = s.large + s.center_txt


bs = BlockStyles


def build():
    """Render the 3-layer architecture: lib → packs → consumer projects."""
    st_write((bs.heading, "Three layers"), toc_lvl="1", tag=t.div)
    st_space(10)
    st_write(
        bs.body,
        "The architecture separates contracts (the library) from "
        "catalogues (the packs) from active configuration (the consumer "
        "project). Each layer has its own release cadence and can be "
        "evolved independently.",
        tag=t.div,
    )
    st_space(20)

    column_features(
        design_system=DS,
        columns=[
            (
                "Layer 1 — Library",
                "info",
                [
                    "streamtex (PyPI) ships contracts only.",
                    "DesignSystemProtocol, ComponentMeta, "
                    "KitManifest, PackManifest.",
                    "validate_* functions, discover_packs.",
                    "Cadence: regular patch releases on the current "
                    "minor; the API of this layer is contract-stable.",
                ],
            ),
            (
                "Layer 2 — Packs",
                "success",
                [
                    "streamtex-pack-design, streamtex-pack-manuals, mypack, ...",
                    "Catalogues: components, design systems, kits.",
                    "Distributed via git, local path, or PyPI.",
                    "Composable: a project can declare N packs.",
                    "Cadence: each pack owns its release rhythm.",
                ],
            ),
            (
                "Layer 3 — Consumer project",
                "warn",
                [
                    "your project + stx.toml.",
                    "Declares packs, design system, kit, resolution "
                    "preference.",
                    "Hosts the local primary pack (mypack) for CE "
                    "capture.",
                    "Cadence: whenever the user codes.",
                ],
            ),
        ],
        min_col_width="280px",
    )

    st_space(20)
    st_write(
        bs.body,
        "The library exposes contracts only. Catalogues never live "
        "inside the library; packs never depend on each other; the "
        "consumer project never modifies the library or the packs in "
        "place.",
        tag=t.div,
    )
