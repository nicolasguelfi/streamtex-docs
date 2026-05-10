"""Extrapolation contract — INVARIANTS / PARAMS / INTERDITS.

# @pattern: ptn_manual_section
"""

from streamtex import *
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Extrapolation page styles."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    body = s.large
    invariant_label = s.bold + s.project.colors.warning_red
    params_label = s.bold + s.project.colors.success_green
    interdits_label = s.bold + s.project.colors.warning_red


bs = BlockStyles


def build():
    """Document the extrapolation contract that drives AI generation."""
    with st_block(s.center_txt):
        st_write(bs.heading, "Extrapolation Contract",
                 tag=t.div, toc_lvl="1")
        st_space("v", 2)

    # ---- Why three categories ----
    st_write(bs.sub, "Three categories, one contract", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        When Claude Code generates a block from a pattern, it never
        copy-pastes the skeleton verbatim. It **extrapolates**: same
        structure, project-specific palette, project-specific content.

        To bound that freedom, every pattern declares three categories
        of rules — the **extrapolation contract** — under
        `## Extrapolation rules`.
    """)
    st_space("v", 2)

    # ---- INVARIANTS ----
    st_write(bs.sub, "INVARIANTS — never change", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Properties of the pattern that, if violated, break the
        identity of the pattern itself. Examples: a `manual_section`
        always has the **explanation → code → demo** triad in that
        order; a `feature_walkthrough` always has **numbered** steps.
    """)
    st_space("v", 1)

    show_code("""\
### INVARIANTS (never change)

- The triad is **explanation → code → demo**, in that order.
- `show_code` displays the exact same code that the live demo executes.
- The section has one heading at `toc_lvl="1"` and sub-topics at
  `toc_lvl="+1"`. The TOC structure must follow.
- Helpers (`show_code`, `show_explanation`, `show_details`) are imported
  from the manual's helper module, never inlined.""", language="markdown")
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(bs.invariant_label, "Hard rule")
        st_space("v", 0.5)
        st_write(bs.body,
                 "An AI generator that breaks an INVARIANT is not "
                 "applying the pattern — it is producing something else. "
                 "Reviewers should reject the output.")
    st_space("v", 2)

    # ---- PARAMS ----
    st_write(bs.sub, "PARAMS — adjustable", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Knobs the AI is allowed to turn. PARAMS list the dimensions
        of variation a pattern accepts: number of sub-topics, optional
        sections, alternative cell styles, density.
    """)
    st_space("v", 1)

    show_code("""\
### PARAMS (adjustable)

- Number of sub-topics: 1 to ~5 per section.
- `show_details` may be added between explanation and code for an
  expandable deeper-dive (rare).
- The cell style for demos may vary (`solid_border` vs
  `dashed_border`, padding size).
- A sub-topic may **omit the live demo** when the code only
  illustrates syntax that doesn't render (e.g. configuration in
  `book.py`).""", language="markdown")
    st_space("v", 1)

    with st_block(s.project.containers.good_callout):
        st_write(bs.params_label, "Design space")
        st_space("v", 0.5)
        st_write(bs.body,
                 "PARAMS define the **legal design space**. The AI may "
                 "freely combine PARAMS to fit the project's tone, but "
                 "must not invent new dimensions outside this list.")
    st_space("v", 2)

    # ---- INTERDITS ----
    st_write(bs.sub, "INTERDITS — forbidden", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Anti-patterns specific to this pattern. INTERDITS are how an
        author warns: "I know you might be tempted to do X — don't."

        They are usually **scope violations** (using a slide pattern
        in a manual), **DRY violations**, or **visual conflicts**.
    """)
    st_space("v", 1)

    show_code("""\
### INTERDITS (forbidden)

- Do not put the live demo before the code — the reader needs to know
  what they are about to see.
- Do not skip the explanation — even a one-line explanation anchors
  the reader.
- Do not duplicate `show_code` snippets for the same demo (DRY at the
  reader level — one snippet, one demo).
- Do not use slide-presentation patterns (`stat_hero`,
  `evidence_insight`) in a manual section.""", language="markdown")
    st_space("v", 1)

    with st_block(s.project.containers.bad_callout):
        st_write(bs.interdits_label, "Frontier")
        st_space("v", 0.5)
        st_write(bs.body,
                 "INTERDITS protect the boundary between scopes "
                 "(slides vs docs vs core). They are the most "
                 "important section for reviewers to read.")
    st_space("v", 2)

    # ---- How AI consumes the contract ----
    st_write(bs.sub, "How Claude Code uses the contract", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        At block-generation time, Claude Code:

        1. Reads `_pattern_library.md` to discover available patterns.
        2. If the user references a pattern by name (or a slash command
           like `/stx-pattern:apply manual_section`), reads the full
           markdown of that pattern.
        3. Uses **Code skeleton** as a starting point.
        4. Applies **PARAMS** to the project's palette and content.
        5. Verifies the output against **INVARIANTS** (self-check).
        6. Avoids every pattern in **INTERDITS**.

        The `# @pattern: <name>` annotation at the top of a generated
        block records which pattern produced it — useful for audits.
    """)
    st_space("v", 1)

    show_details("""\
        For ambiguity (e.g. a project where `manual_section` and
        `feature_walkthrough` could both fit), the AI defaults to the
        pattern most explicitly named by the user, falling back to the
        one whose **When to use** section best matches the request.
    """)
    st_space("v", 1)
