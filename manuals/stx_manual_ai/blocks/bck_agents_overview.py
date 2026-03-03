"""Part 4 — AI Agents Overview: commands vs agents, the four agents."""

import textwrap
from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Agents overview block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Agent card style
    agent_card = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 3px solid #8B5CF6; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "agent_card",
    )
    agent_name = s.project.colors.ai_violet + s.bold + s.Large
    agent_desc = s.large


bs = BlockStyles


def build():
    """Render the AI Agents overview section."""
    st_space("v", 1)
    st_write(bs.heading, "AI Agents Overview", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Command vs Agent ───────────────────────────────────────────
    st_write(bs.sub, "Command vs Agent", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.tip_callout):
                st_write(
                    s.project.titles.subsection_title, "Command",
                    tag=t.div,
                )
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item():
                        st_write(
                            s.large,
                            (s.bold, "Single task, "),
                            "user-triggered",
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Invoked with ",
                            (s.bold, "/command-name"),
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Executes one focused action and stops",
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Example: ",
                            (s.bold, "/block-new"),
                            " creates one block file",
                        )

        with g.cell():
            with st_block(s.project.containers.ai_callout):
                st_write(
                    s.project.titles.subsection_title, "Agent",
                    tag=t.div,
                )
                st_space("v", 1)
                with st_list(list_type="ul") as l:
                    with l.item():
                        st_write(
                            s.large,
                            (s.bold, "Autonomous "),
                            "multi-step workflow",
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Reads context, makes decisions, iterates",
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Orchestrates multiple commands in sequence",
                        )
                    with l.item():
                        st_write(
                            s.large,
                            "Example: ",
                            (s.bold, "Project Architect"),
                            " designs an entire project",
                        )
    st_space("v", 2)

    show_explanation("""\
        Think of commands as tools and agents as craftspeople.
        A command does one thing well. An agent decides which
        commands to use, in what order, and adapts based on
        the results.
    """)
    st_space("v", 2)

    # ── The four agents ────────────────────────────────────────────
    st_write(bs.sub, "The Four Agents", toc_lvl="+1")
    st_space("v", 1)

    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Project Architect", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.agent_desc, textwrap.dedent("""\
                    Designs full project structure from a natural
                    language description. Creates block plan, color
                    palette, and feature list.
                """))
        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Slide Designer", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.agent_desc, textwrap.dedent("""\
                    Creates visually polished, pedagogically
                    structured blocks. Enforces formatting rules
                    and detects anti-patterns.
                """))
        with g.cell():
            with st_block(bs.agent_card):
                st_write(bs.agent_name, "Slide Reviewer", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.agent_desc, textwrap.dedent("""\
                    Reviews completed slides for compliance.
                    Checks structure, visual quality, pedagogy,
                    and formatting. Returns pass/fail per criterion.
                """))
        with g.cell():
            with st_block(bs.agent_card):
                st_write(
                    bs.agent_name, "Presentation Designer", tag=t.div,
                )
                st_space("v", 0.5)
                st_write(bs.agent_desc, textwrap.dedent("""\
                    Specialist for live projection slides.
                    Uses larger fonts, fewer items, and high
                    contrast for viewing at 10-20 meters.
                """))
    st_space("v", 2)

    # ── How agents are defined ─────────────────────────────────────
    st_write(bs.sub, "How Agents Are Defined", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Each agent is a Markdown file stored in the profile's agents
        directory. When invoked, the agent automatically loads its
        context — coding standards, skills, and design rules — before
        performing any action.
    """)
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        .claude/
          designer/
            agents/
              project-architect.md
              slide-designer.md
              slide-reviewer.md
          presentation/
            agents/
              presentation-designer.md
    """), language="text", line_numbers=False)
    st_space("v", 1)

    show_details("""\
        Agents auto-load their context before acting. This means
        they read the relevant skills, coding standards, and
        blueprints defined in the profile so that every generated
        block is standards-compliant from the start. You never
        need to manually paste rules into the conversation.
    """)
    st_space("v", 1)
