"""Developer manual styles. Extends StxStyles with a developer-focused palette and callout containers.

Usage in blocks:
    from custom.styles import Styles as s
    st_write(s.project.colors.dev_green, "Hello")
    st_write(s.project.titles.section_title, "Architecture")
"""

from streamtex.styles import Container, StxStyles, Style, Text


class ColorsCustom:
    """Developer manual text colors."""
    dev_green = Style("color: #27AE60;", "dev_green")
    dev_cyan = Style("color: #00BCD4;", "dev_cyan")
    dev_orange = Style("color: #FF9800;", "dev_orange")
    dev_purple = Style("color: #9C27B0;", "dev_purple")
    neutral_gray = Style("color: #95A5A6;", "neutral_gray")
    dev_blue = Style("color: #2196F3;", "dev_blue")


class BackgroundsCustom:
    """Developer manual background colors for callout containers."""
    info_bg = Style("background-color: rgba(0, 188, 212, 0.12);", "info_bg")
    warning_bg = Style("background-color: rgba(255, 152, 0, 0.12);", "warning_bg")
    success_bg = Style("background-color: rgba(39, 174, 96, 0.15);", "success_bg")
    code_bg = Style("background-color: rgba(0, 188, 212, 0.08);", "code_bg")


class TextStylesCustom:
    """Developer manual title compositions."""
    course_title = Style.create(
        ColorsCustom.dev_green + Text.weights.bold_weight + Text.sizes.huge_size,
        "course_title"
    )
    page_title = Style.create(
        ColorsCustom.dev_green + Text.weights.bold_weight + Text.sizes.huge_size,
        "page_title"
    )
    section_title = Style.create(
        ColorsCustom.dev_cyan + Text.weights.bold_weight + Text.sizes.LARGE_size,
        "section_title"
    )
    section_subtitle = Style.create(
        ColorsCustom.dev_orange + Text.weights.bold_weight + Text.sizes.Large_size,
        "section_subtitle"
    )
    subsection_title = Style.create(
        ColorsCustom.dev_green + Text.weights.bold_weight + Text.sizes.large_size,
        "subsection_title"
    )
    tip_label = Style.create(
        ColorsCustom.dev_cyan + Text.weights.bold_weight + Text.sizes.large_size,
        "tip_label"
    )
    warning_label = Style.create(
        ColorsCustom.dev_orange + Text.weights.bold_weight + Text.sizes.large_size,
        "warning_label"
    )
    explanation_label = Style.create(
        ColorsCustom.dev_cyan + Text.weights.bold_weight + Text.sizes.large_size,
        "explanation_label"
    )
    details_label = Style.create(
        ColorsCustom.dev_orange + Text.weights.bold_weight + Text.sizes.large_size,
        "details_label"
    )


class ContainerStylesCustom:
    """Developer manual callout container styles."""
    code_box = Style.create(
        BackgroundsCustom.code_bg
        + Container.borders.solid_border
        + Style("border-color: #00BCD4; border-width: 1px;", "code_box_border")
        + Style("border-radius: 6px;", "code_box_radius")
        + Container.paddings.medium_padding
        + Container.layouts.center,
        "code_box"
    )
    explanation_box = Style.create(
        BackgroundsCustom.info_bg
        + Container.borders.solid_border
        + Style("border-color: #00BCD4; border-width: 0 0 0 4px;", "explanation_border")
        + Style("border-radius: 4px;", "explanation_radius")
        + Container.paddings.medium_padding,
        "explanation_box"
    )
    details_box = Style.create(
        BackgroundsCustom.warning_bg
        + Container.borders.solid_border
        + Style("border-color: #FF9800; border-width: 0 0 0 3px;", "details_border")
        + Style("border-radius: 4px;", "details_radius")
        + Container.paddings.medium_padding,
        "details_box"
    )
    tip_callout = Style.create(
        BackgroundsCustom.info_bg
        + Container.borders.solid_border
        + Style("border-color: #00BCD4; border-width: 0 0 0 4px;", "tip_border")
        + Container.paddings.medium_padding,
        "tip_callout"
    )
    note_callout = Style.create(
        BackgroundsCustom.warning_bg
        + Container.borders.solid_border
        + Style("border-color: #FF9800; border-width: 0 0 0 4px;", "note_border")
        + Container.paddings.medium_padding,
        "note_callout"
    )
    warning_callout = Style.create(
        Style("background-color: rgba(156, 39, 176, 0.12);", "warning_callout_bg")
        + Container.borders.solid_border
        + Style("border-color: #9C27B0; border-width: 0 0 0 4px;", "warning_border")
        + Container.paddings.medium_padding,
        "warning_callout"
    )
    separator = Style.create(
        Style(
            "border: none; border-top: 2px solid rgba(0, 188, 212, 0.3);"
            " margin: 0 10%; height: 0;",
            "separator_line"
        ),
        "separator"
    )
    result_box = Style.create(
        BackgroundsCustom.success_bg
        + Container.borders.solid_border
        + Style("border-color: #27AE60; border-width: 0 0 0 4px;", "result_border")
        + Style("border-radius: 4px;", "result_radius")
        + Container.paddings.medium_padding,
        "result_box"
    )


class Custom:
    """Aggregation class for all project-specific styles."""
    colors = ColorsCustom
    backgrounds = BackgroundsCustom
    titles = TextStylesCustom
    containers = ContainerStylesCustom


class Styles(StxStyles):
    """Main Styles class — inherits all StreamTeX styles + project-specific ones."""
    project = Custom
