"""Part 8 — Reference: Profile Comparison — feature matrix for all profiles."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation


class BlockStyles:
    """Profile comparison block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    col_header = Style(
        "background: rgba(139, 92, 246, 0.12); "
        "padding: 12px 16px; border-radius: 6px; "
        "text-align: center;",
        "profile_col_header",
    )
    col_header_recommended = Style(
        "background: rgba(16, 185, 129, 0.15); "
        "border: 2px solid #10B981; "
        "padding: 12px 16px; border-radius: 6px; "
        "text-align: center;",
        "profile_col_recommended",
    )
    profile_name = s.project.colors.ai_violet + s.bold + s.Large
    profile_name_rec = s.project.colors.success_green + s.bold + s.Large
    row_card = Style(
        "background: rgba(59, 130, 246, 0.04); "
        "border-bottom: 1px solid rgba(59, 130, 246, 0.12); "
        "padding: 10px 16px;",
        "profile_row",
    )
    feature_label = s.project.colors.tech_blue + s.bold + s.large
    feature_value = s.large


bs = BlockStyles


def _render_profile_column(name: str, commands: str, agents: str,
                           audience: str, focus: str, extends: str,
                           unique: str, recommended: bool = False):
    """Render a single profile column with all feature values."""
    header_style = (bs.col_header_recommended
                    if recommended else bs.col_header)
    name_style = bs.profile_name_rec if recommended else bs.profile_name
    with st_block(header_style):
        st_write(name_style, name, tag=t.div)
        if recommended:
            st_space("v", 0.3)
            st_write(s.project.colors.success_green + s.bold + s.medium,
                     "RECOMMENDED", tag=t.div)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Commands: "),
                     (bs.feature_value, commands))
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Agents: "),
                     (bs.feature_value, agents))
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Audience: "),
                     (bs.feature_value, audience))
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Key focus: "),
                     (bs.feature_value, focus))
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Extends: "),
                     (bs.feature_value, extends))
        with l.item():
            st_write(s.large,
                     (bs.feature_label, "Unique: "),
                     (bs.feature_value, unique))


def build():
    """Render the profile comparison matrix."""
    st_space("v", 1)
    st_write(bs.heading, "Reference: Profile Comparison",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        StreamTeX provides four AI profiles, each tailored to a
        specific workflow. The project profile is recommended for
        most users. Compare features below to choose the right one.
    """)
    st_space("v", 2)

    # ── Row 1: project + presentation ─────────────────────────────
    st_write(bs.sub, "Profile Matrix", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_profile_column(
                name="project",
                commands="20 (project + designer + migration + developer)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="Course authors, documentation writers",
                focus="Full project lifecycle from init to deploy",
                extends="base profile",
                unique="project-init, project-customize, course-generate",
                recommended=True,
            )
        with g.cell():
            _render_profile_column(
                name="presentation",
                commands="15 (project + designer + presentation)",
                agents="4 (all, including Presentation Designer)",
                audience="Speakers, trainers, lecturers",
                focus="Live projection with large fonts and high contrast",
                extends="project profile",
                unique="presentation-audit, presentation-fix, survey-convert",
            )
    st_space("v", 2)

    # ── Row 2: documentation + library ────────────────────────────
    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_profile_column(
                name="documentation",
                commands="17 (project + designer + migration)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="Technical writers, doc teams",
                focus="HTML migration and documentation workflows",
                extends="project profile",
                unique="html-migrate, html-convert-batch, html-export",
            )
        with g.cell():
            _render_profile_column(
                name="library",
                commands="15 (project + designer + developer)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="StreamTeX library contributors",
                focus="Library development, testing, deployment",
                extends="project profile",
                unique="deploy, testing-patterns.md, architecture.md",
            )
    st_space("v", 2)

    # ── Recommendation callout ────────────────────────────────────
    st_write(bs.sub, "Which Profile Should You Choose?", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title,
                 "Start with the project profile", tag=t.div)
        st_space("v", 1)
        st_write(s.large, textwrap.dedent("""\
            The project profile covers 90% of use cases. It includes
            all project, designer, and developer commands plus three
            agents. Switch to a specialized profile only when you
            need presentation optimization, HTML migration tools,
            or library development capabilities.
        """))
    st_space("v", 1)
