"""Part 7 — MEMORY.md: persistent memory for AI assistants across sessions."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation


class BlockStyles:
    """MEMORY.md block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle


bs = BlockStyles


def build():
    """Persistent Memory with MEMORY.md — storage, conventions, and examples."""
    st_space("v", 1)
    st_write(bs.heading, "Persistent Memory with MEMORY.md",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        MEMORY.md is a file that persists across Claude Code sessions.
        It acts as long-term storage for decisions, conventions, and
        patterns that the AI should remember between conversations.
        Unlike CLAUDE.md which defines behavior rules, MEMORY.md
        stores accumulated project knowledge.
    """)
    st_space("v", 2)

    # ── Location ──────────────────────────────────────────────────
    st_write(bs.sub, "Where MEMORY.md Lives", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The memory file is stored inside the .claude directory,
        scoped to the specific project path. Claude Code reads
        it automatically at the start of every session.
    """)
    st_space("v", 1)

    show_code("""\
        .claude/
        └── projects/
            └── <project-path>/
                └── memory/
                    └── MEMORY.md""",
        language="bash", line_numbers=False)
    st_space("v", 2)

    # ── What to store ─────────────────────────────────────────────
    st_write(bs.sub, "What to Store", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(s.project.titles.subsection_title, "GOOD: Store These")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, (s.bold, "Project conventions"), " and naming patterns")
            with l.item(): st_write(s.large, (s.bold, "Color palette"), " and typography decisions")
            with l.item(): st_write(s.large, (s.bold, "Architecture decisions"), " and rationale")
            with l.item(): st_write(s.large, (s.bold, "Recurring patterns"), " discovered during development")
            with l.item(): st_write(s.large, (s.bold, "Infrastructure details"), " (service IDs, URLs, ports)")
            with l.item(): st_write(s.large, (s.bold, "Known gotchas"), " and workarounds")
    st_space("v", 2)

    # ── What NOT to store ─────────────────────────────────────────
    st_write(bs.sub, "What NOT to Store", toc_lvl="+1")
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(s.project.colors.error_red + s.bold, "AVOID: Do Not Store These")
        st_space("v", 1)
        with st_list(list_type="ul") as l:
            with l.item(): st_write(s.large, (s.bold, "Session-specific context"), " or temporary state")
            with l.item(): st_write(s.large, (s.bold, "Duplicates"), " of what is already in CLAUDE.md")
            with l.item(): st_write(s.large, (s.bold, "Secrets"), ", API keys, or credentials")
            with l.item(): st_write(s.large, (s.bold, "Verbose logs"), " or debug output")
            with l.item(): st_write(s.large, (s.bold, "Information that changes"), " every session")
    st_space("v", 2)

    # ── Example ───────────────────────────────────────────────────
    st_write(bs.sub, "Example MEMORY.md", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Here is a real-world example of a MEMORY.md file for a
        StreamTeX documentation workspace. Notice how it captures
        infrastructure details, service mappings, and key decisions.
    """)
    st_space("v", 1)

    show_code("""\
        # StreamTeX Ecosystem — Claude Memory

        ## Workspace Layout
        ```
        streamtex-dev/
          streamtex/          # Library (PyPI: streamtex)
          streamtex-docs/     # Documentation (5 manuals)
          streamtex-claude/   # Claude profiles
        ```

        ## Infrastructure Essentials

        ### The UV_NO_SOURCES Problem
        - pyproject.toml has local editable source
        - CI fix: UV_NO_SOURCES=1 as env var
        - Docker fix: uv sync --no-sources

        ### Render Services
        | Name | ID | Port |
        |------|----|------|
        | streamtex-intro | srv-abc123 | 8502 |
        | streamtex-advanced | srv-def456 | 8503 |

        ## Key Decisions
        - All manuals share one Dockerfile
        - FOLDER env var selects which manual to serve""",
        language="markdown")
    st_space("v", 2)

    # ── Tip ───────────────────────────────────────────────────────
    with st_block(s.project.containers.tip_callout):
        st_write(s.project.titles.tip_label, "Tip: Keep It Concise")
        st_space("v", 1)
        st_write(s.large, (
            "MEMORY.md is truncated after approximately 200 lines. "
            "Keep entries concise and well-structured. Use tables for "
            "repetitive data, remove outdated entries regularly, and "
            "prefer bullet points over paragraphs."
        ))
    st_space("v", 1)
