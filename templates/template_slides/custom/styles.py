"""Presentation styles — optimised for live projection at 10-20m distance.

Usage in blocks:
    from custom.styles import Styles as s
    st_write(s.project.titles.slide_title, "My Title")
    st_write(s.project.colors.primary, "Highlighted text")

Font size hierarchy (projection-safe):
    slide_title   — 96pt (Huge)   — one per slide
    section_title — 80pt (huge)   — section headers
    subtitle      — 48pt (Large)  — slide subtitles
    body          — 48pt (Large)  — all readable content
    caption       — 32pt (large)  — sources, attributions only
"""

from streamtex.styles import Container, StxStyles, Style, Text


class ColorsCustom:
    """Presentation text colors — high contrast only."""
    primary = Style("color: #7AB8F5;", "primary")
    accent = Style("color: #2EC4B6;", "accent")
    highlight = Style("color: #F39C12;", "highlight")
    success = Style("color: #27AE60;", "success")
    muted = Style("color: #95A5A6;", "muted")


class BackgroundsCustom:
    """Presentation backgrounds."""
    callout_bg = Style("background-color: rgba(122, 184, 245, 0.12);", "callout_bg")


class TextStylesCustom:
    """Presentation title hierarchy — large fonts for projection."""
    slide_title = Style.create(
        ColorsCustom.primary + Text.weights.bold_weight + Text.sizes.Huge_size,
        "slide_title"
    )
    section_title = Style.create(
        ColorsCustom.accent + Text.weights.bold_weight + Text.sizes.huge_size,
        "section_title"
    )
    subtitle = Style.create(
        ColorsCustom.highlight + Text.weights.bold_weight + Text.sizes.Large_size,
        "subtitle"
    )
    body = Style.create(
        Text.sizes.Large_size,
        "body"
    )
    body_accent = Style.create(
        ColorsCustom.accent + Text.weights.bold_weight + Text.sizes.Large_size,
        "body_accent"
    )
    caption = Style.create(
        ColorsCustom.muted + Text.sizes.large_size,
        "caption"
    )


class ContainerStylesCustom:
    """Presentation containers."""
    callout = Style.create(
        BackgroundsCustom.callout_bg
        + Container.borders.solid_border
        + Style("border-color: #7AB8F5; border-width: 0 0 0 4px;", "callout_border")
        + Container.paddings.medium_padding,
        "callout"
    )

    # Responsive grid presets
    responsive_2col = "repeat(auto-fit, minmax(350px, 1fr))"

    # Layout gaps
    gap_32 = Style("gap: 32px;", "gap_32")
    gap_24 = Style("gap: 24px;", "gap_24")


class Custom:
    """Aggregation class for all presentation-specific styles."""
    colors = ColorsCustom
    backgrounds = BackgroundsCustom
    titles = TextStylesCustom
    containers = ContainerStylesCustom


class Styles(StxStyles):
    """Main Styles class — inherits all StreamTeX styles + presentation overrides."""
    project = Custom
