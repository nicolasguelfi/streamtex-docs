"""Part 7 — Creating custom commands for Claude Code."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Custom commands block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    step_label = s.project.colors.ai_violet + s.bold + s.large


bs = BlockStyles


def build():
    """Creating Custom Commands — structure, conventions, and examples."""
    st_space("v", 1)
    st_write(bs.heading, "Creating Custom Commands",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Custom commands let you teach Claude Code new workflows
        specific to your project. Each command is a Markdown file
        that describes a task, the context to load, and the steps
        to follow.
    """)
    st_space("v", 2)

    # ── File structure ────────────────────────────────────────────
    st_write(bs.sub, "Command File Structure", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Commands live in .claude/commands/ organized by category.
        Each .md file becomes a slash command that users can invoke
        in Claude Code.
    """)
    st_space("v", 1)

    show_code("""\
        .claude/
        └── commands/
            ├── project/
            │   ├── project-init.md
            │   ├── project-customize.md
            │   └── course-generate.md
            ├── designer/
            │   ├── block-new.md
            │   ├── slide-new.md
            │   └── styles-update.md
            └── developer/
                ├── test-run.md
                └── lint.md""",
        language="bash", line_numbers=False)
    st_space("v", 1)

    show_explanation("""\
        The directory name becomes the command prefix.
        For example, designer/block-new.md is invoked as
        /designer:block-new in Claude Code.
    """)
    st_space("v", 2)

    # ── Required sections ─────────────────────────────────────────
    st_write(bs.sub, "Required Sections in a Command File",
             toc_lvl="+1")
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(s.large, (
                (s.bold, "Description"), " — what the command does and when to use it"
            ))
        with l.item():
            st_write(s.large, (
                (s.bold, "Context Loading"), " — which files the AI must read first"
            ))
        with l.item():
            st_write(s.large, (
                (s.bold, "Workflow"), " — step-by-step instructions the AI follows"
            ))
    st_space("v", 2)

    # ── Step-by-step creation ─────────────────────────────────────
    st_write(bs.sub, "Step-by-Step Creation", toc_lvl="+1")
    st_space("v", 1)

    # Step 1
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label,
                 "Step 1 — Create the category directory", tag=t.div)
        st_space("v", 1)
        st_write(s.large,
                 "Choose a category name that groups related commands.")
    st_space("v", 1)

    show_code("mkdir -p .claude/commands/my-category",
              language="bash", line_numbers=False)
    st_space("v", 1)

    # Step 2
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label,
                 "Step 2 — Write the .md file with structured sections",
                 tag=t.div)
        st_space("v", 1)
        st_write(s.large,
                 "Use the template below as a starting point.")
    st_space("v", 1)

    # Step 3
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label,
                 "Step 3 — Define context files to load", tag=t.div)
        st_space("v", 1)
        st_write(s.large, (
            "List the files the AI must read before executing. "
            "This ensures it has the right knowledge."
        ))
    st_space("v", 1)

    # Step 4
    with st_block(s.project.containers.tip_callout):
        st_write(bs.step_label,
                 "Step 4 — Write the step-by-step workflow", tag=t.div)
        st_space("v", 1)
        st_write(s.large, (
            "Number each step clearly. Be explicit about what "
            "the AI should produce at each stage."
        ))
    st_space("v", 2)

    # ── Example command ───────────────────────────────────────────
    st_write(bs.sub, "Example: Custom Command File", toc_lvl="+1")
    st_space("v", 1)

    show_code("""\
        # Command: block-new

        ## Description
        Create a new StreamTeX block file from a topic description.
        The block follows project coding standards and integrates
        with the existing book structure.

        ## Context Loading
        Before executing, read the following files:
        1. `.claude/references/coding_standards.md`
        2. `.claude/references/streamtex_cheatsheet_en.md`
        3. The target manual's `book.py`
        4. The manual's `blocks/helpers.py`
        5. An existing block in the same manual (for style reference)

        ## Workflow
        1. Ask the user for the block topic and target manual
        2. Read context files listed above
        3. Determine the next block number from book.py
        4. Generate the block file following BlockStyles + build() pattern
        5. Register the block in book.py
        6. Run `uv run ruff check` on the new file
        7. Show the user a summary of what was created""",
        language="markdown")
    st_space("v", 2)

    # ── Tips ──────────────────────────────────────────────────────
    show_details("""\
        Keep commands focused on one task. A command that tries to do
        too much becomes unreliable. If you need a multi-task workflow,
        create an agent instead. Reference skills in the context loading
        section so the AI has the knowledge it needs without duplicating
        documentation inside the command file.
    """)
    st_space("v", 1)
