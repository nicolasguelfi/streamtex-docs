"""Best Practices — Writing effective descriptions for AI commands."""

from streamtex import st_write, st_space, st_block, st_grid
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_explanation, show_details

class BlockStyles:
    """Effective prompting block styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    tip_number = s.project.colors.ai_violet + s.bold + s.large
    bad_label = s.project.colors.error_red + s.bold + s.large
    good_label = s.project.colors.success_green + s.bold + s.large

bs = BlockStyles

def build():
    """Render the Effective Prompting best practices section."""
    st_space("v", 1)
    st_write(bs.heading, "Writing Effective Descriptions",
             tag=t.div, toc_lvl="1")
    st_space("v", 2)

    show_explanation("""\
        The quality of AI-generated output depends directly on the
        quality of your descriptions. A precise, context-rich prompt
        saves iterations and produces better blocks from the first pass.
    """)
    st_space("v", 2)

    # ── 5 Tips ────────────────────────────────────────────────────
    st_write(bs.sub, "Five Tips for Better Prompts", toc_lvl="+1")
    st_space("v", 1)

    # Tip 1
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.tip_number, "1. Be specific about content",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            'Say ',
            (s.bold, '"10-slide course on Python basics"'),
            ' instead of ',
            (s.bold, '"make a course"'),
            '. Include the number of slides, the topic scope, and '
            'the depth of coverage you expect.',
        )
    st_space("v", 1)

    # Tip 2
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.tip_number, "2. Mention the audience",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            'A course ',
            (s.bold, '"for university students"'),
            ' differs significantly from one ',
            (s.bold, '"for a conference keynote"'),
            '. The audience drives vocabulary, depth, and visual density.',
        )
    st_space("v", 1)

    # Tip 3
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.tip_number, "3. Specify visual preferences",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            'Include theme direction: ',
            (s.bold, '"dark theme, blue palette, minimal design"'),
            '. This helps the AI generate appropriate Style objects '
            'and color choices from the start.',
        )
    st_space("v", 1)

    # Tip 4
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.tip_number, "4. Include structure hints",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            'Describe the sections you want: ',
            (s.bold, '"3 sections: intro, main content, conclusion"'),
            '. This gives the AI a skeleton to build on rather than '
            'inventing the structure from scratch.',
        )
    st_space("v", 1)

    # Tip 5
    with st_block(s.project.containers.tip_callout):
        st_write(
            bs.tip_number, "5. Reference existing work",
            tag=t.div,
        )
        st_space("v", 1)
        st_write(
            s.large,
            'Point to examples: ',
            (s.bold, '"similar to stx_manual_intro style"'),
            '. The AI can read existing blocks and replicate their '
            'patterns, spacing, and visual conventions.',
        )
    st_space("v", 2)

    # ── Bad vs Good examples ─────────────────────────────────────
    st_write(bs.sub, "Bad vs Good Prompts", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        The following examples illustrate how adding context transforms
        a vague request into an actionable description that produces
        high-quality output on the first attempt.
    """)
    st_space("v", 1)

    # Example 1
    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(bs.bad_label, "Bad", tag=t.div)
                st_space("v", 1)
                st_write(s.large, '"Make slides"')
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.good_label, "Good", tag=t.div)
                st_space("v", 1)
                st_write(
                    s.large,
                    '"Create 8 slides about REST APIs for backend developers"',
                )
    st_space("v", 1)

    # Example 2
    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(bs.bad_label, "Bad", tag=t.div)
                st_space("v", 1)
                st_write(s.large, '"Fix the style"')
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.good_label, "Good", tag=t.div)
                st_space("v", 1)
                st_write(
                    s.large,
                    '"Refactor inline CSS in bck_03 to use Style objects '
                    'from BlockStyles"',
                )
    st_space("v", 1)

    # Example 3
    with st_grid(cols=2) as g:
        with g.cell():
            with st_block(s.project.containers.bad_callout):
                st_write(bs.bad_label, "Bad", tag=t.div)
                st_space("v", 1)
                st_write(s.large, '"Add content"')
        with g.cell():
            with st_block(s.project.containers.good_callout):
                st_write(bs.good_label, "Good", tag=t.div)
                st_space("v", 1)
                st_write(
                    s.large,
                    '"Add a comparison grid showing Python vs JavaScript '
                    'syntax for loops"',
                )
    st_space("v", 2)

    # ── Final tip ─────────────────────────────────────────────────
    show_details("""\
        Tip: the more context you give, the fewer iterations you need.
        A well-crafted prompt with audience, scope, structure, and visual
        preferences typically produces a usable block in a single pass.
        A vague prompt may require 3-5 rounds of refinement.
    """)
    st_space("v", 1)
