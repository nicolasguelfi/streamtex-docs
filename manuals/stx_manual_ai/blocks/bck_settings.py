"""Part 2 — Claude Code Settings and tool permissions."""

import textwrap
from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Settings block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Claude Code Settings — permissions, scopes, and configuration."""
    st_space("v", 1)
    st_write(bs.heading, "Claude Code Settings", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        The settings.json file controls which tools Claude Code is
        allowed to use in your project. It defines permission scopes
        that balance productivity with safety.
    """))
    st_space("v", 2)

    # --- File structure ---
    st_write(bs.sub, "Settings File Structure", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The settings file lives at .claude/settings.json inside
        your project. It uses a simple JSON structure with
        permission arrays.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        {
          "permissions": {
            "allowedTools": [
              "Bash(uv run *)",
              "Bash(uv add *)",
              "Bash(uv sync)",
              "Bash(stx *)",
              "Bash(git *)",
              "Read",
              "Write",
              "Edit",
              "Glob",
              "Grep"
            ],
            "blockedTools": [
              "Bash(rm -rf *)",
              "Bash(pip install *)",
              "Bash(python *)"
            ]
          }
        }
    """), language="json", line_numbers=False)
    st_space("v", 2)

    # --- Permission scopes ---
    st_write(bs.sub, "Permission Scopes", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The two main permission arrays control what Claude Code
        can and cannot do in your project.
    """))
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "allowedTools")
        st_space("v", 1)
        st_write(s.large, (
            "Lists the tools and command patterns that Claude Code "
            "can use without asking for permission. Supports glob "
            "patterns for flexible matching."
        ))
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, 'Bash(uv run *) — allows all uv run commands')
            with l.item(): st_write(s.large, 'Bash(git *) — allows all git operations')
            with l.item(): st_write(s.large, 'Read, Write, Edit — file operations')
            with l.item(): st_write(s.large, 'Glob, Grep — search operations')
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(s.project.colors.error_red + s.bold, "blockedTools")
        st_space("v", 1)
        st_write(s.large, (
            "Lists tools and patterns that are explicitly forbidden. "
            "These take precedence over allowedTools. Use this to "
            "prevent dangerous operations."
        ))
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, 'Bash(rm -rf *) — prevents recursive deletion')
            with l.item(): st_write(s.large, 'Bash(pip install *) — enforces uv usage')
            with l.item(): st_write(s.large, 'Bash(python *) — enforces uv run prefix')
    st_space("v", 2)

    # --- How to configure ---
    st_write(bs.sub, "Configuring Permissions", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        You can edit settings.json directly to add or remove
        tool permissions. Common customizations include allowing
        Docker commands or restricting file writes to specific
        directories.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        {
          "permissions": {
            "allowedTools": [
              "Bash(uv run *)",
              "Bash(docker build *)",
              "Bash(docker compose *)",
              "Read",
              "Write(./blocks/*)",
              "Edit(./blocks/*)"
            ]
          }
        }
    """), language="json", line_numbers=False)
    st_space("v", 2)

    # --- Tip about safe defaults ---
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip: Safe Defaults")
        st_space("v", 1)
        st_write(s.large, (
            "When you install a profile with stx claude install, "
            "the settings.json is pre-configured with safe defaults "
            "for that profile. The project profile allows standard "
            "development tools while blocking destructive operations. "
            "You only need to customize if your project has specific "
            "security requirements."
        ))
    st_space("v", 1)
