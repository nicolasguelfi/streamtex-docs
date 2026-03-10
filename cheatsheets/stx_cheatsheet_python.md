# StreamTeX Python API -- Cheatsheet

> **Version**: streamtex 0.4.1 | **Date**: 2026-03-10

---

## Quick Reference

```python
from streamtex import *

s = StxStyles()

# Text
st_write(s.bold, "Hello World")
st_write(s.bold + s.text.colors.red, "Bold red")
st_write((s.bold, "Bold"), " normal ", (s.italic, "italic"))
st_write(s.Large, "Title", toc_lvl="1")
st_write("Visit ", (s.text.colors.blue, "Google", "https://google.com"))

# Layout
with st_grid(cols="1fr 1fr") as g:
    with g.cell(): st_write(s.bold, "Left")
    with g.cell(): st_write(s.bold, "Right")

with st_list() as l:
    with l.item(): st_write("Item 1")
    with l.item(): st_write("Item 2")

with st_block(style=s.container.paddings.p_20):
    st_write("Padded content")

# Media & diagrams
st_image(uri="path/to/image.png", width="100%")
st_code(code="print('hello')", language="python")
st_mermaid("graph LR; A-->B")
st_latex(r"E = mc^2")
st_plantuml("@startuml\nA -> B: Hello\n@enduml")

# Spacing & breaks
st_space("v", "2em")
st_br(2)
st_slide_break()
```

---

## 1. Imports & Setup

### Block file imports

```python
from streamtex import *

s = StxStyles()

def build():
    st_write(s.bold, "My block content")
```

### Book file (book.py) imports

```python
from streamtex import *
import blocks  # Local blocks/__init__.py

st_book(
    [blocks.bck_intro, blocks.bck_content],
    toc_config=TOCConfig(),
    marker_config=MarkerConfig(),
)
```

### StxStyles instance

```python
s = StxStyles()  # Preferred shorthand

# Aliases (deprecated but functional)
s = StreamTeX_Styles()
```

---

## 2. Style System

### Style creation and composition

```python
from streamtex import Style, StxStyles

s = StxStyles()

# Create from CSS
my_style = Style("color: red; font-size: 24pt;", "my_custom_style")

# Composition with +
combined = s.bold + s.text.colors.red + s.Large
combined = s.bold + "padding: 10px;"  # Style + raw CSS string

# Removal with -
stripped = combined - s.bold  # removes bold properties

# Factory copy with new ID
themed = Style.create(s.bold, "project_bold")
```

### StxStyles catalog

#### Text sizes

| Shortcut      | Size  |
|---------------|-------|
| `s.GIANT`     | 196pt |
| `s.Giant`     | 160pt |
| `s.giant`     | 128pt |
| `s.HUGE`      | 96pt  |
| `s.Huge`      | 80pt  |
| `s.huge`      | 64pt  |
| `s.LARGE`     | 48pt  |
| `s.Large`     | 32pt  |
| `s.large`     | 24pt  |
| `s.big`       | 16pt  |
| `s.medium`    | 12pt  |
| `s.little`    | 8pt   |
| `s.small`     | 6pt   |
| `s.tiny`      | 4pt   |

#### Text weights & decorations

```python
s.bold               # font-weight: bold
s.reset_bold         # font-weight: normal
s.italic             # font-style: italic
s.center_txt         # text-align: center
s.text.decors.underline_text
s.text.decors.strike_text
s.text.weights.light_weight
```

#### Colors (named CSS colors via `s.text.colors.*`)

```python
s.text.colors.red
s.text.colors.blue
s.text.colors.coral
s.text.colors.dark_cyan
s.text.colors.cornflower_blue
# ... full CSS named color set available
s.text.colors.reset  # color: initial
```

#### Background colors

```python
s.text.bg_colors.red_bg
s.text.bg_colors.blue_bg
s.text.bg_colors.reset_bg
# ... mirrors named colors with _bg suffix
```

#### Containers

```python
s.container.paddings.p_5     # padding: 5px
s.container.paddings.p_20    # padding: 20px
s.container.margins.m_10     # margin: 10px
s.container.borders.thin_border
s.container.borders.rounded_border
s.container.layouts.flex_row
s.container.layouts.flex_col
s.container.positions.relative
s.container.positions.absolute
```

#### Alignments

```python
s.text.alignments.center_align
s.text.alignments.right_align
s.text.alignments.left_align
s.text.alignments.justify_align
```

#### Special styles

```python
s.none       # Empty style (no CSS)
s.reset      # Reset all: color, bg, weight, size, alignment
s.light_bg   # White background with padding (for diagrams on dark pages)
```

#### Style factory methods

```python
# Dynamic text size
s.text.sizes.size(20, "custom_20pt")   # Factory for custom size

# Container padding factories
s.container.paddings.size("10px", "20px", style_id="custom_pad")
s.container.paddings.little_padding    # Named presets
s.container.paddings.small_padding
s.container.paddings.medium_padding

# Container border factories
s.container.borders.size("2px")
s.container.borders.color(s.text.colors.blue)
s.container.borders.solid_border

# Container list styles
s.container.lists.g_docs               # Google Docs symbols
s.container.lists.ordered_lowercase    # lower-alpha list

# Container sizes
s.container.sizes.width_full           # width: 100%
s.container.sizes.height_auto          # height: auto
```

#### Flex & layout container styles

```python
s.container.flex.center_flex
s.container.flex.space_between_justify
s.container.layouts.vertical_center_layout
s.container.layouts.center
s.container.layouts.flex_row
s.container.layouts.flex_col
```

### StxStyles inheritance for project Styles

```python
from streamtex import StxStyles  # or StreamTeX_Styles (alias)
class Styles(StxStyles):
    project = MyCustomStyles
```

### ListStyle

```python
from streamtex import ListStyle

ls = ListStyle(
    css="color: navy; font-size: 14pt;",
    style_id="my_list",
    symbols=["-->", "=>", "*"]  # cycle per nesting level
)
```

### StyleGrid

```python
from streamtex import StyleGrid

grid_styles = StyleGrid([
    [s.bold, s.italic],        # row 0
    [s.text.colors.red, s.none],  # row 1
])
```

