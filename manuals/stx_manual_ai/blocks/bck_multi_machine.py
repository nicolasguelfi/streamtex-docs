"""Part 7 — Multi-machine synchronization for .claude/ configuration."""

import textwrap
from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Multi-machine sync block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Multi-Machine Synchronization — sync strategies and best practices."""
    st_space("v", 1)
    st_write(bs.heading, "Multi-Machine Synchronization",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── The problem ───────────────────────────────────────────────
    show_explanation(textwrap.dedent("""\
        The .claude/ directory contains your AI configuration: commands,
        agents, skills, and settings. When you work on multiple machines
        (laptop, desktop, CI server), you need a strategy to keep this
        configuration synchronized.
    """))
    st_space("v", 2)

    # ── What to sync ──────────────────────────────────────────────
    st_write(bs.sub, "What to Sync", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "SYNC: These Files")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, "commands/ — all custom command .md files")
            st_write(s.large, "agents/ — all agent definition files")
            st_write(s.large, "skills/ — knowledge base files")
            st_write(s.large, "references/ — coding standards, cheatsheets")
            st_write(s.large, "CLAUDE.md — the main behavior configuration")
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(s.project.colors.error_red + s.bold,
                 "DO NOT SYNC: These Files")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, (
                "memory/ — machine-specific, contains local context"
            ))
            st_write(s.large, (
                "settings.json — contains path-dependent permissions"
            ))
            st_write(s.large, (
                "Any files with absolute paths or machine-specific config"
            ))
    st_space("v", 2)

    # ── Solution: sync script ─────────────────────────────────────
    st_write(bs.sub, "Solution: claude-sync.sh Script", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        A simple shell script can synchronize the portable parts of
        .claude/ between machines. Run it after pulling changes or
        when setting up a new machine.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        #!/bin/bash
        # claude-sync.sh — Sync .claude/ configuration between machines
        set -euo pipefail

        SOURCE="${1:?Usage: claude-sync.sh <source-dir>}"
        TARGET=".claude"

        echo "Syncing from $SOURCE to $TARGET..."

        # Sync commands, agents, skills, references
        for dir in commands agents skills references; do
            if [ -d "$SOURCE/$dir" ]; then
                mkdir -p "$TARGET/$dir"
                rsync -av --delete "$SOURCE/$dir/" "$TARGET/$dir/"
                echo "  Synced $dir/"
            fi
        done

        # Sync CLAUDE.md (but not settings or memory)
        if [ -f "$SOURCE/CLAUDE.md" ]; then
            cp "$SOURCE/CLAUDE.md" "$TARGET/CLAUDE.md"
            echo "  Synced CLAUDE.md"
        fi

        echo "Done. Skipped: memory/, settings.json" """),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Alternative: git ──────────────────────────────────────────
    st_write(bs.sub, "Alternative: Version .claude/ with Git",
             toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Instead of a sync script, you can commit .claude/ to your
        project repository. This ensures every collaborator and
        every machine gets the same configuration. Use .gitignore
        to exclude machine-specific files.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # .gitignore — exclude machine-specific .claude/ files
        .claude/projects/*/memory/
        .claude/settings.json"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Tips ──────────────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip: Always Exclude Memory")
        st_space("v", 1)
        st_write(s.large, (
            "The memory/ directory contains machine-specific context "
            "that Claude accumulates during sessions. Syncing it between "
            "machines causes confusion because paths, service IDs, and "
            "local state differ. Each machine should build its own memory "
            "organically through usage."
        ))
    st_space("v", 1)
