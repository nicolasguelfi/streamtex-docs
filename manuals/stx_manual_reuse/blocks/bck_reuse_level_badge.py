"""Welcome page — uses `level_badge_hero` from streamtex-manuals.

The reuse manual is the showcase of the reuse architecture: its cover
page is rendered by importing a pack component, not by inlining the
gradient + level box CSS in the block. The pack ships the recurring
"manual cover hero" pattern shared by every documentation manual.
"""

from streamtex_design.design_systems.default import DesignSystem
from streamtex_manuals.components.level_badge_hero import level_badge_hero


_LOGO = "https://media.githubusercontent.com/media/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png"

DS = DesignSystem()


def build():
    """Render the reuse manual cover via the shared `level_badge_hero`."""
    level_badge_hero(
        design_system=DS,
        manual_title="StreamTeX Reuse Architecture",
        manual_subtitle="Packs, components, design systems, kits — "
                        "and Pack Engineering",
        level_label="Reuse Level",
        level_headline="The streamtex reuse layer, end-to-end",
        level_body=(
            "This manual covers the reuse architecture of streamtex: "
            "how reusable artefacts (components, design systems, kits) "
            "ship inside Python packs, how projects consume them, and "
            "how Pack Engineering orchestrates their full lifecycle "
            "across N projects."
        ),
        bullets=[
            "Concepts: packs, components, design systems, kits",
            "Authoring: scaffold components, design systems, kits, "
            "and CLI templates",
            "Pack Engineering (/stx-pe): bootstrap, specialize, refine, "
            "audit, adopt, publish",
            "Self-demonstration: this manual consumes streamtex-design "
            "and renders every component for real",
        ],
        accent_color="#2ecc71",
        gradient_start="#2ecc71",
        gradient_end="#27ae60",
        logo_uri=_LOGO,
        support_url="https://github.com/sponsors/nicolasguelfi",
    )
