"""Part 4 — Agent: Presentation Designer — specialist for live projection."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_details


class BlockStyles:
    """Presentation Designer block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Comparison card styles
    standard_card = Style(
        "background: rgba(59, 130, 246, 0.08); "
        "border: 1px solid rgba(59, 130, 246, 0.25); "
        "border-radius: 8px; padding: 20px;",
        "standard_card",
    )
    presentation_card = Style(
        "background: rgba(139, 92, 246, 0.08); "
        "border: 1px solid rgba(139, 92, 246, 0.25); "
        "border-radius: 8px; padding: 20px;",
        "presentation_card",
    )
    card_title = s.bold + s.Large
    card_value_std = s.project.colors.tech_blue + s.bold + s.large
    card_value_pres = s.project.colors.ai_violet + s.bold + s.large
    card_label = s.large

    # Comparison rule row
    rule_box = Style(
        "background: rgba(6, 182, 212, 0.06); "
        "border-radius: 6px; padding: 12px 16px;",
        "rule_row",
    )


bs = BlockStyles


def build():
    """Render the Presentation Designer agent section."""
    st_space("v", 1)
    st_write(bs.heading, "Agent: Presentation Designer",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        The Presentation Designer is a specialist agent for creating
        slides meant for live projection at 10 to 20 meters viewing
        distance. It is only available in the "presentation" profile
        and applies stricter formatting rules than the standard
        Slide Designer.
    """))
    st_space("v", 2)

    # ── Special rules ──────────────────────────────────────────────
    st_write(bs.sub, "Presentation Rules vs Standard",
             toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.standard_card):
                st_write(
                    s.project.colors.tech_blue + s.bold + s.Large,
                    "Standard Designer",
                    tag=t.div,
                )
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(
                        s.large,
                        (s.bold, "32pt "),
                        "body text",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Full sentences "),
                        "allowed",
                    )
                    st_write(
                        s.large,
                        (s.bold, "~45 chars "),
                        "per line",
                    )
                    st_write(
                        s.large,
                        "Standard color contrast",
                    )
                    st_write(
                        s.large,
                        "Multiple items per section",
                    )

        with g.cell():
            with st_block(bs.presentation_card):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.Large,
                    "Presentation Designer",
                    tag=t.div,
                )
                st_space("v", 1)
                with st_list(list_type="ul"):
                    st_write(
                        s.large,
                        (s.bold, "48pt+ "),
                        "body text",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Keywords only "),
                        "(5-7 words per bullet)",
                    )
                    st_write(
                        s.large,
                        (s.bold, "96pt+ "),
                        "titles",
                    )
                    st_write(
                        s.large,
                        (s.bold, "High contrast "),
                        "colors enforced",
                    )
                    st_write(
                        s.large,
                        (s.bold, "Fewer items "),
                        "per slide",
                    )
    st_space("v", 2)

    # ── When to use ────────────────────────────────────────────────
    st_write(bs.sub, "When to Use", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(
        cols=3, cell_styles=s.container.paddings.small_padding,
    ) as g:
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Amphitheater",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Large venue with 50+ seats.
                    Audience far from screen.
                    Maximum readability needed.
                """))
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Conference",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Professional setting.
                    Projected on large screen.
                    Keywords beat paragraphs.
                """))
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.large,
                    "Classroom",
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    Teaching environment.
                    Students take notes.
                    Concise points preferred.
                """))
    st_space("v", 2)

    # ── Side-by-side comparison ────────────────────────────────────
    st_write(bs.sub, "Same Content, Different Output",
             toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.standard_card):
                st_write(
                    s.project.colors.tech_blue + s.bold + s.Large,
                    "Standard Slide",
                    tag=t.div,
                )
                st_space("v", 1)
                st_write(
                    s.large,
                    (s.bold, "Variables in Python"),
                    tag=t.div,
                )
                st_space("v", 0.5)
                st_write(s.large, textwrap.dedent("""\
                    A variable is a named reference to a value
                    stored in memory. You create a variable by
                    assigning a value with the = operator.
                    Python infers the type automatically.
                """))

        with g.cell():
            with st_block(bs.presentation_card):
                st_write(
                    s.project.colors.ai_violet + s.bold + s.Large,
                    "Presentation Slide",
                    tag=t.div,
                )
                st_space("v", 1)
                st_write(
                    s.Large + s.bold,
                    "Variables in Python",
                    tag=t.div,
                )
                st_space("v", 0.5)
                with st_list(list_type="ul"):
                    st_write(s.Large, "Named reference to a value")
                    st_write(s.Large, "Created with = operator")
                    st_write(s.Large, "Type inferred automatically")
    st_space("v", 2)

    show_details(textwrap.dedent("""\
        The Presentation Designer is only available when the
        "presentation" profile is active. Switch profiles with
        the stx CLI before invoking the agent. All standard
        designer commands still work — the presentation agent
        simply applies stricter formatting constraints on top
        of the base design rules.
    """))
    st_space("v", 1)
