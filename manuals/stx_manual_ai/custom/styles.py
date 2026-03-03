"""AI Manual styles. Extends StxStyles with an AI/tech palette and callout containers.

Usage in blocks:
    from custom.styles import Styles as s
    st_write(s.project.colors.ai_violet, "Hello")
    st_write(s.project.titles.page_title, "AI-Powered StreamTeX")
"""

from streamtex.styles import Container, StxStyles, Style, Text


class ColorsCustom:
    """AI manual text colors."""
    ai_violet = Style("color: #8B5CF6;", "ai_violet")
    tech_blue = Style("color: #3B82F6;", "tech_blue")
    cyber_cyan = Style("color: #06B6D4;", "cyber_cyan")
    success_green = Style("color: #10B981;", "success_green")
    warning_amber = Style("color: #F59E0B;", "warning_amber")
    error_red = Style("color: #EF4444;", "error_red")


class BackgroundsCustom:
    """AI manual background colors for callout containers."""
    ai_bg = Style("background-color: rgba(139, 92, 246, 0.12);", "ai_bg")
    tech_bg = Style("background-color: rgba(59, 130, 246, 0.12);", "tech_bg")
    success_bg = Style("background-color: rgba(16, 185, 129, 0.15);", "success_bg")
    warning_bg = Style("background-color: rgba(245, 158, 11, 0.12);", "warning_bg")
    error_bg = Style("background-color: rgba(239, 68, 68, 0.15);", "error_bg")
    cyber_bg = Style("background-color: rgba(6, 182, 212, 0.12);", "cyber_bg")


class TextStylesCustom:
    """AI manual title compositions."""
    page_title = Style.create(
        ColorsCustom.ai_violet + Text.weights.bold_weight + Text.sizes.huge_size,
        "page_title"
    )
    section_title = Style.create(
        ColorsCustom.tech_blue + Text.weights.bold_weight + Text.sizes.LARGE_size,
        "section_title"
    )
    section_subtitle = Style.create(
        ColorsCustom.cyber_cyan + Text.weights.bold_weight + Text.sizes.Large_size,
        "section_subtitle"
    )
    subsection_title = Style.create(
        ColorsCustom.success_green + Text.weights.bold_weight + Text.sizes.large_size,
        "subsection_title"
    )
    feature_title = Style.create(
        ColorsCustom.ai_violet + Text.weights.bold_weight + Text.sizes.large_size,
        "feature_title"
    )
    tip_label = Style.create(
        ColorsCustom.tech_blue + Text.weights.bold_weight + Text.sizes.large_size,
        "tip_label"
    )
    warning_label = Style.create(
        ColorsCustom.warning_amber + Text.weights.bold_weight + Text.sizes.large_size,
        "warning_label"
    )
    explanation_label = Style.create(
        ColorsCustom.tech_blue + Text.weights.bold_weight + Text.sizes.large_size,
        "explanation_label"
    )
    details_label = Style.create(
        ColorsCustom.cyber_cyan + Text.weights.bold_weight + Text.sizes.large_size,
        "details_label"
    )


class ContainerStylesCustom:
    """AI manual callout container styles."""
    ai_callout = Style.create(
        BackgroundsCustom.ai_bg
        + Container.borders.solid_border
        + Style("border-color: #8B5CF6; border-width: 0 0 0 4px;", "ai_border")
        + Container.paddings.medium_padding,
        "ai_callout"
    )
    good_callout = Style.create(
        BackgroundsCustom.success_bg
        + Container.borders.solid_border
        + Style("border-color: #10B981; border-width: 0 0 0 4px;", "good_border")
        + Container.paddings.medium_padding,
        "good_callout"
    )
    bad_callout = Style.create(
        BackgroundsCustom.error_bg
        + Container.borders.solid_border
        + Style("border-color: #EF4444; border-width: 0 0 0 4px;", "bad_border")
        + Container.paddings.medium_padding,
        "bad_callout"
    )
    tip_callout = Style.create(
        BackgroundsCustom.tech_bg
        + Container.borders.solid_border
        + Style("border-color: #3B82F6; border-width: 0 0 0 4px;", "tip_border")
        + Container.paddings.medium_padding,
        "tip_callout"
    )
    note_callout = Style.create(
        BackgroundsCustom.warning_bg
        + Container.borders.solid_border
        + Style("border-color: #F59E0B; border-width: 0 0 0 4px;", "note_border")
        + Container.paddings.medium_padding,
        "note_callout"
    )
    code_box = Style.create(
        Style("background-color: rgba(139, 92, 246, 0.08);", "code_box_bg")
        + Container.borders.solid_border
        + Style("border-color: #8B5CF6; border-width: 1px;", "code_box_border")
        + Style("border-radius: 6px;", "code_box_radius")
        + Container.paddings.medium_padding
        + Container.layouts.center,
        "code_box"
    )
    explanation_box = Style.create(
        BackgroundsCustom.tech_bg
        + Container.borders.solid_border
        + Style("border-color: #3B82F6; border-width: 0 0 0 4px;", "explanation_border")
        + Style("border-radius: 4px;", "explanation_radius")
        + Container.paddings.medium_padding,
        "explanation_box"
    )
    details_box = Style.create(
        BackgroundsCustom.cyber_bg
        + Container.borders.solid_border
        + Style("border-color: #06B6D4; border-width: 0 0 0 3px;", "details_border")
        + Style("border-radius: 4px;", "details_radius")
        + Container.paddings.medium_padding,
        "details_box"
    )
    separator = Style.create(
        Style(
            "border: none; border-top: 2px solid rgba(139, 92, 246, 0.3);"
            " margin: 0 10%; height: 0;",
            "separator_line"
        ),
        "separator"
    )
    result_box = Style.create(
        BackgroundsCustom.cyber_bg
        + Container.borders.solid_border
        + Style("border-color: #06B6D4; border-width: 0 0 0 4px;", "result_border")
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
