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
            install, and update workspaces.
        """)
        st_space("v", 2)

        # --- 2. stx install ---
        st_write(bs.sub, "stx install", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Creates a new workspace with stx.toml and a projects/
            directory, or upgrades an existing workspace to a
            higher preset. Use --preset to control which repos
            are declared (default: standard).
        """)
        st_space("v", 1)

        show_code("""\
# Create a standard workspace (docs + claude) — default
stx install

# Other presets
stx install --preset basic       # no repos
stx install --preset user        # claude only
stx install --preset standard    # docs + claude (default)
stx install --preset power       # developer + extras
stx install --preset developer   # all 3 repos

# Create a project during install
stx install --project myapp
stx install --project myapp --template presentation

# Template options: project (default), presentation, collection, course

# Creates:
#   stx.toml    — workspace configuration
#   projects/   — directory for user projects""", language="bash")
        st_space("v", 2)

        # --- 3. stx update ---
        st_write(bs.sub, "stx update", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            The single command for all workspace operations: clone
            repos, pull latest changes, sync dependencies, install
            pre-commit hooks, update Claude profiles, and install
            global commands. Use it after install and whenever you
            need to update.
        """)
        st_space("v", 1)

        show_code("""\
# Clone + pull + sync + hooks + profiles + global commands
stx update

# Fine-grained control
stx update --skip-sync      # skip uv sync
stx update --skip-profiles  # skip Claude profile update
stx update --dry-run        # show steps without executing
stx update --repair         # fix broken venv, missing __init__.py""", language="bash")
        st_space("v", 2)

        # --- 4. stx install --preset (upgrade) ---
        st_write(bs.sub, "Upgrading a workspace preset", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Upgrade a workspace to a higher preset. Adds missing
            repo sections to stx.toml. Run stx update after to
            fetch the new repos.
        """)
        st_space("v", 1)

        show_code("""\
# Upgrade from standard to developer
stx install --preset developer
stx update""", language="bash")
        st_space("v", 2)

        # --- 5. stx status ---
        st_write(bs.sub, "stx status", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Check the git state of all repos in the workspace.
        """)
        st_space("v", 1)

        show_code("""\
# Check workspace state
stx status""", language="bash")
        st_space("v", 2)

        # --- 6. stx project upgrade ---
        st_write(bs.sub, "stx project upgrade", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Upgrade an existing project to a newer StreamTeX version.
            Runs migrations, performs AST-based API compatibility
            checks, and optionally syncs dependencies and updates
            Claude profiles. Use --check for a dry preview.
        """)
        st_space("v", 1)

        show_code("""\
# Check what would change (no modifications)
stx project upgrade --check

# Preview upgrade steps without executing
stx project upgrade --dry-run

# Run upgrade, skip uv sync
stx project upgrade --skip-sync

# Run upgrade, skip Claude profile update
stx project upgrade --skip-claude

# Full upgrade (default)
stx project upgrade""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            If the upgrade detects API incompatibilities that cannot
            be auto-fixed, use the **/stx-migrate** Claude skill for
            assisted code fixes. It walks you through each breaking
            change and suggests the correct replacement.
        """)
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
                         "stx install")
            with g.cell():
                st_write(s.large, "Create or upgrade a workspace")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx update")
            with g.cell():
                st_write(s.large, "Clone + pull + sync + hooks + profiles")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx status")
            with g.cell():
                st_write(s.large, "Check workspace state")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx project upgrade")
            with g.cell():
                st_write(s.large, "Upgrade project to newer StreamTeX")
        st_space("v", 2)

        show_details("""\
            The five workspace presets are:

            - **basic** — no repos, just stx.toml and projects/
            - **user** — streamtex-claude only
            - **standard** — streamtex-docs + streamtex-claude (default)
            - **power** — developer preset + extras
            - **developer** — all 3 repos (streamtex + docs + claude)

            The developer preset lets you work with streamtex-docs
            alongside the streamtex library for live testing via
            editable installs.

            Use stx status regularly to check for drift between
            linked projects. Use stx project upgrade --check to
            verify API compatibility before upgrading.
        """)
