"""Part 2 — Installing an AI Profile into a StreamTeX project."""

from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Profile installation block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    profile_cell = (
        s.container.paddings.small_padding
        + s.container.borders.solid_border
        + s.container.layouts.vertical_center_layout
    )


bs = BlockStyles


def build():
    """Installing an AI Profile — profiles, install command, and result."""
    st_space("v", 1)
    st_write(bs.heading, "Installing an AI Profile", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        AI profiles configure Claude Code (or Cursor) for StreamTeX
        development. Each profile bundles a CLAUDE.md, custom commands,
        agents, skills, and reference documentation tailored to
        a specific workflow.
    """)
    st_space("v", 2)

    # --- Install command ---
    st_write(bs.sub, "The Install Command", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        # Syntax
        stx claude install [profile] [project_path]

        # Example: install the project profile into ./my-presentation
        stx claude install project ./my-presentation
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- The 4 profiles ---
    st_write(bs.sub, "Available Profiles", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX ships with four AI profiles. Each one extends
        the base configuration with domain-specific rules and tools.
    """)
    st_space("v", 1)

    with st_grid(cols=2, cell_styles=bs.profile_cell) as g:
        # Profile: project
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(s.project.titles.subsection_title, "project")
                st_space("v", 0.5)
                st_write(s.bold + s.large, "Standard (recommended)")
                st_space("v", 0.5)
                st_write(s.large,
                         "The default profile for most users. "
                         "Includes commands for ",
                         (s.bold, "project scaffolding"), ", ",
                         (s.bold, "block creation"), ", and ",
                         (s.bold, "style management"), ".")

        # Profile: presentation
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(s.project.titles.subsection_title, "presentation")
                st_space("v", 0.5)
                st_write(s.bold + s.large, "Extends project")
                st_space("v", 0.5)
                st_write(s.large,
                         "Adds ", (s.bold, "live projection rules"), ", ",
                         (s.bold, "slide design agents"),
                         ", and presentation-specific skills like slide layout "
                         "and transition management.")

        # Profile: documentation
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(s.project.titles.subsection_title, "documentation")
                st_space("v", 0.5)
                st_write(s.bold + s.large, "Manual authoring focus")
                st_space("v", 0.5)
                st_write(s.large, (
                    "Optimized for writing manuals and courses. "
                    "Includes documentation structure rules, "
                    "cross-reference management, and book assembly."
                ))

        # Profile: library
        with g.cell():
            with st_block(s.project.containers.note_callout):
                st_write(s.project.titles.subsection_title, "library")
                st_space("v", 0.5)
                st_write(s.bold + s.large, "StreamTeX core development")
                st_space("v", 0.5)
                st_write(s.large, (
                    "For contributors to the StreamTeX library itself. "
                    "Includes testing workflows, release process, "
                    "and architecture documentation."
                ))
    st_space("v", 2)

    # --- What gets installed ---
    st_write(bs.sub, "What Gets Installed", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Running the install command creates a .claude/ directory
        in your project with the following structure.
    """)
    st_space("v", 1)

    show_code("""\
        my-presentation/
        +-- .claude/
        |   +-- commands/       # Slash commands (/stx-block:init, etc.)
        |   +-- agents/         # Autonomous agents (architect, designer)
        |   +-- skills/         # Reusable skill definitions
        |   +-- references/     # Coding standards, cheatsheets
        |   +-- settings.json   # Tool permissions
        +-- CLAUDE.md           # AI behavior configuration
    """, language="text", line_numbers=False)
    st_space("v", 2)

    # --- Example ---
    st_write(bs.sub, "Full Example", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        # Create a new project and install the project profile
        stx project new my-presentation
        stx claude install project ./my-presentation

        # Navigate and start working with Claude Code
        cd my-presentation
        claude
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        Profiles are additive: installing a new profile merges
        its contents with any existing .claude/ configuration.
        You can safely install multiple profiles into the same
        project if needed.
    """)
    st_space("v", 2)

    # --- Workspace presets with AI extras ---
    st_write(bs.sub, "Workspace Presets and AI Extras", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX workspace presets bundle optional extras alongside
        the core installation. Two presets include AI capabilities
        out of the box.
    """)
    st_space("v", 1)

    show_code("""\
        # standard preset — includes pdf + ai extras
        stx install --preset standard

        # power preset — includes pdf + ai + inspector extras
        stx install --preset power
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        With these presets, AI image generation
        (st_image(prompt=..., editable=True), generate_image) and
        related providers are available without manually adding
        optional dependencies.
    """)
    st_space("v", 2)

    # --- Upgrading existing projects ---
    st_write(bs.sub, "Upgrading Existing Projects", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        If you created a project before AI features were available,
        use stx project upgrade to bring your project up to date
        with the latest scaffolding and configuration — including
        AI-related dependencies and settings.
    """)
    st_space("v", 1)

    show_code("""\
        # Check what would change
        stx project upgrade --check

        # Preview without applying
        stx project upgrade --dry-run

        # Apply the upgrade
        stx project upgrade
    """, language="bash", line_numbers=False)
    st_space("v", 1)

    # --- Previewing an install (0.7.35) ---
    st_write(bs.sub, "Previewing an Install: --dry-run and --yes",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Since streamtex 0.7.35, stx claude install --dry-run lists every
        file the install would create, replace, merge or keep, and writes
        nothing. When the target already holds files that stx did not
        install (no .claude/.stx-profile yet), the real install stops and
        lists them instead of replacing them. Review the list, then rerun
        with --yes to install anyway.
    """)
    st_space("v", 1)

    show_code("""\
        # 1. See every file the install would write — nothing is written
        stx claude install project ./my-presentation --dry-run

        # 2. Install. Stops with the list of existing files that stx
        #    did not install and would replace
        stx claude install project ./my-presentation

        # 3. Install anyway, once the list has been reviewed
        stx claude install project ./my-presentation --yes
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Updating and git (0.7.35) ---
    st_write(bs.sub, "Updating a Profile: stx Never Commits",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        stx claude update adds the .gitignore block that ignores the
        installed copies under .claude/ (custom/ and .stx-profile stay
        tracked), then prints the git commands that untrack them. It
        never commits in your project unless you ask with --commit.
        The clones of the official repositories declared in the
        workspace [repos] (created and pulled by stx update) are the
        exception: they keep the migration commit, so their tree stays
        clean for git pull.
    """)
    st_space("v", 1)

    show_code("""\
        # Default: .gitignore completed, git commands printed, no commit
        stx claude update

        # On request: untrack the managed .claude/ files and commit that change
        stx claude update --commit

        # Replace your local edits of installed files (backup in .claude/.backup/)
        stx claude update --force
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- What the installer places (shared files) ---
    st_write(bs.sub, "Shared Skills, Agents and Import Formats",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Besides its own files, a profile's manifest.toml declares
        shared files in its [shared] section. stx claude install,
        update and sync install the declared skills, agents and import
        formats (reuse-architecture, modular-design-philosophy,
        authoring-gate, import-conventions, the deploy and import
        agents, the marp / html / latex import formats). Older
        versions of the library installer skipped them: the next
        update adds them and removes nothing.
    """)
    st_space("v", 1)

    show_code("""\
        # profiles/project/manifest.toml (streamtex-claude)
        [shared]
        skills = ["import-conventions.md", "hetzner-infrastructure.md",
                  "ssh-operations.md", "reuse-architecture.md",
                  "modular-design-philosophy.md", "authoring-gate.md"]
        agents = ["import-converter.md", "deploy-operator.md"]
        import-formats = ["marp", "html", "latex"]

        # Where they land in the project
        #   skills          -> .claude/developer/skills/
        #   agents          -> .claude/developer/agents/
        #   import-formats  -> .claude/import-formats/
    """, language="toml", line_numbers=False)
    st_space("v", 2)

    # --- Project mode (0.7.35) ---
    st_write(bs.sub, "Project Mode", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        In project mode (streamtex 0.7.35+), the project declares its
        Claude content in stx.toml, and stx claude sync makes .claude/
        match that declaration. Git keeps the declaration and the lock
        file; a fresh clone followed by stx claude sync rebuilds the
        same .claude/. The commands live in the project only, not in
        ~/.claude/commands.
    """)
    st_space("v", 1)

    show_code("""\
        # stx.toml of the project
        [claude]
        mode = "project"
        profile = "presentation"   # project | presentation | library | documentation
        include = []               # extra profiles merged in, e.g. ["library"]
        exclude = []               # groups left out, e.g. ["stx-ce", "ce", "stx-pe", "pack-engineering"]
    """, language="toml", line_numbers=False)
    st_space("v", 1)

    show_code("""\
        stx claude sync --dry-run   # what would change — nothing written
        stx claude sync             # install / update / prune; writes .claude/stx.lock
        stx claude sync --force     # also replace your local edits (backup in .claude/.backup/)
        stx claude sync --remove    # uninstall every file stx installed (custom/ kept)
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        Every sync records, in .claude/stx.lock, the profile, the
        include / exclude lists, the streamtex-claude revision and the
        sha256 of every installed file. The lock starts with format = 1;
        a lock written without it (streamtex 0.7.35 to 0.7.40) is read
        as format 1, and a higher format (written by a newer stx) is
        refused instead of rewritten.
    """)
    st_space("v", 1)

    show_code("""\
        # .claude/stx.lock — written by `stx claude sync`; do not edit.
        # Versioned with the project: a clone + `stx claude sync` rebuilds the same .claude/.
        [lock]
        format = 1
        profile = "presentation"
        include = []
        exclude = []
        source = "/path/to/streamtex-claude"
        source_rev = "<git commit of streamtex-claude>"
        claude_md = "CLAUDE.md"
        claude_md_sha = "<sha256>"

        [files]
        ".claude/references/coding_standards.md" = "<sha256>"
    """, language="toml", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        The lock gives a three-way comparison for each file: the local
        file, the source file in streamtex-claude, and the hash recorded
        at the last sync.
    """)
    st_space("v", 1)

    with st_grid(cols=3, cell_styles=bs.profile_cell) as g:
        with g.cell():
            st_write(s.bold + s.large, "Local file vs lock")
        with g.cell():
            st_write(s.bold + s.large, "Source vs local")
        with g.cell():
            st_write(s.bold + s.large, "What sync does")
        with g.cell():
            st_write(s.large, "equal (untouched)")
        with g.cell():
            st_write(s.large, "different")
        with g.cell():
            st_write(s.large, "update — the change came from upstream")
        with g.cell():
            st_write(s.large, "different (edited by you)")
        with g.cell():
            st_write(s.large, "different")
        with g.cell():
            st_write(s.large, "keep and report — --force replaces it, with a backup")
        with g.cell():
            st_write(s.large, "—")
        with g.cell():
            st_write(s.large, "equal")
        with g.cell():
            st_write(s.large, "nothing to do")
        with g.cell():
            st_write(s.large, "absent")
        with g.cell():
            st_write(s.large, "—")
        with g.cell():
            st_write(s.large, "install")
    st_space("v", 2)

    show_details("""\
        A file no longer declared is removed only if it is unchanged
        since the last sync; an edited one is kept and reported. A file
        stx never installed is never touched, and .claude/custom/ never.
        settings.json is merged, not replaced. stx update,
        stx claude update (--all) and stx claude check handle
        project-mode targets through the same path, the workspace root
        included when it declares project mode. stx validate checks the
        [claude] section (unknown profile, an exclude that matches
        nothing). The .gitignore keeps custom/, .stx-profile and
        stx.lock tracked and ignores the copies; nothing is committed.
    """)
    st_space("v", 2)

    # --- Machine mode (0.7.35) ---
    st_write(bs.sub, "Machine Mode: Global Commands", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        In the classic machine mode, stx install and stx update also
        copy the shared commands (such as /stx-guide) into
        ~/.claude/commands, so they are available in every directory.
        Since 0.7.35 each copy is recorded in
        ~/.config/streamtex/global-commands.json, and two commands
        inspect and remove only what stx copied there.
    """)
    st_space("v", 1)

    show_code("""\
        # Classify each stx-* entry of ~/.claude/commands:
        # current / outdated / obsolete / modified by you
        stx claude global status

        # Show what would be removed (dry run: nothing removed)
        stx claude global remove

        # Remove the stx copies; a file you changed is kept and listed
        stx claude global remove --yes
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    show_explanation("""\
        The copy itself is optional. The machine setting lives in
        ~/.config/streamtex/config.toml; the flags on stx install and
        stx update override it for one run (they set
        $STX_GLOBAL_COMMANDS underneath). Without any setting, the
        commands are copied, as before.
    """)
    st_space("v", 1)

    show_code("""\
        # ~/.config/streamtex/config.toml
        [claude]
        global_commands = false
    """, language="toml", line_numbers=False)
    st_space("v", 1)

    show_code("""\
        stx update --no-global-commands    # do not copy for this run
        stx update --global-commands       # copy for this run
        stx install --no-global-commands   # same flags on stx install
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- Duplicate report (0.7.35) ---
    st_write(bs.sub, "Duplicate and Obsolete Commands Report", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        stx claude check and stx status end with a "Claude commands"
        section when something needs attention, and print nothing
        otherwise. They report the command groups present both in
        ~/.claude/commands and in a project (Claude Code loads both
        copies), the obsolete global groups no longer shipped (such as
        stx-pattern), and, when the global copy is off, a workspace in
        which no project has a local profile.
    """)
    st_space("v", 1)

    show_code("""\
        $ stx claude check
        ...
        Claude commands
          ! projects/my-deck (presentation) — 3 command group(s) also in ~/.claude/commands (both load): stx-ds, stx-pack, stx-validate
          ! ~/.claude/commands — obsolete group(s) no longer shipped: stx-pattern (stx claude global remove)
    """, language="text", line_numbers=False, wrap=True)
    st_space("v", 1)
