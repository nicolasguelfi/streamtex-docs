import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

class BlockStyles:
    """Claude profiles management styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles

def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Managing Claude Profiles",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- Profile types ---
        st_write(bs.sub, "Profile types", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Each StreamTeX project has a profile type that determines
            which Claude configuration is applied. There are three
            profile types:

            - library: for the StreamTeX library itself.
            - docs: for documentation projects (manuals).
            - project: for end-user StreamTeX applications.

            The profile type is stored in .claude/.stx-profile and
            determines which templates, skills, and commands are
            installed.
        """)
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Profile")
            with g.cell(): st_write(s.bold + s.large, "Use case")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "library")
            with g.cell():
                st_write(s.large, "StreamTeX core library development")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "docs")
            with g.cell():
                st_write(s.large, "Documentation and manual authoring")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large, "project")
            with g.cell():
                st_write(s.large, "End-user StreamTeX applications")
        st_space("v", 2)

        # --- stx claude install ---
        st_write(bs.sub, "stx claude install", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Install Claude profiles from template
stx claude install""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Reads .claude/.stx-profile to determine the project type,
            then copies the matching profile template into .claude/.
            This includes settings.json, references, skills, and
            commands. Existing files are not overwritten unless
            --force is used.
        """)
        st_space("v", 2)

        # --- stx claude list ---
        st_write(bs.sub, "stx claude list", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# List all available Claude profiles
stx claude list""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Displays all available profile templates and their
            contents. Useful for understanding what each profile
            type includes before installing.
        """)
        st_space("v", 2)

        # --- stx claude update ---
        st_write(bs.sub, "stx claude update", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Update local profiles to latest template version
stx claude update""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Compares local .claude/ files against the latest
            template and updates any files that have changed.
            Local customizations in settings.json are preserved.
            New files from the template are added automatically.
        """)
        st_space("v", 2)

        # --- stx claude diff ---
        st_write(bs.sub, "stx claude diff", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Show differences between local and template
stx claude diff""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Shows a diff between the local .claude/ directory and
            the template for the current profile type. This helps
            identify local customizations and detect when the
            template has been updated upstream.
        """)
        st_space("v", 2)

        # --- Profile storage ---
        st_write(bs.sub, "Profile storage", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Profile templates are stored in the streamtex-claude/
            repository. The stx claude commands fetch templates
            from this repository. The structure is:

            streamtex-claude/
              profiles/
                library/    — template for library projects
                docs/       — template for docs projects
                project/    — template for user projects

            Each profile directory mirrors the .claude/ structure
            and contains all files needed for that project type.
        """)
        st_space("v", 2)

        # --- Command summary ---
        st_write(bs.sub, "Command summary", toc_lvl="+1")
        st_space("v", 1)

        with st_grid(cols=2, cell_styles=(
            s.container.borders.solid_border
            + s.container.paddings.small_padding
            + s.container.layouts.vertical_center_layout
        )) as g:
            with g.cell(): st_write(s.bold + s.large, "Command")
            with g.cell(): st_write(s.bold + s.large, "Purpose")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude install")
            with g.cell():
                st_write(s.large, "Install profiles from template")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude list")
            with g.cell():
                st_write(s.large, "List available profiles")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude update")
            with g.cell():
                st_write(s.large, "Update to latest template version")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude diff")
            with g.cell():
                st_write(s.large, "Diff local vs template")
        st_space("v", 2)

        show_details("""\
            Run stx claude diff periodically to check if your
            profiles are up to date. When the template adds new
            skills or commands, stx claude update will bring
            them into your project automatically.
        """)
