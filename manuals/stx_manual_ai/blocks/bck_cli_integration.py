"""Part 7 — CLI integration commands: install, diff, update, and workspace."""

from streamtex import st_write, st_space, st_block
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """CLI integration block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """CLI Integration Commands — stx claude and stx workspace."""
    st_space("v", 1)
    st_write(bs.heading, "CLI Integration Commands",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The stx CLI provides commands for managing AI profiles and
        workspaces. These commands bridge the gap between the StreamTeX
        library and Claude Code configuration.
    """)
    st_space("v", 2)

    # ── stx claude install ────────────────────────────────────────
    st_write(bs.sub, "stx claude install", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Install a Claude Code profile into your project. This generates
        CLAUDE.md from the profile template, copies commands, agents,
        skills, and creates settings.json with safe defaults.
    """)
    st_space("v", 1)

    show_code("""\
        # Install the default 'project' profile
        stx claude install

        # Install a specific profile
        stx claude install --profile presentation

        # Example output:
        # Installing profile 'project' into .claude/...
        #   Created CLAUDE.md
        #   Installed 8 commands (project: 4, designer: 3, developer: 1)
        #   Installed 3 agents
        #   Installed 4 skills
        #   Created settings.json
        # Done. Profile 'project' installed successfully.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx claude diff ──────────────────────────────────────────
    st_write(bs.sub, "stx claude diff", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Compare your installed profile against the latest version.
        This shows which commands, agents, or skills have been added,
        modified, or removed since your last installation.
    """)
    st_space("v", 1)

    show_code("""\
        stx claude diff

        # Example output:
        # Comparing installed 'project' (v1.2.0) with latest (v1.3.0)
        #
        # Commands:
        #   + designer/chart-new.md          (new)
        #   ~ project/project-init.md        (modified)
        #
        # Agents:
        #   ~ architect-agent.md             (modified)
        #
        # Skills:
        #   + data_visualization.md          (new)
        #
        # Run 'stx claude update' to apply changes.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx claude update ─────────────────────────────────────────
    st_write(bs.sub, "stx claude update", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Update your installed profile to the latest version. This
        merges new components while preserving your custom additions.
        Your CLAUDE.md customizations are kept in a separate section.
    """)
    st_space("v", 1)

    show_code("""\
        # Update to latest version
        stx claude update

        # Force update (overwrites local modifications)
        stx claude update --force

        # Example output:
        # Updating profile 'project' from v1.2.0 to v1.3.0...
        #   Updated 1 command (project/project-init.md)
        #   Added 1 command (designer/chart-new.md)
        #   Updated 1 agent (architect-agent.md)
        #   Added 1 skill (data_visualization.md)
        #   Preserved CLAUDE.md custom sections
        # Done. Profile updated to v1.3.0.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace init ────────────────────────────────────────
    st_write(bs.sub, "stx workspace init", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Initialize a new StreamTeX workspace with stx.toml.
        The --preset option controls which repos are declared.
        Default preset is standard (docs + claude).
    """)
    st_space("v", 1)

    show_code("""\
        stx workspace init .
        stx workspace init . --preset user       # Claude profiles only
        stx workspace init . --preset developer   # all 3 repos

        # Example output:
        # Workspace initialized: /path/to/workspace
        #   stx.toml created (name='my-workspace', preset='standard')
        #   projects/ directory created""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace update ──────────────────────────────────────
    st_write(bs.sub, "stx workspace update", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The single command for all workspace operations: clone repos,
        pull latest changes, sync dependencies, install pre-commit
        hooks, update Claude profiles, and install global commands.
    """)
    st_space("v", 1)

    show_code("""\
        stx workspace update

        # Fine-grained control
        stx workspace update --skip-sync      # skip uv sync
        stx workspace update --skip-profiles  # skip Claude profile update
        stx workspace update --dry-run        # show steps without executing
        stx workspace update --repair         # fix broken venv, missing __init__.py

        # Example output:
        #   Step 1/6: git pull (2 repos)
        #   Step 2/6: clone missing repos (0 new)
        #   Step 3/6: uv sync (2 repos)
        #   Step 4/6: update Claude profiles
        #   Step 5/6: install global commands
        #   Step 6/6: install pre-commit hooks
        # Done.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace upgrade ─────────────────────────────────────
    st_write(bs.sub, "stx workspace upgrade", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Upgrade a workspace to a higher preset. Adds missing repo
        sections to stx.toml without touching existing configuration.
        Run stx workspace update after to fetch new repos.
    """)
    st_space("v", 1)

    show_code("""\
        stx workspace upgrade developer
        stx workspace update

        # Example output:
        # Upgraded from 'standard' to 'developer'.
        #   + streamtex
        # Run stx workspace update to clone the new repos.""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Tip ───────────────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip: Check for Updates Regularly")
        st_space("v", 1)
        st_write(s.large, (
            "Run stx claude diff periodically to check if your installed "
            "profile has fallen behind the latest version. New StreamTeX "
            "releases often include improved commands, updated coding "
            "standards, and new agent capabilities. Keeping your profile "
            "up to date ensures you benefit from these improvements."
        ))
    st_space("v", 1)
