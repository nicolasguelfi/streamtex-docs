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
from streamtex_design.components import callout, stat_hero, takeaways


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
    st_write((label, bs.label))
    for name, ds in DESIGN_SYSTEMS:
        st_write((f"design_system = {name}", s.italic + s.medium))
        with st_block(bs.frame):
            render(ds)
        st_space(6)
    st_space(15)


def build():
    """Render the 3 design systems side-by-side via 3 sample components."""
    with st_block(s.center_txt):
        st_write(("Design systems — 3 themes", bs.heading))
        st_space(15)
        st_write(
            "The same component (`callout`, `stat_hero`, `takeaways`) is "
            "rendered three times below, with `default`, `modern_dark`, and "
            "`modern_light` design systems. The component code is identical; "
            "only the bundles change. This is the contract D6 — lib +components are agnostic of the visual choice.",
            bs.body,
        )

    st_space(20)
    st_write(("1 — callout(variant='info')", bs.section))
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

    st_write(("2 — stat_hero(value, body)", bs.section))
    st_space(10)
    _showcase(
        "stat_hero across 3 design systems",
        lambda ds: stat_hero(
            design_system=ds,
            value="100 %",
            body="bundles delegated to the design system, never inlined.",
        ),
    )

    st_write(("3 — takeaways(items, numbered=True)", bs.section))
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
