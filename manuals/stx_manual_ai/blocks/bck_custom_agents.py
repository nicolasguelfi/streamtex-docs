"""Part 7 — Creating custom agents: autonomous, multi-step AI assistants."""

import textwrap
from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Custom agents block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Creating Custom Agents — structure, principles, and examples."""
    st_space("v", 1)
    st_write(bs.heading, "Creating Custom Agents",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation(textwrap.dedent("""\
        Agents are autonomous AI assistants that can execute multi-step
        workflows without constant user guidance. Unlike commands which
        follow a fixed script, agents make decisions, adapt to context,
        and operate according to a set of principles.
    """))
    st_space("v", 2)

    # ── Agent vs Command ──────────────────────────────────────────
    st_write(bs.sub, "Agent vs Command", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "Agent")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, "Autonomous — makes decisions independently")
            st_write(s.large, "Multi-step — chains several operations")
            st_write(s.large, "Context-aware — reads skills and adapts")
            st_write(s.large, "Principle-driven — follows guiding rules")
            st_write(s.large, "Best for: complex creative or structural tasks")
    st_space("v", 1)

    with st_block(s.project.containers.note_callout):
        st_write(s.project.titles.warning_label, "Command")
        st_space("v", 1)
        with st_list(list_type="ul"):
            st_write(s.large, "Scripted — follows a fixed step sequence")
            st_write(s.large, "Single-task — one clearly defined outcome")
            st_write(s.large, "User-guided — may ask questions at each step")
            st_write(s.large, "Template-driven — produces predictable output")
            st_write(s.large, "Best for: repetitive, well-defined tasks")
    st_space("v", 2)

    # ── File structure ────────────────────────────────────────────
    st_write(bs.sub, "Agent File Structure", toc_lvl="+1")
    st_space("v", 1)

    show_explanation(textwrap.dedent("""\
        Agent files live in a role-specific directory under .claude/.
        The role name (e.g., "architect", "designer") scopes the agent
        to a particular domain of expertise.
    """))
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        .claude/
        ├── architect/
        │   └── agents/
        │       └── architect-agent.md
        ├── designer/
        │   └── agents/
        │       ├── slide-designer-agent.md
        │       └── presentation-designer-agent.md
        └── developer/
            └── agents/
                └── developer-agent.md"""),
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── Required sections ─────────────────────────────────────────
    st_write(bs.sub, "Required Sections", toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type="ul"):
        st_write(s.large, (
            (s.bold, "Role"), " — define who the agent is and its specialization"
        ))
        st_write(s.large, (
            (s.bold, "Context"), " — list skills and reference files to read"
        ))
        st_write(s.large, (
            (s.bold, "Workflow"), " — describe the multi-step process the agent follows"
        ))
        st_write(s.large, (
            (s.bold, "Principles"), " — guiding rules the agent must always respect"
        ))
    st_space("v", 2)

    # ── Example agent ─────────────────────────────────────────────
    st_write(bs.sub, "Example: Custom Agent File", toc_lvl="+1")
    st_space("v", 1)

    show_code(textwrap.dedent("""\
        # Agent: Quality Reviewer

        ## Role
        You are a StreamTeX Quality Reviewer. You audit block files
        for coding standard compliance, style consistency, and
        accessibility. You work autonomously and produce a report.

        ## Context
        Before starting, read the following skills:
        1. `.claude/skills/coding_standards.md`
        2. `.claude/skills/streamtex_api.md`
        3. `.claude/skills/style_guide.md`

        ## Workflow
        1. List all block files in the target manual's blocks/ directory
        2. For each block file:
           a. Check imports follow the standard pattern
           b. Verify BlockStyles class exists with heading and sub
           c. Verify build() function exists and is properly documented
           d. Check all st_write calls use Style objects (no raw strings)
           e. Verify no raw st.markdown or st.write calls
        3. Generate a report with findings grouped by severity
        4. Suggest fixes for each issue found

        ## Principles
        - Never modify files — only read and report
        - Flag issues but do not auto-fix without user approval
        - Prioritize accessibility issues over style preferences
        - Be specific: include file name, line number, and fix suggestion
        - If all blocks pass, confirm compliance explicitly"""),
        language="markdown")
    st_space("v", 2)

    # ── Tips ──────────────────────────────────────────────────────
    show_details(textwrap.dedent("""\
        Define clear principles that constrain the agent's behavior.
        Without principles, agents may take unexpected actions. Reference
        specific skills in the Context section so the agent has domain
        knowledge without you repeating it. Set explicit constraints
        like "never modify files" or "always ask before deleting" to
        keep the agent safe and predictable.
    """))
    st_space("v", 1)
