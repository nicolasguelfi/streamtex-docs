"""Part 7 — The stx-guide global skill: StreamTeX expertise for any session."""

import textwrap
from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """stx-guide skill block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """The stx-guide Global Skill — purpose, activation, and usage."""
    st_space("v", 1)
    st_write(bs.heading, "The stx-guide Global Skill",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        The stx-guide skill is a global knowledge base that provides
        StreamTeX expertise to any AI assistant. Unlike project-specific
        profiles, it is available across all projects and sessions
        without any installation.
    """))
    st_space("v", 2)

    # ── What it covers ────────────────────────────────────────────
    st_write(bs.sub, "What stx-guide Covers", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The skill packages the complete StreamTeX knowledge base into
        a format that Claude Code can consume on demand.
    """))
    st_space("v", 1)

    with st_list(list_type="ul"):
        st_write(s.large, (
            (s.bold, "API Reference"), " — all stx functions with signatures and examples"
        ))
        st_write(s.large, (
            (s.bold, "Best Practices"), " — coding standards, Style composition, block patterns"
        ))
        st_write(s.large, (
            (s.bold, "Common Patterns"), " — grids, lists, code blocks, containers"
        ))
        st_write(s.large, (
            (s.bold, "Troubleshooting"), " — common errors and how to fix them"
        ))
        st_write(s.large, (
            (s.bold, "Migration Guides"), " — upgrading from older StreamTeX versions"
        ))
    st_space("v", 2)

    # ── How to activate ──────────────────────────────────────────
    st_write(bs.sub, "How to Activate", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        The stx-guide skill activates automatically when you mention
        StreamTeX in a Claude Code conversation. You can also invoke
        it explicitly using the slash command syntax.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Automatic activation — just mention StreamTeX
        > How do I create a grid layout in StreamTeX?

        # Explicit invocation
        /stx-guide"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Guide vs Profile ─────────────────────────────────────────
    st_write(bs.sub, "Guide vs Project Profile", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "stx-guide (Global Skill)")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, "Read-only knowledge base")
            st_write(s.large, "Available in any project, any session")
            st_write(s.large, "No commands or agents — pure reference")
            st_write(s.large, "Answers API questions, explains syntax")
            st_write(s.large, "Does not modify project files")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Project Profile (Installed)")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, "Full behavior configuration (CLAUDE.md)")
            st_write(s.large, "Includes commands, agents, and skills")
            st_write(s.large, "Project-specific — must be installed")
            st_write(s.large, "Can create and modify files")
            st_write(s.large, "Defines coding standards and constraints")
    st_space("v", 2)

    # ── When to use ──────────────────────────────────────────────
    st_write(bs.sub, "When to Use stx-guide", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Use stx-guide for quick lookups when you do not need the full
        profile machinery. It is ideal for these situations:
    """))
    st_space("v", 1)

    with st_list(list_type="ul"):
        st_write(s.large, "Quick questions about a specific API function")
        st_write(s.large, "Syntax help when writing blocks from memory")
        st_write(s.large, "Debugging a rendering issue")
        st_write(s.large, "Exploring what StreamTeX can do before starting a project")
        st_write(s.large, "Working in a non-StreamTeX project that needs a one-off slide")
    st_space("v", 2)

    show_details(textwrap.dedent("""\
        The stx-guide skill is maintained alongside the StreamTeX
        library. When the library is updated, the skill is updated
        automatically to reflect new functions, deprecations, and
        changed signatures.
    """))
    st_space("v", 1)
