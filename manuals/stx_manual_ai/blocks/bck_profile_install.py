"""Part 2 — Installing an AI Profile into a StreamTeX project."""

import textwrap
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

    show_code(textwrap.dedent("""\
        # Syntax
        stx claude install [profile] [project_path]

        # Example: install the project profile into ./my-presentation
        stx claude install project ./my-presentation
    """), language="bash", line_numbers=False)
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
                st_write(s.large, (
                    "The default profile for most users. "
                    "Includes commands for project scaffolding, "
                    "block creation, and style management."
                ))

        # Profile: presentation
        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(s.project.titles.subsection_title, "presentation")
                st_space("v", 0.5)
                st_write(s.bold + s.large, "Extends project")
                st_space("v", 0.5)
                st_write(s.large, (
                    "Adds live projection rules, slide design agents, "
                    "and presentation-specific skills like slide layout "
                    "and transition management."
                ))

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

    show_code(textwrap.dedent("""\
        my-presentation/
        +-- .claude/
        |   +-- commands/       # Slash commands (/project:init, etc.)
        |   +-- agents/         # Autonomous agents (architect, designer)
        |   +-- skills/         # Reusable skill definitions
        |   +-- references/     # Coding standards, cheatsheets
        |   +-- settings.json   # Tool permissions
        +-- CLAUDE.md           # AI behavior configuration
    """), language="text", line_numbers=False)
    st_space("v", 2)

    # --- Example ---
    st_write(bs.sub, "Full Example", toc_lvl="+1")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Create a new project and install the project profile
        stx project new my-presentation
        stx claude install project ./my-presentation

        # Navigate and start working with Claude Code
        cd my-presentation
        claude
    """), language="bash", line_numbers=False)
    st_space("v", 2)

    show_details("""\
        Profiles are additive: installing a new profile merges
        its contents with any existing .claude/ configuration.
        You can safely install multiple profiles into the same
        project if needed.
    """)
    st_space("v", 1)