### Theme overrides

```python
from streamtex.styles import theme

# Override any style_id globally
theme["bold_weight"] = "font-weight: 900;"
theme["my_custom_style"] = "color: gold; font-size: 36pt;"
```

---

## 3. Content Rendering

### st_write

```python
def st_write(
    *args,
    style: Style = StxStyles.none,
    tag: Tag = Tags.span,
    link: str = "",
    no_link_decor: bool = False,
    hover: bool = True,
    toc_lvl: Optional[str] = None,
    label: str = "",
    marker: Optional[bool] = None,
)
```

**Basic text:**

```python
st_write(s.big, "Hello World")
st_write("Plain text without style")
```

**Styled text:**

```python
st_write(s.bold + s.text.colors.red, "Bold red text")
st_write(s.Large + s.center_txt, "Centered title")
```

**Tuple syntax for inline mixed styles:**

```python
st_write(
    s.big,
    (s.bold, "Bold part"),
    " normal text ",
    (s.italic + s.text.colors.blue, "italic blue"),
)
```

**Links (tuple with 3 elements):**

```python
st_write("Click ", (s.text.colors.blue, "here", "https://example.com"))
st_write(s.big, "Full link", link="https://example.com")
```

**TOC registration:**

```python
st_write(s.Large, "Chapter 1", toc_lvl="1")
st_write(s.large, "Section 1.1", toc_lvl="2")
st_write(s.big, "Subsection", toc_lvl="+1")  # relative: one level deeper
st_write(s.big, "Custom label", toc_lvl="2", label="Short TOC Label")
```

**Marker anchors:**

```python
st_write(s.Large, "Title", toc_lvl="1", marker=True)   # force marker
st_write(s.Large, "Title", toc_lvl="1", marker=False)   # suppress marker
```

**HTML tags:**

```python
st_write(s.bold, "Title", tag=Tags.h1)
st_write(s.big, "Paragraph", tag=Tags.p)
# Available: Tags.div, Tags.span, Tags.p, Tags.h1..h6,
#            Tags.header, Tags.section, Tags.footer, Tags.blockquote,
#            Tags.cite, Tags.code, Tags.figcaption, Tags.figure
```

### st_code

```python
def st_code(
    style: Style = StxStyles.none,
    code: str = "",
    language: str = "python",
    line_numbers: bool = True,
    font_size: str = "var(--stx-code-size, 18pt)",
    line_number_color: str = "#6A9BC5",
    wrap: Optional[bool] = None,
    file: str | None = None,
    encoding: str = "utf-8",
    line_start: int | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
)
```

**Examples:**

```python
st_code(code="print('hello')", language="python")
st_code(s.container.paddings.p_10, code="<h1>Title</h1>", language="html")
st_code(file="examples/demo.py", start_line=5, end_line=20)
st_code(code="long line...", wrap=True)
```

**Global wrap toggle (sidebar):**

```python
add_wrap_all_option(default=True)
```

### st_markdown

```python
def st_markdown(
    content: str = "",
    *,
    style: Style = StxStyles.none,
    file: str | None = None,
    encoding: str = "utf-8",
)
```

**Examples:**

```python
st_markdown("**Bold** and *italic* with `code`")
st_markdown(file="docs/intro.md")
st_markdown("# Heading", style=s.container.paddings.p_20)
```

**Supported syntax:** pipe tables, fenced code blocks, inline/display math (`$...$` / `$$...$$`), standard Markdown (bold, italic, links, lists, headings).

**st_markdown() vs st_write():**

| Feature | `st_markdown()` | `st_write()` |
|---------|-----------------|--------------|
| Input | Raw Markdown string | Style + text/tuples |
| Styling | Container style only | Inline mixed styles via tuples |
| Tables | Pipe tables supported | Use `st_grid` instead |
| Math | `$...$` and `$$...$$` | Use `st_latex()` |
| Best for | Long-form Markdown content | Styled inline text |

### st_image

```python
def st_image(
    style: Style = StxStyles.none,
    width="100%",
    height="auto",
    uri: str = "",
    alt: str = "",
    link: str = "",
    hover: bool = True,
    light_bg: bool = False,
)
```

**Examples:**

```python
st_image(uri="images/photo.png")
st_image(uri="https://example.com/img.jpg", width="50%", alt="Photo")
st_image(uri="logo.svg", width=200, link="https://example.com")
st_image(uri="diagram.svg", light_bg=True)  # white bg in iframe
```

Image URI resolution order:
1. URL (`https://...`) -- used directly
2. Absolute/relative path -- base64 encoded
3. Static path -- searches configured static source directories

### st_space / st_br

```python
def st_space(direction: Literal["v", "h"] = "v", size="1em")
def st_br(count: int = 1)
```

**Examples:**

```python
st_space("v", "2em")      # vertical space
st_space("h", "20px")     # horizontal space
st_space("v", 3)           # 3em vertical space (numeric = em)
st_br()                    # single <br>
st_br(3)                   # three <br> tags
```

---

## 4. Layout

### st_block -- styled container

```python
@contextmanager
def st_block(style: Style = StxStyles.none, _export_wrapper: bool = True)
```

**Examples:**

```python
with st_block(style=s.container.paddings.p_20 + s.text.bg_colors.light_gray_bg):
    st_write(s.big, "Content in a styled box")
    st_code(code="x = 1")
```

### st_span -- inline container

```python
@contextmanager
def st_span(style: Style = StxStyles.none)
```

```python
with st_span(style=s.bold):
    st_write("These ")
    st_write("are inline")
```

### st_grid

```python
@contextmanager
def st_grid(
    cols: str | int = 2,
    grid_style: Style = StxStyles.none,
    cell_styles: CELL_STYLES_TYPE = StxStyles.none,
    gap: str = None,
    responsive: bool = False,
    min_width: str | int | None = None,
    breakpoint: str | None = None,
)
```

**Basic grid:**

```python
with st_grid(2) as g:
    with g.cell(): st_write("Left")
    with g.cell(): st_write("Right")
```

**CSS template columns:**

