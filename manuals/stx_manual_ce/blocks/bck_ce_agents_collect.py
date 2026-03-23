"""CE Manual — Part 3: COLLECT Agents Detail."""

from streamtex import *

try:
    from blocks.helpers import show_explanation, show_details
except ImportError:
    from streamtex import show_explanation, show_details

from custom.styles import Styles as s


class BlockStyles:
    """Styles for the COLLECT agents block."""

    title = s.section_title
    table = s.reference_table


def build():
    """COLLECT agents: source-scanner and import-assessor."""

    st_write("""
    ## COLLECT Phase Agents

    The COLLECT phase is the entry point of every CE cycle. Its two agents
    gather raw material and evaluate what it will take to bring that material
    into a StreamTeX project. Together, they answer: **"What do we have, and
    how hard is it to use?"**
    """)

    show_explanation("""
    ### Agent: source-scanner

    The **source-scanner** is the first agent to run. It walks through the
    directories and files you point it to, building a comprehensive inventory
    of available content.

    **Responsibilities:**

    - **File detection** — recursively scans directories for supported formats:
      HTML, Marp/Markdown, PDF, images, code files, and existing StreamTeX blocks.
    - **Metadata extraction** — for each file, records: format, size, last modified
      date, estimated word count, number of images, and structural landmarks
      (headings, sections, slides).
    - **Dependency mapping** — identifies cross-references between files (shared
      images, linked stylesheets, imported code snippets).
    - **Inventory report** — produces a structured source inventory listing every
      detected asset with its metadata and a unique reference ID.

    The source-scanner does NOT evaluate quality or recommend actions — that is
    left to the import-assessor and the ASSESS phase agents.
    """)

    show_details("""
    ### source-scanner Output Format

    The inventory follows the `tpl_source_inventory` template:

    ```
    Source Inventory
    ================
    Project: <project-name>
    Scan date: <timestamp>
    Total sources: <count>

    Sources:
      [S001] report.html
         Format: HTML | Size: 45KB | Words: ~3200
         Headings: 12 | Images: 5 | Tables: 3
         Dependencies: styles.css, logo.png

      [S002] slides.md
         Format: Marp | Size: 12KB | Words: ~1800
         Slides: 24 | Images: 8
         Dependencies: theme.css
    ```

    Each source gets a stable ID (S001, S002...) used throughout the cycle
    to trace content back to its origin.
    """)

    show_explanation("""
    ### Agent: import-assessor

    The **import-assessor** takes the source inventory and evaluates the
    difficulty of converting each source into StreamTeX blocks.

    **Responsibilities:**

    - **Complexity evaluation** — scores each source on a 3-level scale:
      - **Low**: clean structure, standard formatting, straightforward mapping
      - **Medium**: some manual intervention needed (custom layouts, embedded scripts)
      - **High**: significant restructuring required (complex interactivity, legacy formats)
    - **Method recommendation** — for each source, suggests the conversion approach:
      - *Automated*: direct `/stx-import:html` or `/stx-import:marp` conversion
      - *Assisted*: automated conversion + manual fixup pass
      - *Manual*: hand-rewrite using source as reference only
    - **Effort estimation** — rough time estimates based on complexity and method.
    - **Priority ranking** — orders sources by import priority considering
      dependencies, content value, and conversion difficulty.
    """)

    show_details("""
    ### import-assessor Complexity Criteria

    | Criterion | Low | Medium | High |
    |-----------|-----|--------|------|
    | Structure | Clean headings, sections | Mixed structure | No clear hierarchy |
    | Formatting | Standard HTML/Markdown | Custom CSS, some JS | Heavy JS, animations |
    | Images | Simple embedded images | SVG, diagrams | Interactive charts |
    | Tables | Basic tables | Merged cells, styling | Complex data grids |
    | Layout | Single column | Two-column, sidebars | Grid layouts, overlays |
    | Interactivity | None | Toggles, tabs | Forms, dynamic content |

    **Decision matrix for method recommendation:**

    | Complexity | Source Format | Recommended Method |
    |------------|-------------|--------------------|
    | Low | HTML/Marp | Automated |
    | Low | PDF | Assisted |
    | Medium | HTML/Marp | Assisted |
    | Medium | PDF | Manual |
    | High | Any | Manual |

    The import-assessor writes its findings to the `tpl_assessment_brief`
    template, which feeds directly into the ASSESS phase.
    """)
