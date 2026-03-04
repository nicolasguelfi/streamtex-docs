"""Part 8 — FAQ & Troubleshooting — common questions and error resolution."""

from streamtex import st_write, st_space, st_block, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s
from blocks.helpers import show_explanation

class BlockStyles:
    """FAQ block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    question_card = Style(
        "background: rgba(59, 130, 246, 0.06); "
        "border-left: 3px solid #3B82F6; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "faq_question",
    )
    question_text = s.project.colors.tech_blue + s.bold + s.large
    answer_text = s.large

    error_card = Style(
        "background: rgba(239, 68, 68, 0.06); "
        "border-left: 3px solid #EF4444; "
        "padding: 16px 20px; border-radius: 0 6px 6px 0;",
        "faq_error",
    )
    error_title = s.project.colors.error_red + s.bold + s.large
    fix_label = s.project.colors.success_green + s.bold + s.large

bs = BlockStyles

def _render_qa(question, *answer_parts):
    """Render a question-answer pair in a styled card."""
    with st_block(bs.question_card):
        st_write(bs.question_text, question, tag=t.div)
        st_space("v", 1)
        st_write(bs.answer_text, *answer_parts)

def _render_error(error, *fix_parts):
    """Render a troubleshooting entry with error and fix."""
    with st_block(bs.error_card):
        st_write(bs.error_title, error, tag=t.div)
        st_space("v", 1)
        st_write(bs.fix_label, "Fix: ", tag=t.span)
        st_write(bs.answer_text, *fix_parts)

def build():
    """Render the FAQ and troubleshooting section."""
    st_space("v", 1)
    st_write(bs.heading, "FAQ & Troubleshooting", tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        Answers to the most common questions about using StreamTeX
        with AI assistants, followed by a troubleshooting guide
        for frequent errors.
    """)
    st_space("v", 2)

    # ── FAQ Section ───────────────────────────────────────────────
    st_write(bs.sub, "Frequently Asked Questions", toc_lvl="+1")
    st_space("v", 1)

    # Q1
    _render_qa(
        "Do I need Python to use StreamTeX with AI?",
        "Not for the zero-code path. You can describe your project "
        "in natural language and let the AI generate everything. "
        "However, if you want to customize blocks or write code-first "
        "content, Python 3.10+ is required.",
    )
    st_space("v", 1)

    # Q2
    _render_qa(
        "Which profile should I choose?",
        "Start with the ",
        (s.bold, "project"),
        " profile — it covers 90% of use cases "
        "with 20 commands and 3 agents. Choose ",
        (s.bold, "presentation"),
        " for live events, ",
        (s.bold, "documentation"),
        " for HTML migration workflows, or ",
        (s.bold, "library"),
        " if you contribute to the StreamTeX library itself.",
    )
    st_space("v", 1)

    # Q3
    _render_qa(
        "Can I use Cursor instead of Claude Code?",
        "Yes. StreamTeX profiles work with both ",
        (s.bold, "Claude Code"),
        " and ",
        (s.bold, "Cursor IDE"),
        ". For Cursor, profiles are adapted to use ",
        (s.bold, ".cursor/rules/"),
        " instead of ",
        (s.bold, ".claude/"),
        ". The commands, agents, "
        "and skills are identical in both environments.",
    )
    st_space("v", 1)

    # Q4
    _render_qa(
        "How do I update my profile?",
        "Use the ",
        (s.bold, "stx claude update"),
        " command to pull the latest profile "
        "version. Alternatively, use ",
        (s.bold, "stx claude diff"),
        " to see what "
        "changed before applying the update. This updates commands, "
        "agents, skills, and settings without affecting your content.",
    )
    st_space("v", 1)

    # Q5
    _render_qa(
        "Can I create custom commands?",
        "Yes. Add a .md file to the ",
        (s.bold, ".claude/commands/"),
        " directory in "
        "your project. The file name becomes the command name. Follow "
        "the standard structure: ",
        (s.bold, "description"),
        ", ",
        (s.bold, "context loading"),
        ", and a step-by-step ",
        (s.bold, "workflow"),
        ". Custom commands appear alongside "
        "built-in ones.",
    )
    st_space("v", 1)

    # Q6
    with st_block(bs.question_card):
        st_write(bs.question_text, "Why does my block not show up?", tag=t.div)
        st_space("v", 1)
        st_write(bs.answer_text, "Check three things:")
        with st_list(list_type="ol") as l:
            with l.item():
                st_write(bs.answer_text,
                         "The file name matches the ", (s.bold, "bck_*"), " pattern")
            with l.item():
                st_write(bs.answer_text,
                         "The file has a ", (s.bold, "build()"), " function at module level")
            with l.item():
                st_write(bs.answer_text,
                         "The block is registered in ", (s.bold, "book.py"))
        st_write(bs.answer_text,
                 "Also verify there are no import errors by running ",
                 (s.bold, "uv run ruff check"), ".")
    st_space("v", 1)

    # Q7
    _render_qa(
        "How do I reset AI context?",
        "Delete the .claude/memory/ directory and restart your Claude "
        "Code session. This clears all accumulated conversation context. "
        "The profile itself (commands, agents, skills) is not affected "
        "— only the session memory is cleared.",
    )
    st_space("v", 1)

    # Q8
    _render_qa(
        "Can I use multiple profiles?",
        "No. Each project uses exactly one profile at a time. Profiles "
        "support composition through the extends mechanism: the "
        "presentation profile extends project, which extends base. "
        "If you need features from two profiles, choose the one that "
        "extends the other.",
    )
    st_space("v", 2)

    # ── Troubleshooting Section ───────────────────────────────────
    st_write(bs.sub, "Troubleshooting", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Common errors and their solutions. If your issue is not listed
        here, check the StreamTeX developer manual or open an issue
        on the GitHub repository.
    """)
    st_space("v", 1)

    # Error 1
    _render_error(
        "ModuleNotFoundError: No module named 'streamtex'",
        "StreamTeX is not installed in the current environment. "
        "Run ", (s.bold, "uv add streamtex"), " or ",
        (s.bold, "pip install streamtex"), ". If using "
        "uv, make sure you prefix commands with ", (s.bold, "uv run"), ".",
    )
    st_space("v", 1)

    # Error 2
    _render_error(
        "ImportError: cannot import name 'st_write' from 'streamtex'",
        "Your StreamTeX version is outdated. Run uv add streamtex "
        "--upgrade to get the latest version.",
    )
    st_space("v", 1)

    # Error 3
    _render_error(
        "Block build() function not found",
        "Ensure your block file defines a build() function at the "
        "module level (not inside a class). The function must be "
        "named exactly build with no parameters.",
    )
    st_space("v", 1)

    # Error 4
    _render_error(
        "Style composition error: unsupported operand type",
        "You are trying to combine incompatible types. Use ",
        (s.bold, "Style + Style"),
        " for composition. If combining with a string, the "
        "string must be a valid CSS property. Check that both "
        "operands are ",
        (s.bold, "Style instances"), ".",
    )
    st_space("v", 1)

    # Error 5
    _render_error(
        "Command not found: /project:project-init",
        "The profile is not installed or the .claude/commands/ "
        "directory is missing. Run stx claude install to set up "
        "the profile, or verify the .md file exists in the "
        "commands directory.",
    )
    st_space("v", 1)

    # Error 6
    _render_error(
        "uv run: error: Failed to resolve requirements",
        "The lock file may reference a local path that does not "
        "exist. Run uv sync (without --frozen) to regenerate "
        "the lock file. In CI, set UV_NO_SOURCES=1 to ignore "
        "local source overrides.",
    )
    st_space("v", 1)
