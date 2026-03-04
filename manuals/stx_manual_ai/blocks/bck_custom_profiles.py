"""Part 7 — Creating and extending profiles: manifest.toml and templates."""

from streamtex import st_write, st_space, st_block
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """Custom profiles block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Creating & Extending Profiles — manifest, templates, and inheritance."""
    st_space("v", 1)
    st_write(bs.heading, "Creating & Extending Profiles",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        A profile is a complete AI configuration package. It bundles
        CLAUDE.md templates, commands, agents, skills, and settings
        into a reusable unit. Profiles can extend other profiles to
        inherit and specialize behavior.
    """)
    st_space("v", 2)

    # ── Profile structure ─────────────────────────────────────────
    st_write(bs.sub, "Profile Directory Structure", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        streamtex-claude/
        └── profiles/
            └── my-profile/
                ├── manifest.toml          # Profile metadata
                ├── CLAUDE.md.j2           # Template for CLAUDE.md
                ├── commands/
                │   ├── project/
                │   │   └── my-command.md
                │   └── designer/
                │       └── my-design-cmd.md
                ├── agents/
                │   └── my-agent.md
                └── skills/
                    └── my-knowledge.md""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── manifest.toml anatomy ─────────────────────────────────────
    st_write(bs.sub, "The manifest.toml File", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The manifest.toml file is the heart of a profile. It declares
        metadata, lists all components, and optionally specifies a
        parent profile to extend.
    """)
    st_space("v", 1)

    show_code("""\
        [profile]
        name = "my-profile"
        description = "Custom profile for data science presentations"
        version = "1.0.0"
        extends = "project"   # Inherit from the base project profile

        [commands]
        project = [
            "project-init",
            "project-customize",
            "course-generate",
        ]
        designer = [
            "block-new",
            "slide-new",
        ]
        analysis = [
            "data-import",     # Custom command for this profile
            "chart-generate",  # Custom command for this profile
        ]

        [agents]
        agents = [
            "architect-agent",
            "slide-designer-agent",
            "data-analyst-agent",  # Custom agent for this profile
        ]

        [skills]
        skills = [
            "coding_standards",
            "streamtex_api",
            "data_visualization",  # Custom skill for this profile
        ]""",
        language="toml")
    st_space("v", 2)

    # ── Extending profiles ────────────────────────────────────────
    st_write(bs.sub, "Extending an Existing Profile", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The extends field in [profile] tells the installer to merge
        the parent profile's components with your additions. Your
        profile inherits all commands, agents, and skills from the
        parent, and you can add or override specific ones.
    """)
    st_space("v", 1)

    show_code("""\
        [profile]
        name = "presentation"
        description = "Extended profile for live presentations"
        extends = "project"  # Inherits everything from 'project'

        [commands]
        # Only list NEW commands — inherited ones come automatically
        presenter = [
            "rehearsal-mode",
            "export-pdf",
        ]

        [agents]
        agents = [
            "presentation-designer-agent",  # Overrides standard designer
        ]""",
        language="toml")
    st_space("v", 2)

    # ── Creating from scratch ─────────────────────────────────────
    st_write(bs.sub, "Creating a Profile from Scratch", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        If you do not want to extend an existing profile, omit the
        extends field. You must then provide a complete CLAUDE.md.j2
        template and all the commands, agents, and skills your
        profile needs.
    """)
    st_space("v", 1)

    show_code("""\
        [profile]
        name = "standalone"
        description = "Minimal standalone profile"
        version = "1.0.0"
        # No 'extends' — fully self-contained

        [commands]
        project = ["project-init"]

        [agents]
        agents = []

        [skills]
        skills = ["streamtex_api"]""",
        language="toml")
    st_space("v", 2)

    # ── Tips ──────────────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip: Extend, Don't Duplicate")
        st_space("v", 1)
        st_write(s.large, (
            "Always prefer extending an existing profile over creating "
            "one from scratch. The base 'project' profile is maintained "
            "and updated with each StreamTeX release. By extending it, "
            "you automatically benefit from improvements. Share common "
            "skills across profiles to avoid knowledge duplication."
        ))
    st_space("v", 1)