```python
with st_grid(cols="1fr 2fr 1fr") as g:
    with g.cell(): st_write("Sidebar")
    with g.cell(): st_write("Main")
    with g.cell(): st_write("Aside")
```

**Responsive grid:**

```python
with st_grid(cols=3, responsive=True) as g:
    for i in range(6):
        with g.cell(): st_write(f"Card {i}")

with st_grid(cols="25% 1fr", breakpoint="600px") as g:
    with g.cell(): st_write("Sidebar")
    with g.cell(): st_write("Content")
```

**Cell styles:**

```python
with st_grid(2, cell_styles=[s.bold, s.italic]) as g:
    with g.cell(): st_write("Bold cell")
    with g.cell(): st_write("Italic cell")

# Matrix of styles
with st_grid(2, cell_styles=StyleGrid([
    [s.text.colors.red, s.text.colors.blue],
    [s.text.colors.green, s.text.colors.coral],
])) as g:
    for i in range(4):
        with g.cell(): st_write(f"Cell {i}")
```

**responsive_cols() helper:**

```python
def responsive_cols(cols: int, min_width: str | int | None = None) -> str
```

```python
template = responsive_cols(3)          # "repeat(auto-fit, minmax(280px, 1fr))"
template = responsive_cols(4, "200px") # "repeat(auto-fit, minmax(200px, 1fr))"
```

**Responsive presets:**

```python
responsive_2col   # "repeat(auto-fit, minmax(350px, 1fr))"
responsive_3col   # "repeat(auto-fit, minmax(250px, 1fr))"
responsive_cards  # "repeat(auto-fit, minmax(300px, 1fr))"
```

### StyleGrid advanced (sg.create with range notation)

```python
from streamtex import StyleGrid as sg

# Excel-like cell notation
cell_styles = sg.create("A1,A3", s.bold) + sg.create("A2", s.italic)
# Range notation
cell_styles = sg.create("A1:B3", s.bold)
# Operators: + (add), * (override), - (subtract)
combined = sg1 + sg2    # Merge
override = sg1 * sg2    # sg2 wins on conflicts
removed = sg1 - sg2     # Remove sg2's styles
```

### st_list

```python
@contextmanager
def st_list(
    list_type: ListType = ListTypes.unordered,
    l_style: Style = StxStyles.none,
    li_style: Style = StxStyles.none,
    align: str = None,
    alt_li_styles: list[Style] | None = None,
)
```

**Unordered list:**

```python
with st_list() as l:
    with l.item(): st_write(s.big, "Item 1")
    with l.item(): st_write(s.big, "Item 2")
```

**Ordered list:**

```python
from streamtex.enums import ListTypes

with st_list(list_type=ListTypes.ordered) as l:
    with l.item(): st_write("First")
    with l.item(): st_write("Second")
```

**Nested lists:**

```python
with st_list() as l:
    with l.item():
        st_write("Parent")
        with st_list() as l2:
            with l2.item(): st_write("Child 1")
            with l2.item(): st_write("Child 2")
```

**Custom list styles:**

```python
ls = ListStyle(symbols=["-->", "=>", "*"])
with st_list(l_style=ls, li_style=s.big) as l:
    with l.item(): st_write("Arrow item")
```

**Alternating item styles:**

```python
with st_list(alt_li_styles=[s.text.colors.red, s.text.colors.blue]) as l:
    with l.item(): st_write("Red")
    with l.item(): st_write("Blue")
    with l.item(): st_write("Red again")
```

**Per-item style override:**

```python
with st_list() as l:
    with l.item(style=s.bold): st_write("Bold item")
    with l.item(): st_write("Normal item")
```

**Centered list:**

```python
with st_list(align="center") as l:
    with l.item(): st_write("Centered list")
```

### st_overlay

```python
@contextmanager
def st_overlay(style: Style = StxStyles.none)
```

Yields an `OverlayController` with `.layer()`:

```python
controller.layer(
    style: Style = StxStyles.none,
    top: str | int = None,
    left: str | int = None,
    right: str | int = None,
    bottom: str | int = None,
)
```

**Example:**

```python
with st_overlay() as o:
    st_image(uri="background.jpg")
    with o.layer(top=50, left=50):
        st_write(s.bold + s.text.colors.white, "Overlay Text")
    with o.layer(bottom="10%", right="5%"):
        st_write("Bottom-right caption")
```

---

## 5. Diagrams & Math

### st_mermaid

```python
def st_mermaid(
    code: str = "",
    *,
    style: Style | None = None,
    light_bg: bool = True,
    height: int = 500,
    fit: str = "contain",   # "contain" | "width" | "none"
    file: str | None = None,
    encoding: str = "utf-8",
)
```

```python
st_mermaid("""
    graph LR
        A[Start] --> B{Decision}
        B -->|Yes| C[OK]
        B -->|No| D[Fail]
""")
st_mermaid(file="diagrams/flow.mmd", height=600, fit="width")
```

### st_plantuml

```python
def st_plantuml(
    code: str = "",
    *,
    style: Style | None = None,
    light_bg: bool = True,
    height: int = 500,
    server: str = "https://www.plantuml.com/plantuml",
    file: str | None = None,
    encoding: str = "utf-8",
)
```

```python
st_plantuml("""
    @startuml
    Alice -> Bob: Hello
    Bob --> Alice: Hi
    @enduml
""")
st_plantuml(file="diagrams/sequence.puml")
```

### st_tikz

```python
def st_tikz(
    code: str = "",
    *,
    style: Style | None = None,
    light_bg: bool = True,
    height: int | None = None,
    preamble: str = "",
    file: str | None = None,
    encoding: str = "utf-8",
)
```

Requires system `latex` and `dvisvgm`.

```python
st_tikz(r"""
    \begin{tikzpicture}
        \draw (0,0) -- (4,0) -- (4,3) -- cycle;
    \end{tikzpicture}
""")
st_tikz(file="diagrams/graph.tex", preamble=r"\usepackage{pgfplots}")
```

### st_latex / st_latex_doc

```python
def st_latex(
    content: str = "",
    *,
    style: Style | None = None,
    file: str | None = None,
    encoding: str = "utf-8",
)
```

