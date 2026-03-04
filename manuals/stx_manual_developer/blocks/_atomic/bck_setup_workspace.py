from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details

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

        show_explanation("""\
            A workspace groups the StreamTeX library, documentation,
            and Claude profiles so you can develop and test them
            side by side. The stx CLI provides commands to create,
            clone, link, and upgrade workspaces.
        """)
        st_space("v", 2)

        # --- 2. stx workspace init ---
        st_write(bs.sub, "stx workspace init", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Creates a new workspace with stx.toml and a projects/
            directory. Use --preset to control which repos
            are declared (default: standard).
        """)
        st_space("v", 1)

        show_code("""\
# Create a standard workspace (docs + claude)
stx workspace init .

# Developer workspace (all 3 repos)
stx workspace init . --preset developer

# Creates:
#   stx.toml    — workspace configuration
#   projects/   — directory for user projects""", language="bash")
        st_space("v", 2)

        # --- 3. stx workspace clone ---
        st_write(bs.sub, "stx workspace clone", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Clones all repos declared in stx.toml. The number of
            repos depends on the workspace preset. Already-cloned
            repos are skipped. Shared commands (like /stx-guide)
            are also installed globally to ~/.claude/commands/.
        """)
        st_space("v", 1)

        show_code("""\
# Clone repos declared in stx.toml
# Also installs shared commands globally (~/.claude/commands/)
stx workspace clone""", language="bash")
        st_space("v", 2)

        # --- 4. stx workspace link ---
        st_write(bs.sub, "stx workspace link", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Runs uv sync in docs and project repos for editable
            installs. Only needed with the developer preset when
            you want library changes reflected immediately.
        """)
        st_space("v", 1)

        show_code("""\
# Developer preset: configure editable installs
stx workspace link""", language="bash")
        st_space("v", 2)

        # --- 5. stx workspace upgrade ---
        st_write(bs.sub, "stx workspace upgrade", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Upgrade a workspace to a higher preset. Adds missing
            repo sections to stx.toml. Run stx workspace clone
            after to fetch the new repos.
        """)
        st_space("v", 1)

        show_code("""\
# Upgrade from standard to developer
stx workspace upgrade developer
stx workspace clone""", language="bash")
        st_space("v", 2)

        # --- 6. stx workspace status and sync ---
        st_write(bs.sub, "stx workspace status and sync", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Check the git state of all repos and synchronize
            dependencies across the workspace.
        """)
        st_space("v", 1)

        show_code("""\
# Check workspace state
stx workspace status

# Run uv sync in all repos
stx workspace sync""", language="bash")
        st_space("v", 2)

        # --- 7. Command summary ---
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
                st_write(s.large, "Clone repos + install global commands")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace link")
            with g.cell():
                st_write(s.large, "Editable installs (developer)")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace upgrade")
            with g.cell():
                st_write(s.large, "Upgrade to a higher preset")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace status")
            with g.cell():
                st_write(s.large, "Check workspace state")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx workspace sync")
            with g.cell():
                st_write(s.large, "Run uv sync in all repos")
        st_space("v", 2)

        show_details("""\
            The workspace presets are: basic (no repos), user
            (claude only), standard (docs + claude), and developer
            (all 3 repos). The developer preset lets you work with
            streamtex-docs alongside the streamtex library for live
            testing via editable installs.

            Use stx workspace status regularly to check for drift
            between linked projects.
        """)
