"""Part 7 — CLI integration commands: install, diff, update, and workspace."""

import textwrap
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

    show_explanation(textwrap.dedent("""\
        The stx CLI provides commands for managing AI profiles and
        workspaces. These commands bridge the gap between the StreamTeX
        library and Claude Code configuration.
    """))
    st_space("v", 2)

    # ── stx claude install ────────────────────────────────────────
    st_write(bs.sub, "stx claude install", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Install a Claude Code profile into your project. This generates
        CLAUDE.md from the profile template, copies commands, agents,
        skills, and creates settings.json with safe defaults.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
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
        # Done. Profile 'project' installed successfully."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx claude diff ──────────────────────────────────────────
    st_write(bs.sub, "stx claude diff", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Compare your installed profile against the latest version.
        This shows which commands, agents, or skills have been added,
        modified, or removed since your last installation.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
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
        # Run 'stx claude update' to apply changes."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx claude update ─────────────────────────────────────────
    st_write(bs.sub, "stx claude update", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Update your installed profile to the latest version. This
        merges new components while preserving your custom additions.
        Your CLAUDE.md customizations are kept in a separate section.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
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
        # Done. Profile updated to v1.3.0."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace init ────────────────────────────────────────
    st_write(bs.sub, "stx workspace init", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Initialize a new StreamTeX workspace. Creates the directory
        structure, stx.toml configuration, and a starter project.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        stx workspace init my-workspace

        # Example output:
        # Creating workspace 'my-workspace'...
        #   Created stx.toml
        #   Created projects/ directory
        #   Created pyproject.toml
        # Done. Run 'cd my-workspace' to get started."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace clone ───────────────────────────────────────
    st_write(bs.sub, "stx workspace clone", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Clone a workspace from a remote Git repository. Sets up the
        full project structure and installs dependencies.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        stx workspace clone https://github.com/org/my-workspace.git

        # Example output:
        # Cloning workspace from https://github.com/org/my-workspace.git...
        #   Cloned repository
        #   Found 3 projects in stx.toml
        #   Running uv sync...
        # Done. Workspace ready."""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── stx workspace link ────────────────────────────────────────
    st_write(bs.sub, "stx workspace link", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Link a local StreamTeX library checkout for development.
        Changes to the library source are immediately available
        in your workspace without reinstalling.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        stx workspace link ../streamtex

        # Example output:
        # Linking StreamTeX library from ../streamtex...
        #   Added editable source to pyproject.toml
        #   Running uv sync...
        # Done. Library linked for development."""),
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