```python
st_latex(r"E = mc^2")
st_latex(r"\int_0^\infty e^{-x}\,dx = 1")
```

```python
def st_latex_doc(
    code: str = "",
    *,
    style: Style | None = None,
    light_bg: bool = True,
    height: int = 600,
    hyphenate: bool = True,
    file: str | None = None,
    encoding: str = "utf-8",
)
```

Renders full LaTeX documents via LaTeX.js (client-side, no system dependency). Fragments without `\documentclass` are auto-wrapped.

```python
st_latex_doc(r"""
    \section{Introduction}
    This is a \textbf{LaTeX} document rendered in the browser.
    \begin{itemize}
        \item First point
        \item Second point
    \end{itemize}
""")
st_latex_doc(file="documents/report.tex", height=800)
```

### st_graphviz

```python
def st_graphviz(dot_source="", *, file: str | None = None, encoding: str = "utf-8", **kw)
```

```python
st_graphviz("""
    digraph G {
        A -> B -> C;
        B -> D;
    }
""")
st_graphviz(file="diagrams/graph.dot")
```

### LaTeX parsing utilities

```python
from streamtex import extract_tikz, extract_math, extract_frames
tikz_blocks = extract_tikz(latex_source)
math_exprs = extract_math(latex_source)
frames = extract_frames(latex_source)
```

---

## 6. Book Organization

### st_book

```python
def st_book(
    module_list,
    toc_config: TOCConfig = None,
    marker_config: MarkerConfig = None,
    separator=None,
    export: bool = True,
    export_title: str = "StreamTeX Export",
    pdf_config: PdfConfig = None,
    paginate: bool = False,
    banner_color: str = "rgba(211, 47, 47, 0.8)",
    banner: BannerConfig = None,
    bib_sources=None,
    bib_config=None,
    inspector=None,
    page_width: int = 90,
    zoom: int = 100,
)
```

**Minimal book:**

```python
import blocks

st_book([blocks.bck_intro, blocks.bck_content])
```

**Full-featured book:**

```python
st_book(
    [blocks.bck_intro, blocks.bck_ch1, blocks.bck_ch2],
    toc_config=TOCConfig(
        numerate_titles=True,
        numbering=NumberingMode.BOTH,
        search=True,
    ),
    marker_config=MarkerConfig(
        auto_marker_on_toc=2,
        nav_position="bottom-right",
    ),
    paginate=True,
    banner=BannerConfig.compact(),
    export=True,
    export_title="My Book",
    pdf_config=PdfConfig(format="A4", landscape=True),
    bib_sources=["refs/bibliography.bib"],
    bib_config=BibConfig(format=BibFormat.APA),
    page_width=85,
    zoom=100,
)
```

### st_include

```python
def st_include(block_file_module, *args, **kwargs)
```

Calls `block_file_module.build(*args, **kwargs)`. Used internally by `st_book` and can be called manually.

```python
import blocks
st_include(blocks.bck_intro)
st_include(blocks.bck_content, some_param="value")
```

### TOCConfig

```python
@dataclass
class TOCConfig:
    numerate_titles: bool = True
    numbering: str | None = None  # NumberingMode value
    toc_position: int = -1        # -1=end, 0=start, None=no TOC
    title_style: Style = ...
    content_style: Style = ...
    search: bool = False
    search_placeholder: str = "Search..."
    sidebar_max_level: int | None = None
```

### NumberingMode

```python
class NumberingMode:
    NONE = "none"
    BOTH = "both"
    SIDEBAR_ONLY = "sidebar"
    MAIN_ONLY = "main"
```

### MarkerConfig

```python
@dataclass
class MarkerConfig:
    show_nav_ui: bool = True
    auto_marker_on_toc: int | bool = False  # True=all, int N=up to level N
    nav_position: str = "bottom-right"      # or "bottom-center"
    nav_label_chars: int = 40
    popup_open: bool = False
    next_keys: list[str] = ["PageDown"]     # JS KeyboardEvent.key values
    prev_keys: list[str] = ["PageUp"]
```

### st_marker

```python
def st_marker(label: str = "", visible: bool = False, hidden: bool = False)
```

```python
st_marker("Section Start")
st_marker("Nav stop", visible=True)    # dashed line visible
st_marker("Silent", hidden=True)       # works for PageDown but not in list
```

### st_slide_break / SlideBreakConfig

```python
def st_slide_break()
```

```python
st_slide_break()  # Insert a section separator (rule + spacer + marker)
```

```python
@dataclass
class SlideBreakConfig:
    mode: SlideBreakMode = SlideBreakMode.FULL
    space: str = "60vh"
    rule_margin_top: str = "1em"
    rule_margin_bottom: str = "0.5em"
    thickness: str = "1px"
    color: str = "128, 128, 128"  # RGB values
    opacity: float = 0.5
    marker: bool = True
```

```python
class SlideBreakMode(Enum):
    FULL         # rule + spacer + marker (default)
    RULE_ONLY    # horizontal rule only
    SPACER_ONLY  # vertical space only
    MARKER_ONLY  # hidden marker only
    HIDDEN       # nothing rendered
```

```python
from streamtex import set_slide_break_config, SlideBreakConfig, SlideBreakMode

set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.FULL,
    space="80vh",
    thickness="2px",
    color="79, 172, 254",
    opacity=0.5,
))
```

### BannerConfig / BannerMode

```python
@dataclass
class BannerConfig:
    mode: BannerMode = BannerMode.FULL
    color: str = "rgba(211, 47, 47, 0.8)"
    text_color: str = "white"
    # ... font_size, padding, border_radius, show_dividers
```

```python
class BannerMode(Enum):
    FULL      # prominent banner
    COMPACT   # slim, discreet
    HIDDEN    # no visual banner
```

**Factory classmethods:**

```python
st_book(modules, paginate=True, banner=BannerConfig.compact())
st_book(modules, paginate=True, banner=BannerConfig.hidden())
```

### book.py complete orchestration pattern

