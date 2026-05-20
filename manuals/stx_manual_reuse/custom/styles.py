"""Patterns Manual styles. Extends StxStyles with a violet/teal palette
and callout containers tuned for documentation pages.

Usage in blocks:
    from custom.styles import Styles as s
    st_write(s.project.colors.primary_violet, "Hello")
    st_write(s.project.titles.section_title, "Patterns Manual")
"""

from streamtex.styles import Container, StxStyles, Style, Text


class ColorsCustom:
    """Patterns Manual text colors."""
    primary_violet = Style("color: #a78bfa;", "primary_violet")
    accent_teal = Style("color: #2EC4B6;", "accent_teal")
    warning_red = Style("color: #E74C3C;", "warning_red")
    success_green = Style("color: #27AE60;", "success_green")
    neutral_gray = Style("color: #95A5A6;", "neutral_gray")
    highlight_amber = Style("color: #F39C12;", "highlight_amber")


class BackgroundsCustom:
    """Patterns Manual background colors for callout containers."""
    good_example_bg = Style("background-color: rgba(39, 174, 96, 0.15);", "good_example_bg")
    bad_example_bg = Style("background-color: rgba(231, 76, 60, 0.15);", "bad_example_bg")
    tip_bg = Style("background-color: rgba(167, 139, 250, 0.12);", "tip_bg")
    note_bg = Style("background-color: rgba(243, 156, 18, 0.12);", "note_bg")
    interactive_result_bg = Style(
        "background-color: rgba(46, 196, 182, 0.12);", "interactive_result_bg"
    )


class TextStylesCustom:
    """Patterns Manual title compositions."""
    course_title = Style.create(
        ColorsCustom.primary_violet + Text.weights.bold_weight + Text.sizes.LARGE_size,
        "course_title"
    )
    page_title = Style.create(
        ColorsCustom.primary_violet + Text.weights.bold_weight + Text.sizes.LARGE_size,
        "page_title"
    )
    section_title = Style.create(
        ColorsCustom.accent_teal + Text.weights.bold_weight + Text.sizes.Large_size,
        "section_title"
    )
    section_subtitle = Style.create(
        ColorsCustom.highlight_amber + Text.weights.bold_weight + Text.sizes.large_size,
        "section_subtitle"
    )
    subsection_title = Style.create(
        ColorsCustom.success_green + Text.weights.bold_weight + Text.sizes.big_size,
        "subsection_title"
    )
    feature_title = Style.create(
        ColorsCustom.success_green + Text.weights.bold_weight + Text.sizes.large_size,
        "feature_title"
    )
    body = Style.create(Text.sizes.large_size, "body")
    tip_label = Style.create(
        ColorsCustom.primary_violet + Text.weights.bold_weight + Text.sizes.large_size,
        "tip_label"
    )
    warning_label = Style.create(
        ColorsCustom.warning_red + Text.weights.bold_weight + Text.sizes.large_size,
        "warning_label"
    )
    explanation_label = Style.create(
        ColorsCustom.primary_violet + Text.weights.bold_weight + Text.sizes.large_size,
        "explanation_label"
    )
    details_label = Style.create(
        ColorsCustom.highlight_amber + Text.weights.bold_weight + Text.sizes.large_size,
        "details_label"
    )


class ContainerStylesCustom:
    """Patterns Manual callout container styles."""
    good_callout = Style.create(
        BackgroundsCustom.good_example_bg
        + Container.borders.solid_border
        + Style("border-color: #27AE60; border-width: 0 0 0 4px;", "good_border")
        + Container.paddings.medium_padding,
        "good_callout"
    )
    bad_callout = Style.create(
        BackgroundsCustom.bad_example_bg
        + Container.borders.solid_border
        + Style("border-color: #E74C3C; border-width: 0 0 0 4px;", "bad_border")
        + Container.paddings.medium_padding,
        "bad_callout"
    )
    tip_callout = Style.create(
        BackgroundsCustom.tip_bg
        + Container.borders.solid_border
        + Style("border-color: #a78bfa; border-width: 0 0 0 4px;", "tip_border")
        + Container.paddings.medium_padding,
        "tip_callout"
    )
    note_callout = Style.create(
        BackgroundsCustom.note_bg
        + Container.borders.solid_border
        + Style("border-color: #F39C12; border-width: 0 0 0 4px;", "note_border")
        + Container.paddings.medium_padding,
        "note_callout"
    )
    code_box = Style.create(
        Style("background-color: rgba(167, 139, 250, 0.08);", "code_box_bg")
        + Container.borders.solid_border
        + Style("border-color: #a78bfa; border-width: 1px;", "code_box_border")
        + Style("border-radius: 6px;", "code_box_radius")
        + Container.paddings.medium_padding,
        "code_box"
    )
    explanation_box = Style.create(
        BackgroundsCustom.tip_bg
        + Container.borders.solid_border
        + Style("border-color: #a78bfa; border-width: 0 0 0 4px;", "explanation_border")
        + Style("border-radius: 4px;", "explanation_radius")
        + Container.paddings.medium_padding,
        "explanation_box"
    )
    details_box = Style.create(
        BackgroundsCustom.note_bg
        + Container.borders.solid_border
        + Style("border-color: #F39C12; border-width: 0 0 0 3px;", "details_border")
        + Style("border-radius: 4px;", "details_radius")
        + Container.paddings.medium_padding,
        "details_box"
    )
    separator = Style.create(
        Style(
            "border: none; border-top: 2px solid rgba(167, 139, 250, 0.3);"
            " margin: 0 10%; height: 0;",
            "separator_line"
        ),
        "separator"
    )
    result_box = Style.create(
        BackgroundsCustom.interactive_result_bg
        + Container.borders.solid_border
        + Style("border-color: #2EC4B6; border-width: 0 0 0 4px;", "result_border")
        + Style("border-radius: 4px;", "result_radius")
        + Container.paddings.medium_padding,
        "result_box"
    )
    cell = Style.create(
        Container.borders.solid_border
        + Container.paddings.small_padding
        + Container.layouts.vertical_center_layout,
        "pattern_cell"
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
