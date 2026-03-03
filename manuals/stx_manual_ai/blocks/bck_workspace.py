"""Part 2 — Workspace Setup for StreamTeX projects."""

import textwrap
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
    """Workspace Setup — init, clone, link, and stx.toml."""
    st_space("v", 1)
    st_write(bs.heading, "Workspace Setup", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        A StreamTeX workspace organizes multiple projects under a single
        root directory. It manages shared dependencies, AI profiles, and
        project configuration through stx.toml.
    """))
    st_space("v", 2)

    # --- stx workspace init ---
    st_write(bs.sub, "Initialize a Workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Create a new workspace from scratch. This generates
        the directory structure, stx.toml configuration file,
        and a default project scaffold.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Create a new workspace
        stx workspace init my-workspace

        # Navigate into it
        cd my-workspace
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx workspace clone ---
    st_write(bs.sub, "Clone an Existing Workspace", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Clone a workspace from a Git repository. This pulls down
        the full project structure including all configured
        projects, profiles, and shared resources.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Clone from a Git repository
        stx workspace clone https://github.com/org/my-workspace.git
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx workspace link ---
    st_write(bs.sub, "Link to Library for Development", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Link a local StreamTeX library checkout for development.
        This sets up an editable install so changes to the library
        source are immediately reflected in your workspace.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Link local streamtex library (editable install)
        stx workspace link ../streamtex
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    # --- stx.toml ---
    st_write(bs.sub, "The stx.toml Configuration File", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Every workspace has an stx.toml file at its root. It defines
        the workspace metadata, projects, and their relationships.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        [workspace]
        name = "my-workspace"
        version = "0.1.0"

        [workspace.projects]
        my-presentation = { path = "projects/my-presentation" }
        my-course = { path = "projects/my-course" }

        [workspace.defaults]
        profile = "project"
        python = "3.12"
    """), language="toml")
    st_space("v", 2)

    # --- Workspace vs standalone ---
    st_write(bs.sub, "Workspace vs Standalone Project", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        You can use StreamTeX with or without a workspace.
        Here is when each approach makes sense.
    """))
    st_space("v", 1)

    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Workspace (recommended)")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, "Multiple related projects (presentations, courses)")
            with l.item(): st_write(s.large, "Shared AI profiles across projects")
            with l.item(): st_write(s.large, "Centralized dependency management")
            with l.item(): st_write(s.large, "Team collaboration on the same repository")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Standalone Project")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, "Single presentation or document")
            with l.item(): st_write(s.large, "Quick prototyping or experimentation")
            with l.item(): st_write(s.large, "No need for shared configuration")
    st_space("v", 2)

    show_details(textwrap.dedent("""\
        A standalone project is simply a StreamTeX project without
        a wrapping workspace. It still uses stx.toml but at the
        project level. You can always convert a standalone project
        into a workspace later using stx workspace init --from-project.
    """))
    st_space("v", 1)