```python
import streamlit as st
import streamtex as stx
from streamtex import st_book, TOCConfig, NumberingMode, MarkerConfig, BannerConfig
from custom.styles import Styles as s
from custom.themes import dark
import streamtex.styles as sts
from pathlib import Path
import blocks

stx.set_static_sources([str(Path(__file__).parent / "static")])
st.set_page_config(page_title="My Project", layout="wide", initial_sidebar_state="expanded")
sts.theme = dark

toc = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, sidebar_max_level=2, search=True)
marker_config = MarkerConfig(auto_marker_on_toc=1)

st_book([blocks.bck_01_title, blocks.bck_02_content, ...],
    toc_config=toc, marker_config=marker_config, paginate=True,
    banner=BannerConfig.full(),
    inspector=stx.InspectorConfig(enabled=True))
```

### InspectorConfig

```python
stx.InspectorConfig(
    enabled=True,
    password=None,          # Optional password protection
    panel_width="35vw",     # Right panel width
    backup=True,            # Create .bak files before saving
)
```

### BannerConfig auto-values by mode

| Field | FULL | COMPACT |
|-------|------|---------|
| font_size | "1.1rem" | "0.85rem" |
| font_weight | "600" | "500" |
| padding | "0.5rem 1rem" | "0.3rem 0.6rem" |
| show_dividers | True | False |

### st_slide_break with marker_label

```python
st_slide_break(marker_label="concept_details")
```

### add_slide_break_options

```python
add_slide_break_options()  # Sidebar toggle for slide break visibility
```

### Search + Markers filtering

When `search=True` in TOCConfig and markers are enabled, the sidebar search also filters marker entries.

### st_toc manual placeholder

```python
from streamtex import st_toc
toc_block = st_toc(s.project.titles.section_title)
```

---

## 7. Export-Aware Widgets

All wrappers render the native Streamlit widget AND inject a static HTML fallback into the export buffer.

### Data display

```python
def st_dataframe(data, **kw)
def st_table(data, **kw)
def st_metric(label, value, delta=None, **kw)
def st_json(data, **kw)
```

```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
st_dataframe(df)
st_table(df)
st_metric("Revenue", "$42K", delta="+12%")
st_json({"key": "value", "nested": [1, 2, 3]})
```

### Charts

```python
def st_line_chart(data, *, x=None, y=None, **kw)
def st_bar_chart(data, *, x=None, y=None, **kw)
def st_area_chart(data, *, x=None, y=None, **kw)
def st_scatter_chart(data, *, x=None, y=None, **kw)
```

```python
st_line_chart(df, x="date", y="value")
st_bar_chart(df)
```

Export renders SVG via matplotlib (graceful table fallback if matplotlib is absent).

### Graphviz

```python
def st_graphviz(dot_source="", *, file: str | None = None, encoding: str = "utf-8", **kw)
```

### Media

```python
def st_audio(data, **kw)
def st_video(data, **kw)
```

```python
st_audio("audio/narration.mp3")
st_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st_video("video/demo.mp4")
```

YouTube URLs are auto-detected and exported as iframe embeds.

---

## 8. Bibliography

### Loading bibliography files

```python
def load_bib(path: str) -> List[BibEntry]          # auto-detect format
def load_bibtex(path: str) -> List[BibEntry]        # .bib
def load_bib_json(path: str) -> List[BibEntry]      # .json
def load_bib_ris(path: str) -> List[BibEntry]       # .ris
def load_bib_csl_json(path: str) -> List[BibEntry]  # .csl-json (Zotero)
```

```python
entries = load_bib("refs/bibliography.bib")  # auto-detects BibTeX
```

Preferred approach: pass `bib_sources` to `st_book()`:

```python
st_book(modules, bib_sources=["refs/bibliography.bib"])
```

### Inline citations

```python
def cite(*keys: str, prefix: str = "", suffix: str = "") -> str
def st_cite(*keys: str, prefix: str = "", suffix: str = "", style=None)
```

```python
# Inline (returns HTML string for use in st_write)
st_write(s.big, "According to ", cite("vaswani2017"), " transformers...")

# Multiple citations
st_write(s.big, "Prior work ", cite("smith2020", "jones2021"))

# Prefix/suffix
st_write(s.big, cite("doe2019", prefix="cf. ", suffix=", p. 42"))

# Immediate rendering
st_cite("vaswani2017")
```

### Bibliography rendering

```python
def st_bibliography(
    *,
    style=None,
    title: str = "References",
    title_style=None,
    toc_lvl: Optional[str] = None,
    only_cited: bool = True,
    format: Optional[BibFormat] = None,
)
```

```python
st_bibliography()
st_bibliography(title="Works Cited", toc_lvl="1", format=BibFormat.IEEE)
```

### Configuration

```python
class BibFormat(Enum):
    APA, MLA, IEEE, CHICAGO, HARVARD

class CitationStyle(Enum):
    AUTHOR_YEAR    # (Vaswani et al., 2017)
    NUMERIC        # [1]
    SUPERSCRIPT    # superscript number
```

```python
@dataclass
class BibConfig:
    format: BibFormat = BibFormat.APA
    citation_style: CitationStyle = CitationStyle.AUTHOR_YEAR
    ...
```

```python
st_book(
    modules,
    bib_sources=["refs/main.bib", "refs/extra.ris"],
    bib_config=BibConfig(format=BibFormat.IEEE, citation_style=CitationStyle.NUMERIC),
)
```

**BibConfig advanced fields:**

```python
BibConfig(
    format=BibFormat.IEEE,
    sort_by="year",                  # Sort bibliography by field
    hover_enabled=True,              # Hover preview cards
    hover_show_abstract=True,        # Show abstract in hover
)
```

### BibRegistry advanced API

```python
registry = get_bib_registry()
registry.register(entry)
registry.register_many(entries)
registry.cite("key1")
registry.get_cited_entries()
registry.get_all_entries()
registry.list_keys()
registry.reset()
len(registry)
"key" in registry
reset_bib_registry()
```

### format_entry

```python
from streamtex.bib import format_entry
html = format_entry(entry, BibFormat.APA)
html = format_entry(entry, BibFormat.IEEE, number=3)
```

### Custom bib parsers

```python
from streamtex.bib import register_bib_parser, BibEntry
def my_parser(filepath: str) -> list[BibEntry]:
    ...
register_bib_parser("myformat", my_parser)
```

