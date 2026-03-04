"""LaTeX Documents — full document rendering with st_latex_doc()."""

import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details


class BlockStyles:
    """Styles for LaTeX Documents block."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
    param_label = s.medium + s.text.weights.bold_weight


bs = BlockStyles


def build():
    """Demonstrate st_latex_doc() for rendering full LaTeX documents."""

    st_write(bs.heading, "LaTeX Documents \u2014 st_latex_doc", tag=t.h1, toc_lvl="1")
    st_space("v", 2)

    # --- Introduction ---
    show_explanation("""\
        StreamTeX provides two distinct LaTeX rendering functions:

        - **st_latex()** renders isolated math formulas using Streamlit's
          native KaTeX engine. Fast and lightweight, but math only.
        - **st_latex_doc()** renders full LaTeX documents and fragments
          using LaTeX.js in an iframe. Supports sections, lists, tables,
          math environments, and all standard LaTeX formatting.

        Use st_latex_doc() when you need more than math \u2014 structured
        documents, course notes, articles, or any content that relies on
        LaTeX's document model.
    """)
    st_space("v", 2)

    # --- Section 1: Basic Usage ---
    st_write(bs.sub, "Basic Usage", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Pass a raw LaTeX string to st_latex_doc(). If the string contains
        a \\\\documentclass declaration, it is sent to LaTeX.js as-is.
        Otherwise, StreamTeX auto-wraps the fragment in a minimal
        article document.
    """)
    st_space("v", 1)

    show_code("""\
        st_latex_doc(r\"\"\"
        \\\\documentclass{article}
        \\\\begin{document}
        \\\\section{Introduction}
        Hello from LaTeX!
        \\\\end{document}
        \"\"\")""")
    st_space("v", 1)

    with st_block(s.project.containers.result_box):
        stx.st_latex_doc(r"""
\documentclass{article}
\begin{document}
\section{Introduction}
Hello from LaTeX!
\end{document}
""", height=180, light_bg=True)
    st_space("v", 2)

    # --- Section 2: Fragment Wrapping ---
    st_write(bs.sub, "Fragment Wrapping", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        When no \\\\documentclass is present, StreamTeX automatically wraps
        the content in a minimal article document. This lets you write
        LaTeX fragments without boilerplate.
    """)
    st_space("v", 1)

    show_code("""\
        # No \\\\documentclass needed — StreamTeX wraps it automatically
        st_latex_doc(r\"\"\"
        \\\\section{Quick Note}
        This fragment is auto-wrapped in an article document.
        Supports \\\\textbf{bold}, \\\\emph{italic}, and math: $E = mc^2$.
        \"\"\", height=180)""")
    st_space("v", 1)

    with st_block(s.project.containers.result_box):
        stx.st_latex_doc(r"""
\section{Quick Note}
This fragment is auto-wrapped in an article document.
Supports \textbf{bold}, \emph{italic}, and math: $E = mc^2$.
""", height=180, light_bg=True)
    st_space("v", 2)

    # --- Section 3: Parameters ---
    st_write(bs.sub, "Parameters", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        st_latex_doc() accepts several parameters to control rendering:
    """)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item(): st_write(s.medium, (bs.param_label, "style"), " \u2014 optional Style wrapper for the container")
        with l.item(): st_write(s.medium, (bs.param_label, "light_bg"), " \u2014 True for white background (default), False for dark/transparent")
        with l.item(): st_write(s.medium, (bs.param_label, "height"), " \u2014 iframe height in pixels (default 600)")
        with l.item(): st_write(s.medium, (bs.param_label, "hyphenate"), " \u2014 True for LaTeX.js hyphenation (default True)")
        with l.item(): st_write(s.medium, (bs.param_label, "file"), " \u2014 path to a .tex file (resolved via static assets)")
        with l.item(): st_write(s.medium, (bs.param_label, "encoding"), " \u2014 file encoding (default utf-8)")
    st_space("v", 1)

    show_code("""\
        # Customizing rendering parameters
        st_latex_doc(
            latex_source,
            height=400,          # taller iframe
            light_bg=False,      # transparent background
            hyphenate=False,     # disable hyphenation
        )""")
    st_space("v", 2)

    # --- Section 4: Loading from File ---
    st_write(bs.sub, "Loading from File", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        Use the file parameter to load a .tex file directly. The path
        is resolved via StreamTeX's static asset resolution (same as
        st_mermaid, st_tikz).
    """)
    st_space("v", 1)

    show_code("""\
        # Load a LaTeX document from a file
        st_latex_doc(file="documents/my_article.tex")

        # With custom encoding
        st_latex_doc(file="documents/french_text.tex", encoding="latin-1")""")
    st_space("v", 2)

    # --- Section 5: LaTeX.js Capabilities ---
    st_write(bs.sub, "LaTeX.js Capabilities", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        LaTeX.js supports a wide range of standard LaTeX constructs.
        Here is what works out of the box:
    """)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item(): st_write(s.medium, "Sectioning: \\\\section, \\\\subsection, \\\\subsubsection")
        with l.item(): st_write(s.medium, "Text formatting: \\\\textbf, \\\\emph, \\\\texttt, \\\\underline")
        with l.item(): st_write(s.medium, "Lists: \\\\begin{itemize}, \\\\begin{enumerate}")
        with l.item(): st_write(s.medium, "Tables: \\\\begin{tabular} with basic column specs")
        with l.item(): st_write(s.medium, "Math: inline $...$ and display $$...$$ environments")
        with l.item(): st_write(s.medium, "Quotes: \\\\begin{quote}")
        with l.item(): st_write(s.medium, "Footnotes: \\\\footnote{...}")
    st_space("v", 1)

    show_code("""\
        st_latex_doc(r\"\"\"
        \\\\section{Structured Content}
        \\\\begin{itemize}
          \\\\item First item with \\\\textbf{bold}
          \\\\item Second with inline math: $a^2 + b^2 = c^2$
        \\\\end{itemize}

        \\\\begin{tabular}{|l|r|}
          \\\\hline
          Name & Score \\\\\\\\
          \\\\hline
          Alice & 95 \\\\\\\\
          Bob & 87 \\\\\\\\
          \\\\hline
        \\\\end{tabular}
        \"\"\", height=350)""")
    st_space("v", 1)

    with st_block(s.project.containers.result_box):
        stx.st_latex_doc(r"""
\section{Structured Content}
\begin{itemize}
  \item First item with \textbf{bold}
  \item Second with inline math: $a^2 + b^2 = c^2$
\end{itemize}

\begin{tabular}{|l|r|}
  \hline
  Name & Score \\
  \hline
  Alice & 95 \\
  Bob & 87 \\
  \hline
\end{tabular}
""", height=350, light_bg=True)
    st_space("v", 2)

    # --- Section 6: LaTeX.js Limitations ---
    st_write(bs.sub, "LaTeX.js Limitations", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        LaTeX.js is a client-side parser. It does NOT support everything
        that a full LaTeX distribution provides. Key limitations:
    """)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item(): st_write(s.medium, "No custom packages (\\\\usepackage is limited to built-in ones)")
        with l.item(): st_write(s.medium, "No TikZ diagrams \u2014 use st_tikz() instead")
        with l.item(): st_write(s.medium, "No BibTeX / bibliography management")
        with l.item(): st_write(s.medium, "No \\\\def or \\\\newcommand macros")
        with l.item(): st_write(s.medium, "No cross-references (\\\\ref, \\\\label)")
    st_space("v", 2)

    # --- Section 7: When to Use What ---
    st_write(bs.sub, "Choosing the Right Function", toc_lvl="+1")
    st_space("v", 1)

    show_explanation("""\
        StreamTeX offers several LaTeX-related functions. Choose based
        on your content:
    """)
    st_space("v", 1)

    with st_list(list_type="ul") as l:
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "st_latex()"),
                " \u2014 math formulas only (KaTeX, fast, Streamlit native)",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "st_latex_doc()"),
                " \u2014 full documents, fragments, structured content (LaTeX.js, iframe)",
            )
        with l.item():
            st_write(
                s.medium,
                (s.text.weights.bold_weight, "st_tikz()"),
                " \u2014 TikZ diagrams (requires local pdflatex + dvisvgm)",
            )
    st_space("v", 2)

    show_details("""\
        **st_latex_doc()** uses the LaTeX.js programmatic API (parse + HtmlGenerator),
        loaded from CDN, running entirely client-side in the browser.
        No LaTeX installation required.

        **Fragment wrapping:** When no \\\\documentclass is detected, the source
        is automatically wrapped in a minimal article document before parsing.

        **Iframe isolation:** Each st_latex_doc() call renders in its own iframe,
        providing full CSS/JS isolation from the rest of the Streamlit page.

        **Performance:** Rendering is client-side. Very large documents may
        be slow. For best results, keep documents under a few hundred lines.

        **light_bg:** Forces color-scheme: light for a white background (default True).
        Set to False for transparent/dark backgrounds.

        **hyphenate:** Enables LaTeX.js hyphenation (default True). Disable if
        hyphenation interferes with code listings or monospace text.

        **file=**: Loads .tex files via resolve_static() (same resolution as
        st_mermaid, st_tikz). Supports any text encoding via the encoding parameter.
    """)
    st_space("v", 3)
