"""Part 8 — Reference: Profile Comparison — feature matrix for all profiles."""

from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_details, show_explanation


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
                commands="26 (stx-block 15 + stx-ce 11)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="Course authors, documentation writers",
                focus="Full project lifecycle from init to deploy",
                extends="base profile",
                unique="init, update, audit, fix, tool, docs-lookup",
                recommended=True,
            )
        with g.cell():
            _render_profile_column(
                name="presentation",
                commands="29 (stx-block 15 + stx-ce 11 + presentation 3)",
                agents="4 (all, including Presentation Designer)",
                audience="Speakers, trainers, lecturers",
                focus="Live projection with large fonts and high contrast",
                extends="project profile",
                unique="audit --scope slide, fix --scope slide, tool survey-convert",
            )
    st_space("v", 2)

    # ── Row 2: documentation + library ────────────────────────────
    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding) as g:
        with g.cell():
            _render_profile_column(
                name="documentation",
                commands="26 (stx-block 15 + stx-ce 11)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="Technical writers, doc teams",
                focus="HTML migration and documentation workflows",
                extends="project profile",
                unique="update --migrate, update --export",
            )
        with g.cell():
            _render_profile_column(
                name="library",
                commands="2 (stx-block: test + lint)",
                agents="3 (Architect, Designer, Reviewer)",
                audience="StreamTeX library contributors",
                focus="Library development, testing, linting",
                extends="project profile",
                unique="test, lint, testing-patterns.md, architecture.md",
            )
    st_space("v", 2)

    # ── Recommendation callout ────────────────────────────────────
    st_write(bs.sub, "Which Profile Should You Choose?", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title,
                 "Start with the project profile", tag=t.div)
        st_space("v", 1)
        st_write(s.large, """\
            The project profile covers 90% of use cases. It includes
            all 15 stx-block commands plus 11 stx-ce commands and three
            agents. Switch to a specialized profile only when you
            need presentation optimization, HTML migration tools,
            or library development capabilities.
        """)
    st_space("v", 1)
    st_space("v", 1)

    # ── Child profiles (0.7.35) ───────────────────────────────────
    st_write(bs.sub, "Child Profiles: Parent, then overlay/", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        presentation, documentation and library declare
        extends = "project" in their manifest.toml. Since streamtex
        0.7.35, installing a child profile installs the parent's files
        first, then the child's overlay/ directory on top, then the
        [shared] files the child declares. Before 0.7.35 the overlay
        landed in .claude/overlay/, where Claude Code reads nothing; the
        next update or sync puts the files where they belong.
    """)
    st_space("v", 1)

    show_code("""\
        streamtex-claude/profiles/presentation/
        +-- manifest.toml        # [profile] extends = "project"
        +-- overlay/
            +-- CLAUDE.md.j2     # replaces the parent's template
            +-- commands/
            |   +-- stx-presentation/
            +-- designer/
                +-- presentation/

        # stx claude install presentation ./my-deck
        #   1. every file of profiles/project/ (+ shared references and commands)
        #   2. overlay/ copied on top, into .claude/
        #   3. the [shared] skills / agents / import-formats it declares
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # ── Project-mode declaration reference (0.7.35) ───────────────
    st_write(bs.sub, "Project Mode: the [claude] Section", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        In project mode, the profile is declared in the project's
        stx.toml instead of being chosen once at install time. Every
        key below is read by stx claude sync and checked by
        stx validate.
    """)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=s.container.paddings.small_padding
                 + s.container.borders.solid_border) as g:
        with g.cell():
            st_write(bs.feature_label, "mode")
        with g.cell():
            st_write(bs.feature_value,
                     "\"project\" turns project mode on. Absent: the classic "
                     "install / update.")
        with g.cell():
            st_write(bs.feature_label, "profile")
        with g.cell():
            st_write(bs.feature_value,
                     "Required with mode = \"project\": project, presentation, "
                     "documentation or library.")
        with g.cell():
            st_write(bs.feature_label, "include")
        with g.cell():
            st_write(bs.feature_value,
                     "Extra profiles merged in, e.g. [\"library\"]. Default [].")
        with g.cell():
            st_write(bs.feature_label, "exclude")
        with g.cell():
            st_write(bs.feature_value,
                     "Groups left out, matched against the folder or file "
                     "names under .claude/, e.g. [\"stx-ce\", \"ce\"]. "
                     "An exclude that matches nothing is reported by "
                     "stx validate. Default [].")
    st_space("v", 1)

    show_code("""\
        # stx.toml — a presentation project without the CE and PE workflows
        [claude]
        mode = "project"
        profile = "presentation"
        include = []
        exclude = ["stx-ce", "ce", "stx-pe", "pack-engineering"]
    """, language="toml", line_numbers=False)
    st_space("v", 1)

    show_details("""\
        stx claude sync records the result in .claude/stx.lock
        (format = 1): profile, include, exclude, the streamtex-claude
        revision and the sha256 of every installed file. Commit stx.toml
        and .claude/stx.lock; the installed copies are ignored by git.
        Note: stx claude update run with streamtex 0.7.34 or older does
        not know the lock and removes it as an orphan — upgrade
        streamtex on every machine that works on a project-mode project.
    """)
    st_space("v", 1)