### Exception handling

```python
from streamtex.bib import BibParseError
try:
    entries = load_bib("refs.bib")
except BibParseError as e:
    st.error(f"Bibliography parse error: {e}")
```

### BibEntry dataclass

```python
@dataclass
class BibEntry:
    key: str
    entry_type: str = "misc"
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    journal: str = ""
    volume: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""
    # ... plus publisher, booktitle, isbn, issn, editor, institution, etc.
    extra: Dict[str, str] = field(default_factory=dict)

    # Computed properties
    entry.first_author_last  # "Vaswani"
    entry.authors_short      # "Vaswani et al."
```

### BibRefs / generate_bib_stubs

```python
def generate_bib_stubs(*source_paths: str, output_path: str = "") -> str
```

Generates a typed Python module with `@property` for every bib key, enabling IDE autocompletion.

```python
generate_bib_stubs("refs/main.bib", output_path="refs/bib_stubs.py")
```

```python
from streamtex import st_refs
st_write(s.big, "See ", st_refs.vaswani2017)  # IDE autocompletion
```

### BibTeX export

```python
def export_bibtex(*, only_cited: bool = True) -> str
```

```python
bib_text = export_bibtex(only_cited=True)
```

---

## 9. Google Sheets

### GSheetSource

```python
@dataclass
class GSheetSource:
    sheet_id: str
    tab: str = ""
    range: Optional[str] = None
    headers: bool = True

    @staticmethod
    def from_url(url: str, tab: str = "", range: Optional[str] = None,
                 headers: bool = True) -> GSheetSource
```

### Loading data

```python
def load_gsheet(source: GSheetSource, *, config: Optional[GSheetConfig] = None) -> List[Dict[str, Any]]
def load_gsheet_df(source: GSheetSource, *, config: Optional[GSheetConfig] = None) -> pd.DataFrame
```

```python
src = GSheetSource.from_url(
    "https://docs.google.com/spreadsheets/d/1BxiM.../edit",
    tab="Sheet1",
    range="A1:E30",
)
data = load_gsheet(src)        # List[Dict]
df = load_gsheet_df(src)       # pandas DataFrame
```

### GSheetConfig

```python
@dataclass
class GSheetConfig:
    auth_mode: str = AuthMode.SERVICE_ACCOUNT  # "public" | "service_account" | "oauth2"
    credentials_path: Optional[str] = None
    cache_ttl: Optional[int] = 300             # seconds (0=no cache, None=forever)
    default_tab: str = "Sheet1"
```

```python
from streamtex import set_gsheet_config, GSheetConfig, AuthMode

set_gsheet_config(GSheetConfig(
    auth_mode=AuthMode.PUBLIC,
    cache_ttl=60,
))
```

Env vars: `GSHEET_CREDENTIALS`, `GOOGLE_APPLICATION_CREDENTIALS`.

**Credentials resolution order:** explicit path > `GSHEET_CREDENTIALS` env > `GOOGLE_APPLICATION_CREDENTIALS` env.

### GSheetError

```python
from streamtex.gsheet import GSheetError
try:
    data = load_gsheet(src)
except GSheetError as e:
    st.error(f"Google Sheets error: {e}")
```

---

## 10. AI Image Generation

### st_ai_image

```python
def st_ai_image(
    prompt: str,
    style: Style = StxStyles.none,
    width: str = "100%",
    height: str = "auto",
    *,
    provider: Optional[str] = None,   # "openai" | "google" | "fal"
    size: Optional[str] = None,       # e.g. "1024x1024"
    quality: str = "standard",        # "standard" | "hd"
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    alt: str = "",
    link: str = "",
    hover: bool = True,
    light_bg: bool = False,
    config: Optional[AIImageConfig] = None,
    **kwargs,
) -> Optional[str]  # Returns path to image file, or None
```

**Manual mode (default):** shows placeholder with "Generate" button if not cached.
**Auto mode:** generates immediately if not cached.

```python
st_ai_image("A sunset over mountains in watercolor style")
st_ai_image("Logo design", provider="google", size="1024x1024", quality="hd")
```

### st_ai_image_widget

```python
def st_ai_image_widget(
    style: Style = StxStyles.none,
    width: str = "100%",
    height: str = "auto",
    *,
    provider: Optional[str] = None,
    default_prompt: str = "",
    size: Optional[str] = None,
    quality: str = "standard",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    alt: str = "",
    light_bg: bool = False,
    config: Optional[AIImageConfig] = None,
    key: str = "stx_ai_widget",
    show_save: bool = True,
    **kwargs,
) -> Optional[str]
```

Interactive widget with prompt editor, provider selector, generate button, and optional save.

```python
st_ai_image_widget(default_prompt="A cat in space")
```

### AIImageConfig

```python
@dataclass
class AIImageConfig:
    provider: str = "openai"          # "openai" | "google" | "fal"
    default_size: str = "1024x1024"
    output_dir: str = "static/images/ai"
    auto_generate: bool = False
    api_keys: Dict[str, str] = field(default_factory=dict)
```

```python
from streamtex import set_ai_image_config, AIImageConfig

set_ai_image_config(AIImageConfig(
    provider="openai",
    auto_generate=False,
    api_keys={"openai": "sk-..."},
))
```

### Programmatic generation

```python
def generate_image(prompt, provider=..., size=..., quality=..., api_key=..., model=..., config=...) -> str
def is_cached(prompt, provider=..., size=..., quality=..., model=..., config=...) -> bool
def list_providers() -> list[str]
```

### Providers & env vars

| Provider | Model                    | Env var             |
|----------|--------------------------|---------------------|
| openai   | gpt-image-1              | `STX_OPENAI_API_KEY`  |
| google   | imagen-3.0-generate-002  | `STX_GOOGLE_AI_KEY`   |
| fal      | SD v3.5                  | `STX_FAL_KEY`         |

Optional deps: `streamtex[ai]`, `streamtex[ai-openai]`, `streamtex[ai-google]`, `streamtex[ai-fal]`.

Cache: deterministic hash(prompt + provider + size + quality + seed) maps to a file on disk.

---

## 11. HTML & PDF Export

### ExportConfig

