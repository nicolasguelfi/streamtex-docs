"""Live gallery — the 3 design systems shipped by `streamtex_design`.

Renders the same component (callout) three times, each with a different
design system instance, so a reader sees how the bundles drive the
visual without touching the component code.
"""

from streamtex import *
from custom.styles import Styles as s
from streamtex_design.design_systems.default import DesignSystem as DefaultDS
from streamtex_design.design_systems.modern_dark import DesignSystem as DarkDS
from streamtex_design.design_systems.modern_light import DesignSystem as LightDS
# streamtex_design's components __init__ is intentionally lean — import
# each public function from its module.
from streamtex_design.components.callout import callout
from streamtex_design.components.stat_hero import stat_hero
from streamtex_design.components.takeaways import takeaways


class BlockStyles:
    heading = s.project.titles.section_title + s.center_txt
    section = s.bold + s.large
    label = s.bold + s.medium
    body = s.large
    frame = (
        s.container.borders.solid_border
        + s.container.paddings.small_padding
        + s.container.margins.small_margin
    )


bs = BlockStyles

DESIGN_SYSTEMS = [
    ("default", DefaultDS()),
    ("modern_dark", DarkDS()),
    ("modern_light", LightDS()),
]


def _showcase(label, render):
    """Render the same `render(ds)` once per design system, side-labeled."""
    st_write((bs.label, label))
    for name, ds in DESIGN_SYSTEMS:
        st_write((s.italic + s.medium, f"design_system = {name}"))
        with st_block(bs.frame):
            render(ds)
        st_space(6)
    st_space(15)


def build():
    """Render the 3 design systems side-by-side via 3 sample components."""
    with st_block(s.center_txt):
        st_write((bs.heading, "Design systems — 3 themes"), toc_lvl="1")
        st_space(15)
        st_write(
            bs.body,
            "The same component (`callout`, `stat_hero`, `takeaways`) is "
            "rendered three times below, with `default`, `modern_dark`, and "
            "`modern_light` design systems. The component code is identical; "
            "only the bundles change. This is the contract D6 — lib +components are agnostic of the visual choice.",
        )

    st_space(20)
    st_write((bs.section, "1 — callout(variant='info')"))
    st_space(10)
    _showcase(
        "callout — info variant across 3 design systems",
        lambda ds: callout(
            design_system=ds,
            variant="info",
            title="Knowledge capitalisation",
            body="Same component, three palettes.",
        ),
    )

    st_write((bs.section, "2 — stat_hero(value, body)"))
    st_space(10)
    _showcase(
        "stat_hero across 3 design systems",
        lambda ds: stat_hero(
            design_system=ds,
            value="100 %",
            body="bundles delegated to the design system, never inlined.",
        ),
    )

    st_write((bs.section, "3 — takeaways(items, numbered=True)"))
    st_space(10)
    _showcase(
        "takeaways across 3 design systems",
        lambda ds: takeaways(
            design_system=ds,
            lead="Why this matters",
            items=[
                "A consumer project picks ONE design system via [design_system] use=... in stx.toml.",
                "Switching theme is `stx ds switch <name>` — no block rewrite.",
                "New themes ship in new packs; resolution.prefer arbitrates.",
            ],
            numbered=True,
        ),
    )
