"""Semantic HTML tags enum for content structure.

This block explains the Tags enum used in StreamTeX for semantic markup.
Tags help create properly structured HTML with semantic meaning.
"""

from streamtex import st_write, st_list, st_space
from streamtex.enums import Tags as t
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


def build():
    """Build the Tags enum documentation block."""

    st_write(s.project.titles.page_title, "Semantic Tags (HTML Markup)", tag=t.h1, toc_lvl="1")
    st_space("v", 1)

    show_explanation("""
The Tags enum provides semantic HTML tags for proper document structure.

Use tags to mark headings, paragraphs, and inline elements correctly.

Tags also control table of contents generation in StreamTeX.
    """)

    # ========================================================================
    # HEADING TAGS
    # ========================================================================
    st_write(s.project.titles.section_title, "Heading Tags (h1-h6)", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""
Use heading tags to structure your document hierarchically.

H1 is the main title, h2-h6 are subsections.

In StreamTeX, heading tags automatically update the table of contents.
    """)

    st_write(s.project.titles.feature_title, "Available heading tags:")
    show_code("""
from streamtex import st_write
from streamtex.enums import Tags as t

st_write(s.title, "Main Title", tag=t.h1)
st_write(s.subtitle, "Section", tag=t.h2)
st_write(s.large, "Subsection", tag=t.h3)
# ... h4, h5, h6 also available
    """, language="python")

    st_write(s.project.titles.feature_title, "With Table of Contents:")
    show_code("""
# Tags + toc_lvl update the TOC automatically
st_write(s.title, "Chapter", tag=t.h1, toc_lvl="1")
st_write(s.subtitle, "Section", tag=t.h2, toc_lvl="+1")
st_write(s.large, "Subsection", tag=t.h3, toc_lvl="+1")
    """, language="python")

    st_space("v", 2)

    # ========================================================================
    # BLOCK TAGS
    # ========================================================================
    st_write(s.project.titles.section_title, "Block Tags (paragraph, div)", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""
Block tags structure content into paragraphs and sections.

p = paragraph (single block of text)

div = generic container (can hold multiple elements)
    """)

    st_write(s.project.titles.feature_title, "Usage:")
    show_code("""
from streamtex.enums import Tags as t

# Single paragraph
st_write(s.large, "This is a paragraph.", tag=t.p)

# Generic container (usually implicit in st_block)
st_write(s.large, "Container content", tag=t.div)
    """, language="python")

    st_space("v", 2)

    # ========================================================================
    # INLINE TAGS
    # ========================================================================
    st_write(s.project.titles.section_title, "Inline Tags (span)", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""
Inline tags mark content within text without line breaks.

span = generic inline container

Used with tuple syntax in st_write() for mixed-style text.
    """)

    st_write(s.project.titles.feature_title, "Usage with mixed styles:")
    show_code("""
from streamtex.enums import Tags as t

# Inline text with mixed styling
st_write(s.large,
    (s.bold, "Important: "),
    "Regular text continues here.",
    (s.color_red, "Error message"),
    tag=t.span
)
    """, language="python")

    st_space("v", 2)

    # ========================================================================
    # ALL AVAILABLE TAGS
    # ========================================================================
    st_write(s.project.titles.section_title, "Complete Tag Reference", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large + s.bold, "Heading Tags:")
    with st_list(li_style=s.large, list_type="ul") as l:
        with l.item(): st_write("h1: Main page title")
        with l.item(): st_write("h2: Section heading")
        with l.item(): st_write("h3-h6: Subsection headings")

    st_space("v", 1)

    st_write(s.large + s.bold, "Block Tags:")
    with st_list(li_style=s.large, list_type="ul") as l:
        with l.item(): st_write("p: Paragraph")
        with l.item(): st_write("div: Generic container")

    st_space("v", 1)

    st_write(s.large + s.bold, "Inline Tags:")
    with st_list(li_style=s.large, list_type="ul") as l:
        with l.item(): st_write("span: Inline container")

    st_space("v", 1)

    st_write(s.large + s.bold, "Special:")
    with st_list(li_style=s.large, list_type="ul") as l:
        with l.item(): st_write("None: No semantic tag (default)")

    st_space("v", 2)

    # ========================================================================
    # INTEGRATION WITH TOC
    # ========================================================================
    st_write(s.project.titles.section_title, "Tags + Table of Contents", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""
Tags work with toc_lvl parameter to auto-generate table of contents.

The TOC shows all h1-h6 headings in hierarchical structure.

StreamTeX automatically numbers and links headings.
    """)

    st_write(s.project.titles.feature_title, "Complete example:")
    show_code("""
from streamtex import st_write, TOCConfig, st_toc
from streamtex.enums import Tags as t

# Configure TOC
toc_config = TOCConfig(numerate_titles=True, sidebar_max_level=2)

# Your content with tags and toc_lvl
st_write(s.title, "Chapter 1", tag=t.h1, toc_lvl="1")
st_write(s.subtitle, "Section 1.1", tag=t.h2, toc_lvl="+1")
st_write(s.large, "Content here...", tag=t.p)

st_write(s.subtitle, "Section 1.2", tag=t.h2, toc_lvl="=1")
st_write(s.large, "More content...", tag=t.p)

# TOC is auto-generated!
st_toc(toc_config)
    """, language="python")

    st_space("v", 2)

    # ========================================================================
    # SEMANTIC MEANING
    # ========================================================================
    st_write(s.project.titles.section_title, "Why Semantic Tags Matter", toc_lvl="+1")
    st_space("v", 1)

    st_write(s.large + s.bold, "Benefits of semantic tags:")
    with st_list(li_style=s.large, list_type="ol") as l:
        with l.item(): st_write((s.bold, "Accessibility"), ": Screen readers understand document structure")
        with l.item(): st_write((s.bold, "SEO"), ": Search engines recognize proper heading hierarchy")
        with l.item(): st_write((s.bold, "Structure"), ": TOC generation works correctly")
        with l.item(): st_write((s.bold, "Styling"), ": CSS can target semantic elements")
        with l.item(): st_write((s.bold, "Readability"), ": Humans understand document organization")

    st_space("v", 1)

    st_write(s.large + s.bold, "Best practices:")
    with st_list(li_style=s.large, list_type="ul") as l:
        with l.item(): st_write("Use h1 for main page title (only one per page)")
        with l.item(): st_write("Use h2+ for section hierarchy")
        with l.item(): st_write("Don't skip heading levels (h1 → h3 is bad)")
        with l.item(): st_write("Use p for paragraphs")
        with l.item(): st_write("Use span for inline styling only")

    st_space("v", 2)

    # ========================================================================
    # COMMON MISTAKES
    # ========================================================================
    st_write(s.project.titles.section_title, "Common Mistakes to Avoid", toc_lvl="+1")
    st_space("v", 1)

    show_details("""
Multiple h1 tags
- Wrong: Use multiple h1 on same page
- Right: Use only one h1, rest are h2-h6

Skipping heading levels
- Wrong: h1 → h3 → h4 (skip h2)
- Right: h1 → h2 → h3 (sequential)

Wrong tag for styling
- Wrong: st_write(s.bold, "Title", tag=t.span)
- Right: st_write(s.bold, "Title", tag=t.h2)

Forgetting toc_lvl
- Wrong: st_write(s.title, "Section", tag=t.h2)
- Right: st_write(s.title, "Section", tag=t.h2, toc_lvl="+1")
    """)