```python
@dataclass
class ExportConfig:
    enabled: bool = False
    page_title: str = "StreamTeX Export"
    page_width: str = ...    # from constants.PAGE_WIDTH
    page_padding: str = ...  # from constants.PAGE_PADDING
    zoom: float = 1.0
```

### st_export / st_html

```python
def st_export(fallback_html: str)
```

Context manager to inject static HTML into the export buffer alongside any `st.*` widget.

```python
def st_html(
    html: str,
    *,
    height: int = 0,
    light_bg: bool = False,
    scrolling: bool = False,
)
```

The single bridge for rendering raw HTML. Sends to Streamlit AND the export buffer.

```python
st_html("<div style='color:red'>Custom HTML</div>")
st_html('<svg>...</svg>', height=300, light_bg=True)
```

**height=0 vs height>0:**
- `height=0` (default): renders inline HTML directly in the page (no iframe)
- `height>0`: renders inside an iframe with the specified pixel height

**light_bg:** When `True`, wraps content in an iframe with a white background — useful for diagrams on dark-themed pages.

**Auto font injection:** When rendering in an iframe (`height>0`), `st_html` automatically injects `font-family: Source Sans Pro` so text matches the Streamlit theme.

### PdfConfig

```python
@dataclass
class PdfConfig:
    mode: PdfMode = PdfMode.PAGINATED   # PAGINATED | CONTINUOUS
    format: str = "A4"
    landscape: bool = True
    margin_top: str = "10mm"
    margin_bottom: str = "10mm"
    margin_left: str = "15mm"
    margin_right: str = "15mm"
    print_background: bool = True
    scale: float = 1.0
    header_template: str = ""
    footer_template: str = ""
    page_numbers: bool = False
    theme_bg: str = "#fff"
    theme_text: str = "#333"
```

```python
class PdfMode(Enum):
    CONTINUOUS   # remove all slide breaks
    PAGINATED    # page break at each slide break
```

### export_pdf

```python
def export_pdf(
    html: str,
    output_path: Optional[str] = None,
    config: Optional[PdfConfig] = None,
) -> bytes
```

Requires `streamtex[pdf]` extra and `playwright install chromium`.

```python
pdf_bytes = export_pdf(html_string, config=PdfConfig(format="A4", landscape=True))
```

### WYSIWYG export details

- Width% sets `max-width` on `.streamtex-page`
- Zoom% sets CSS `zoom`
- Export panel shows "Current view: Width X% / Zoom Y%"

### Zoom control

```python
from streamtex import add_zoom_options, inject_zoom_logic
add_zoom_options()                           # Sidebar controls
inject_zoom_logic(width=100, zoom=100)      # Programmatic
```

---

## 12. Block Architecture

### Block file pattern

Every block is a `.py` file with a `build()` function:

```python
# blocks/bck_intro.py
from streamtex import *

s = StxStyles()

def build():
    st_write(s.Large, "Introduction", toc_lvl="1")
    st_slide_break()
    st_write(s.big, "Welcome to the course.")
```

### Naming convention

- Block files: `bck_<name>.py`
- Block functions: `build()` (entry point)

### ProjectBlockRegistry

```python
class ProjectBlockRegistry:
    def __init__(self, blocks_dir: Path)
```

Used in `blocks/__init__.py`:

```python
from pathlib import Path
from streamtex import ProjectBlockRegistry

registry = ProjectBlockRegistry(Path(__file__).parent)
# Access: registry.bck_intro, registry.bck_content, ...
```

Features:
- Lazy-loading with O(1) startup
- Auto-reload on file change
- `registry.list_blocks()` -- all discoverable block names
- `registry.get("bck_name")` -- explicit access

### LazyBlockRegistry

For loading blocks from external/shared directories:

```python
class LazyBlockRegistry:
    def __init__(self, sources: List[str])
```

```python
shared = LazyBlockRegistry(["../../shared-blocks/blocks"])

st_book([
    shared.bck_header,
    blocks.bck_content,
    shared.bck_footer,
])
```

### Block helpers

```python
def show_code(
    code_string: str = "",
    language: str = "python",
    line_numbers: bool = True,
    style: Optional[object] = None,
    wrap: Optional[bool] = None,
    file: str | None = None,
    encoding: str = "utf-8",
    line_start: int | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
)

def show_code_inline(...)  # same signature, no box wrapper

def show_explanation(text: str, style: Optional[object] = None)
def show_details(text: str, style: Optional[object] = None)
```

```python
show_code("print('hello')")
show_code(file="examples/demo.py", start_line=10, end_line=25)

show_explanation("""
    **st_write()** renders styled text using HTML.
    Supports tuple syntax for inline mixed styles.
""")

show_details("""
    **Key point**: content is auto-dedented.
    Supports full *Markdown* with `code spans`.
""")
```

Note: `show_explanation()`, `show_details()`, `show_code()`, `show_code_inline()`, `st_write()`, and `st_code()` all auto-dedent their input. Never wrap with `textwrap.dedent()`.

### BlockHelperConfig (Dependency Injection)

```python
class BlockHelperConfig:
    def get_code_style(self) -> Optional[object]
    def get_code_inline_style(self) -> Optional[object]
    def get_explanation_style(self) -> Optional[object]
    def get_details_style(self) -> Optional[object]
```

```python
from streamtex import set_block_helper_config, BlockHelperConfig

class MyConfig(BlockHelperConfig):
    def get_code_style(self):
        return my_styles.containers.code_box
    def get_explanation_style(self):
        return my_styles.containers.explanation_box

set_block_helper_config(MyConfig())
# Now show_code() and show_explanation() use project styles automatically
```

### BlockHelper (OOP inheritance)

```python
class BlockHelper:
    def show_code(self, code_string, language="python", ...)
    def show_code_inline(self, ...)
    def show_explanation(self, text, style=None)
    def show_details(self, text, style=None)
```

```python
class ProjectHelper(BlockHelper):
    def show_code(self, code_string, **kw):
        # custom logic
        super().show_code(code_string, **kw)
```

### Block Management Advanced API

