"""Part 2 — Workspace Setup for StreamTeX projects."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Workspace setup block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Workspace Setup — init, update, and stx.toml."""
    st_space("v", 1)
    st_write(bs.heading, "Workspace Setup", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        A StreamTeX workspace organizes multiple projects under a single
        root directory. It manages shared dependencies, AI profiles, and
        project configuration through stx.toml.
    """)
    st_space("v", 2)

    # --- stx workspace init ---
    st_write(bs.sub, "Initialize a Workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Create a new workspace with stx.toml. The --preset option
        controls which repos are declared. Default is standard
        (docs + claude profiles).
    """)
    st_space("v", 1)

    show_code("""\
        mkdir streamtex-dev && cd streamtex-dev
        stx workspace init .                     # standard (default)
        stx workspace init . --preset user       # Claude profiles only
        stx workspace init . --preset developer  # all 3 repos
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx workspace update ---
    st_write(bs.sub, "Update a Workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The single command for all workspace operations: clone repos,
        pull latest changes, sync dependencies, install pre-commit
        hooks, update Claude profiles, and install global commands.
        Use it after init and whenever you need to update.
    """)
    st_space("v", 1)

    show_code("""\
        stx workspace update
        # Fine-grained control
        stx workspace update --skip-sync      # skip uv sync
        stx workspace update --skip-profiles  # skip Claude profile update
        stx workspace update --dry-run        # show steps without executing
        stx workspace update --repair         # fix broken venv, missing __init__.py
    """, language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx.toml ---
    st_write(bs.sub, "The stx.toml Configuration File", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Every workspace has an stx.toml file at its root. It defines
        the workspace preset, declared repos, deploy settings,
        and Claude profile source.
    """)
    st_space("v", 1)

    show_code("""\
        [workspace]
        name = "streamtex-dev"
        created = "2026-03-04T12:00:00Z"
        preset = "standard"

        [repos]

        [repos.streamtex-docs]
        url = "https://github.com/nicolasguelfi/streamtex-docs.git"
        path = "streamtex-docs"
        type = "docs"

        [repos.streamtex-claude]
        url = "https://github.com/nicolasguelfi/streamtex-claude.git"
        path = "streamtex-claude"
        type = "claude"

        [deploy]

        [claude]
        source = "streamtex-claude"
    """, language="toml")
    st_space("v", 2)

    # --- Workspace vs standalone ---
    st_write(bs.sub, "Workspace vs Standalone Project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        You can use StreamTeX with or without a workspace.
        Here is when each approach makes sense.
    """)
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Workspace (recommended)")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, (s.bold, "Multiple related projects"), " (presentations, courses)")
            with l.item(): st_write(s.large, (s.bold, "Shared AI profiles"), " across projects")
            with l.item(): st_write(s.large, (s.bold, "Centralized dependency management"))
            with l.item(): st_write(s.large, (s.bold, "Team collaboration"), " on the same repository")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Standalone Project")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, (s.bold, "Single presentation"), " or document")
            with l.item(): st_write(s.large, (s.bold, "Quick prototyping"), " or experimentation")
            with l.item(): st_write(s.large, (s.bold, "No need"), " for shared configuration")
    st_space("v", 2)

    show_details("""\
        A standalone project is simply a StreamTeX project created
        without a workspace (stx project new outside a workspace).
        You can always create a workspace later and move the project
        into its projects/ directory.

        Use stx workspace upgrade to move to a higher preset
        (e.g. from user to standard) without recreating the workspace.
    """)
    st_space("v", 1)
