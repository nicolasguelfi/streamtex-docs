"""Two Paths — zero-code vs code-first approaches to content creation."""


from streamtex import st_write, st_space, st_block, st_grid, st_list
from streamtex.enums import Tags as t
from streamtex.styles import Style
from custom.styles import Styles as s


class BlockStyles:
    """Two Paths block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle

    # Path cards
    path_zero = Style(
        "background: rgba(139, 92, 246, 0.06); "
        "border-left: 4px solid #8B5CF6; "
        "padding: 20px 24px; border-radius: 0 6px 6px 0;",
        "path_zero_code",
    )
    path_code = Style(
        "background: rgba(59, 130, 246, 0.06); "
        "border-left: 4px solid #3B82F6; "
        "padding: 20px 24px; border-radius: 0 6px 6px 0;",
        "path_code_first",
    )
    path_title_violet = s.project.colors.ai_violet + s.bold + s.Large
    path_title_blue = s.project.colors.tech_blue + s.bold + s.Large
    audience = s.project.colors.cyber_cyan + s.bold + s.large
    step_number = s.project.colors.ai_violet + s.bold + s.large
    step_text = s.large

    # Bottom note
    note_box = Style(
        "background: rgba(245, 158, 11, 0.08); "
        "border: 1px solid rgba(245, 158, 11, 0.25); "
        "border-radius: 8px; padding: 16px 20px; text-align: center;",
        "paths_note",
    )
    note_text = s.project.colors.warning_amber + s.bold + s.Large


bs = BlockStyles


def build():
    """Render the two paths to content creation."""
    st_space("v", 1)
    st_write(bs.heading, "Two Paths to Content Creation",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    # ── Side-by-side paths ────────────────────────────────────────
    with st_grid(cols=2) as g:
        # Left: Zero-Code Path
        with g.cell():
            with st_block(bs.path_zero):
                st_write(bs.path_title_violet, "Zero-Code Path", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.audience, "For educators, presenters, content creators",
                         tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ol") as l:
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Install a profile "),
                            "into your project",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Describe your project "),
                            "in plain language",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "AI generates everything "),
                            "— blocks, styles, book.py",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Review and refine "),
                            "the output",
                        )

        # Right: Code-First Path
        with g.cell():
            with st_block(bs.path_code):
                st_write(bs.path_title_blue, "Code-First Path", tag=t.div)
                st_space("v", 0.5)
                st_write(bs.audience, "For developers, library contributors",
                         tag=t.div)
                st_space("v", 1)
                with st_list(list_type="ol") as l:
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Read coding standards "),
                            "and the cheatsheet",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Write blocks manually "),
                            "with full control",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Use AI for audit/review "),
                            "— catch mistakes fast",
                        )
                    with l.item():
                        st_write(
                            bs.step_text,
                            (s.bold, "Custom extensions "),
                            "— new styles, helpers, themes",
                        )
    st_space("v", 2)

    # ── Bottom note ───────────────────────────────────────────────
    with st_block(bs.note_box):
        st_write(bs.note_text,
                 "Both paths can be combined",
                 tag=t.div)
        st_space("v", 0.5)
        st_write(
            s.large + s.center_txt,
            "Start with zero-code to prototype quickly, then switch to "
            "code-first for fine-tuning. Or write blocks by hand and use "
            "AI agents to audit your work.",
            tag=t.div,
        )
    st_space("v", 1)