```python
shared.invalidate()                          # Clear cache
LazyBlockRegistry.invalidate_all()           # Clear ALL caches
registry.list_blocks("composite")            # Filter by type
registry.load_all()                          # Force-load (for testing)
registry.get_stats()                         # {"total": N, "loaded": N, ...}
```

### helpers.py convenience wrapper pattern

```python
# blocks/helpers.py
from streamtex import (
    show_code as _show_code,
    show_explanation as _show_explanation,
    show_details as _show_details,
)
```

---

## 13. Collection

### st_collection

```python
def st_collection(
    config: CollectionConfig,
    home_styles: Optional[object] = None,
)
```

### CollectionConfig

```python
@dataclass
class CollectionConfig:
    title: str = "StreamTeX Collection"
    description: str = ""
    cards_per_row: int = 3
    projects: Dict[str, ProjectMeta] = field(default_factory=dict)

    @classmethod
    def from_toml(cls, path: str) -> CollectionConfig
```

### ProjectMeta

```python
@dataclass
class ProjectMeta:
    title: str
    description: str = ""
    cover: str = ""
    project_url: str = ""
    order: int = 0
```

**Example (collection.toml):**

```toml
[collection]
title = "Course Library"
description = "All courses"
cards_per_row = 3

[projects.intro]
title = "Introduction"
description = "Getting started guide"
cover = "static/images/covers/intro.png"
project_url = "https://streamtex-intro.onrender.com"
order = 1
```

**Usage:**

```python
from streamtex import st_collection, CollectionConfig

config = CollectionConfig.from_toml("collection.toml")
st_collection(config)
```

### Custom collection with st_book pattern

```python
st_book([
    blocks.bck_home,           # Custom home page with cards
    blocks.bck_management,     # Documentation
], toc_config=toc, paginate=False)
```

---

## 14. Utilities & Configuration

### LinkConfig

```python
from streamtex import LinkConfig, set_link_config, get_link_config
set_link_config(LinkConfig(
    internal_target="_self",
    external_target="_blank",
))
```

### Utility functions

```python
from streamtex import load_css, exec_static, configure_image_path, inject_link_preview_scaffold

load_css("custom-theme.css")
exec_static("examples/demo.py")
exec_static("examples/demo.py", start_line=5, end_line=20)
configure_image_path("static/images")
inject_link_preview_scaffold()  # JS for link hover previews
```

### FileCategoryRegistry

```python
from streamtex import FileCategoryRegistry
from streamtex.inspector import FileCategory
registry = FileCategoryRegistry()
registry.register(FileCategory(name="Config", extensions={".ini", ".cfg"}, ace_mode="text"))
```

---

## Appendix: Complete Public API

All symbols exported by `from streamtex import *`:

| Category | Symbols |
|----------|---------|
| **Styles** | `Style`, `ListStyle`, `StyleGrid`, `StxStyles`, `StreamTeX_Styles`, `theme` |
| **Content** | `st_write`, `st_code`, `st_markdown`, `st_image`, `st_html` |
| **Layout** | `st_block`, `st_span`, `st_grid`, `responsive_cols`, `st_list`, `st_overlay` |
| **Spacing** | `st_space`, `st_br` |
| **Diagrams** | `st_mermaid`, `st_plantuml`, `st_tikz`, `st_graphviz` |
| **LaTeX** | `st_latex`, `st_latex_doc` |
| **Book** | `st_book`, `st_include`, `st_toc`, `load_css` |
| **TOC** | `TOCConfig`, `NumberingMode`, `reset_toc_registry`, `toc_entries` |
| **Markers** | `st_marker`, `MarkerConfig` |
| **Slides** | `st_slide_break`, `SlideBreakConfig`, `SlideBreakMode`, `set_slide_break_config`, `get_slide_break_config`, `add_slide_break_options` |
| **Banner** | `BannerConfig`, `BannerMode` |
| **Export** | `ExportConfig`, `st_export`, `PdfConfig`, `PdfMode`, `export_pdf` |
| **Widgets** | `st_dataframe`, `st_table`, `st_metric`, `st_json`, `st_line_chart`, `st_bar_chart`, `st_area_chart`, `st_scatter_chart`, `st_audio`, `st_video` |
| **Bib** | `BibEntry`, `BibConfig`, `BibFormat`, `CitationStyle`, `BibRegistry`, `load_bib`, `load_bibtex`, `load_bib_json`, `load_bib_ris`, `load_bib_csl_json`, `cite`, `st_cite`, `st_bibliography`, `export_bibtex`, `st_refs`, `BibRefs`, `generate_bib_stubs`, `set_bib_config`, `get_bib_config`, `register_bib_parser`, `parse_bibtex_string`, `parse_ris_string`, `format_entry` |
| **GSheet** | `GSheetConfig`, `GSheetSource`, `GSheetError`, `AuthMode`, `set_gsheet_config`, `get_gsheet_config`, `load_gsheet`, `load_gsheet_df` |
| **AI** | `AIImageConfig`, `AIImageError`, `AIImageResult`, `set_ai_image_config`, `get_ai_image_config`, `generate_image`, `is_cached`, `list_providers`, `st_ai_image`, `st_ai_image_widget` |
| **Blocks** | `LazyBlockRegistry`, `ProjectBlockRegistry`, `BlockNotFoundError`, `BlockImportError`, `load_atomic_block`, `set_static_sources`, `get_static_sources`, `resolve_static` |
| **Helpers** | `BlockHelperConfig`, `BlockHelper`, `show_code`, `show_code_inline`, `show_explanation`, `show_details`, `set_block_helper_config`, `get_block_helper_config` |
| **Collection** | `st_collection`, `CollectionConfig`, `ProjectMeta` |
| **Enums** | `Tags` |
| **Image** | `configure_image_path` |
| **Code** | `add_wrap_all_option` |
| **Zoom** | `add_zoom_options`, `inject_zoom_logic` |
| **Link** | `LinkConfig`, `set_link_config`, `get_link_config` |
| **Inspector** | `InspectorConfig`, `FileCategoryRegistry` |
| **Utils** | `exec_static`, `inject_link_preview_scaffold`, `resolve_content` |
| **LaTeX utils** | `extract_tikz`, `extract_math`, `extract_frames` |
