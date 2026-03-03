import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
import textwrap


class BlockStyles:
    """Workspace management styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Workspace Management with stx CLI",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

        # --- 1. What is a workspace ---
        st_write(bs.sub, "What is a workspace?", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            A workspace groups the StreamTeX library and its documentation
            projects so you can develop and test them side by side.
            The stx CLI provides commands to create, clone,
            and synchronize workspaces.
        """))
        st_space("v", 2)

        # --- 2. stx workspace init ---
        st_write(bs.sub, "stx workspace init", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Creates a brand-new workspace directory with the
            standard folder structure and configuration files.
        """))
        st_space("v", 1)

        show_code("""\
# Create a new workspace in the current directory
stx workspace init

# Creates:
#   workspace.toml   — workspace configuration
#   projects/        — directory for linked projects
#   .stx/            — workspace metadata""", language="bash")
        st_space("v", 2)

        # --- 3. stx workspace clone ---
        st_write(bs.sub, "stx workspace clone", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Clones an existing workspace from a remote repository
            and sets up all project links automatically.
        """))
        st_space("v", 1)

        show_code("""\
# Clone an existing workspace
stx workspace clone https://github.com/org/my-workspace.git""", language="bash")
        st_space("v", 2)

        # --- 4. stx workspace link ---
        st_write(bs.sub, "stx workspace link", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Links a project into the workspace for development.
            This is how you connect streamtex-docs alongside
            the streamtex library for live testing.
        """))
        st_space("v", 1)

        show_code("""\
# Link the docs project into the workspace
stx workspace link ../streamtex-docs

# Link creates a symlink so changes are reflected immediately""", language="bash")
        st_space("v", 2)

        # --- 5. stx workspace status and sync ---
        st_write(bs.sub, "stx workspace status and sync", toc_lvl="+1")
        st_space("v", 1)

        show_explanation(textwrap.dedent("""\
            Check the state of all linked projects and
            synchronize changes across the workspace.
        """))
        st_space("v", 1)

        show_code("""\
# Check workspace state
stx workspace status

# Synchronize changes across linked projects
stx workspace sync""", language="bash")
        st_space("v", 2)

        # --- 6. Command summary ---
        st_write(bs.sub, "Command reference", toc_lvl="+1")
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
                         "stx workspace init")
            with g.cell():
                st_write(s.large, "Create a new workspace")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace clone")
            with g.cell():
                st_write(s.large, "Clone an existing workspace")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace link")
            with g.cell():
                st_write(s.large, "Link a project for development")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace status")
            with g.cell():
                st_write(s.large, "Check workspace state")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace sync")
            with g.cell():
                st_write(s.large, "Synchronize changes")
        st_space("v", 2)

        show_details(textwrap.dedent("""\
            The workspace system lets you work with streamtex-docs
            alongside the streamtex library for live testing.

            Edit the library code, then immediately see the effect
            in your documentation manuals without reinstalling.

            Use stx workspace status regularly to check for drift
            between linked projects.
        """))
