from streamtex import *
from streamtex.enums import Tags as t
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

            - **library**: for the StreamTeX library itself.
            - **docs**: for documentation projects (manuals).
            - **project**: for end-user StreamTeX applications.

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
# Install a profile into a project
stx claude install project .
stx claude install documentation .
stx claude install presentation .""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Copies the matching profile template into .claude/.
            This includes settings.json, references, skills,
            commands, and agents. Also copies shared files
            (references and commands) from streamtex-claude/shared/.
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
            Displays all available profile templates with their
            description and file count. Useful for understanding
            what each profile includes before installing.
        """)
        st_space("v", 2)

        # --- stx claude update ---
        st_write(bs.sub, "stx claude update", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Update a single project (preserves CLAUDE.md)
stx claude update .

# Update and overwrite CLAUDE.md too
stx claude update . --force

# Update ALL projects in the workspace at once
stx claude update --all
stx claude update --all --force""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Compares local .claude/ files against the source in
            streamtex-claude/ and updates any modified or missing
            files. CLAUDE.md is preserved by default because it
            contains project-specific instructions (identity,
            local paths, workflows). Use --force to overwrite it.

            The --all flag scans the workspace for all projects
            with a .claude/.stx-profile marker (top-level dirs
            and projects/ subdirectories) and updates them all.
        """)
        st_space("v", 2)

        # --- stx claude diff ---
        st_write(bs.sub, "stx claude diff", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Show differences between local and source
stx claude diff .""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Shows a comparison between installed .claude/ files
            and the source in streamtex-claude/. Each file is
            reported as identical, modified, missing, or extra.
        """)
        st_space("v", 2)

        # --- stx claude check ---
        st_write(bs.sub, "stx claude check", toc_lvl="+1")
        st_space("v", 1)

        show_code("""\
# Verify sync status of all profiles in the workspace
stx claude check""", language="bash")
        st_space("v", 1)

        show_explanation("""\
            Scans the workspace for all projects with a Claude
            profile and reports their sync status. Returns exit
            code 1 if any files are out of sync, making it
            suitable for CI checks.
        """)
        st_space("v", 2)

        # --- Update workflow ---
        st_write(bs.sub, "Update workflow", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            When profiles are updated in the streamtex-claude
            repository (new commands, updated skills, etc.),
            propagate changes to all your projects:
        """)
        st_space("v", 1)

        show_code("""\
# 1. Pull latest profiles from the source repo
cd streamtex-claude && git pull

# 2. Propagate to all projects in the workspace
stx claude update --all

# 3. Verify everything is in sync
stx claude check""", language="bash")
        st_space("v", 2)

        # --- Shared files ---
        st_write(bs.sub, "Shared files", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Some files are shared across all profiles regardless
            of profile type. They live in streamtex-claude/shared/:

            - **shared/references/**: coding standards and cheatsheet,
              copied to .claude/references/ in every project.
            - **shared/commands/**: ecosystem-wide commands (e.g.,
              stx-guide.md), copied to .claude/commands/.

            These shared files are installed as **read-only** (0o444)
            to signal they are managed automatically. Do not edit
            them locally — changes will be overwritten on update.
        """)
        st_space("v", 2)

        # --- Profile storage ---
        st_write(bs.sub, "Profile storage", toc_lvl="+1")
        st_space("v", 1)

        show_explanation("""\
            Profile templates are stored in the streamtex-claude/
            repository. The structure is:

            streamtex-claude/
              profiles/
                project/        — for end-user applications
                presentation/   — extends project (live projection)
                library/        — for library development
                documentation/  — for manual authoring
              shared/
                references/     — coding standards, cheatsheet
                commands/       — stx-guide and other shared commands

            Each profile directory mirrors the .claude/ structure.
            manifest.toml declares which shared files to include.
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
                st_write(s.large, "Install a profile into a project")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude list")
            with g.cell():
                st_write(s.large, "List available profiles")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude update [--all]")
            with g.cell():
                st_write(s.large, "Update one or all projects")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude diff")
            with g.cell():
                st_write(s.large, "Compare installed vs source")
            with g.cell():
                st_write(s.project.colors.neutral_gray + s.large,
                         "stx claude check")
            with g.cell():
                st_write(s.large, "Verify sync of all workspace profiles")
        st_space("v", 2)

        show_details("""\
            Run stx claude check periodically or after pulling
            streamtex-claude to verify all profiles are in sync.
            Use stx claude update --all to propagate changes to
            every project in the workspace at once.
        """)
