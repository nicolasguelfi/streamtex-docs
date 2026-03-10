# StreamTeX Development & Claude Workflow -- Cheatsheet

Complete reference for developers using Claude Code, profiles, slash commands, and agents to create and maintain StreamTeX projects.

---

## Quick Reference

### CLI Commands (copy-pasteable)

```bash
# Workspace
stx workspace init .                      # Initialize workspace (standard preset)
stx workspace update                      # Pull repos + sync deps + update profiles + global commands
stx workspace status                      # Git status of all repos
stx workspace upgrade developer           # Upgrade to developer preset

# Claude Profiles
stx claude install project ./my-project   # Install project profile
stx claude install presentation ./my-pres # Install presentation profile (extends project)
stx claude list                           # List available profiles
stx claude check                          # Verify all profiles are in sync
stx claude update --all                   # Update all project profiles
stx claude update . --force               # Update single project (overwrite CLAUDE.md)
stx claude diff .                         # Compare installed vs source

# Project
stx project new my-project                # Scaffold minimal project
stx project new my-project --template project  # Scaffold from rich template
stx project validate .                    # Validate project structure (10 checks)

# Test & Lint
stx test -v                               # Run pytest verbose
stx lint                                  # Run ruff check
stx lint -- --fix                         # Auto-fix lint issues

# Run
uv run streamlit run book.py              # Launch the app
```

### Slash Commands (in Claude Code)

```
# stx-designer — Project lifecycle (5 commands)
/stx-designer:init [--template] <desc>                Create project from description
                                                      Templates: project, presentation,
                                                      collection, course
/stx-designer:update [--upgrade|--migrate|--export] <desc>  Add/modify content, migrate,
                                                            export, upgrade structure
/stx-designer:audit [--all|--target <name>] <desc>    Check quality (structure, styles,
                                                      design, presentation compliance)
/stx-designer:fix [--all|--target <name>] <desc>      Auto-fix issues found by audit
/stx-designer:tool <tool-name> <desc>                 Specialized tools (survey-convert)

# Lifecycle: init → update → audit → fix → update → ...
# All commands accept --help for the full cheatsheet.

# Developer
/developer:test-run             Run test suite
/developer:lint                 Run linter with auto-fix

# Global (available everywhere)
/stx-guide                      Ecosystem navigation guide (16 topics)
```

---

## 1. Claude Profiles

StreamTeX provides 4 AI profiles, each tailored to a specific audience. Profiles install slash commands, agents, skills, and coding references into a project's `.claude/` directory.

### Profile Types

| Profile | Audience | Commands | Agents | Skills | Key Use Cases |
|---------|----------|:--------:|:------:|:------:|---------------|
| **project** | Content creators, teachers | 19 | 3 | 5 | Create projects, design slides, migrate HTML, audit design |
| **presentation** | Live presenters | +3 | +1 | +2 | All of `project` + live projection rules (48pt+ fonts, 10-20m) |
| **library** | Library contributors | 3 | -- | 2 | Test, lint, deploy the StreamTeX library |
| **documentation** | Manual authors | 10 | 2 | 3 | Multi-manual coordination, course generation |

The **presentation** profile extends **project** -- it includes everything from project plus presentation-specific audit/fix rules (auto-detected by `/stx-designer:audit` and `/stx-designer:fix`), 1 additional agent (Presentation Designer), and 2 additional skills (presentation design rules, survey chart conversion).

### Installation

```bash
stx claude install project ./my-project           # Standard project
stx claude install presentation ./my-presentation  # With projection rules
stx claude install library ./streamtex             # Library development
stx claude install documentation ./streamtex-docs  # Documentation authoring
```

### Update & Sync

```bash
stx claude check                  # Check sync status of all workspace profiles
stx claude diff .                 # Show differences for current project
stx claude update .               # Update current project (preserves CLAUDE.md)
stx claude update . --force       # Update including CLAUDE.md override
stx claude update --all           # Update ALL projects in workspace
stx claude update --all --force   # Update all, overwrite CLAUDE.md everywhere
```

### Profile Marker

Installed profiles are identified by the `.claude/.stx-profile` marker file. This is how `stx claude check` and `stx claude update --all` discover projects.

### Installed File Structure

```
your-project/
├── CLAUDE.md                  # AI assistant instructions (preserved on update)
└── .claude/
    ├── settings.json          # Claude Code permissions
    ├── .stx-profile           # Profile type marker
    ├── commands/
    │   ├── stx-guide.md       # Global ecosystem guide
    │   ├── stx-designer/      # /stx-designer:* commands (init, update, audit, fix, tool)
    │   └── developer/         # /developer:* commands
    ├── references/
    │   ├── coding_standards.md
    │   └── streamtex_cheatsheet_en.md (or presentation_cheatsheet_en.md)
    ├── designer/
    │   ├── agents/            # AI agent definitions
    │   └── skills/            # Design knowledge (blueprints, rules, conventions)
    └── developer/
        └── skills/            # Developer knowledge (testing patterns)
```

Shared files (`references/` and `commands/`) are set read-only (0o444) to indicate they are managed automatically.

### What Gets Updated

| Source in `streamtex-claude/` | Destination in each project |
|---|---|
| `shared/references/*.md` | `.claude/references/` |
| `shared/commands/*.md` | `.claude/commands/` (per-project) + `~/.claude/commands/` (global) |
| `profiles/<profile>/commands/` | `.claude/commands/` |
| `profiles/<profile>/*/skills/` | `.claude/*/skills/` |
| `profiles/<profile>/*/agents/` | `.claude/*/agents/` |
| `profiles/<profile>/CLAUDE.md` | `CLAUDE.md` (preserved unless `--force`) |

---

## 2. /stx-designer:init -- Create a New Project

```
/stx-designer:init "Docker course for beginners, 8 slides, dark presentation style"
/stx-designer:init "technical REST API documentation, 12 sections, with code examples"
/stx-designer:init --collection "my_course_library"
```

**Trigger**: Natural language description of the desired project.

**Templates** (auto-detected from description, or specify explicitly):
- **project** (default) -- standard StreamTeX project
- **presentation** -- project with live projection rules
- **collection** -- multi-project hub with `st_collection`, `collection.toml`, home page with project cards
- **course** -- course project with `blocks.csv` and book generator

**What it reads before generating**:
1. `coding_standards.md` -- coding rules
2. `streamtex_cheatsheet_en.md` -- syntax reference
3. `visual-design-rules.md` -- visual quality rules
4. `style-conventions.md` -- style naming and composition
5. `block-blueprints.md` -- 12 block templates
6. `project-architect.md` -- structure planning agent
7. Existing `book.py` (if project already scaffolded)

**Workflow**:
1. **Analyze** -- extracts type (presentation/documentation/collection), slide count, theme, features, audience
2. **Propose** -- adopts Project Architect role, proposes block list with blueprints, features, palette
3. **Confirm** -- asks for explicit approval before generating
4. **Generate** -- creates all `blocks/bck_NN_*.py`, updates `book.py`, adapts `custom/styles.py` and `custom/themes.py`
5. **Validate** -- checks all blocks have `build()`, book references all blocks, styles are consistent

**Defaults** (when information is missing): type=presentation, theme=dark, TOC=SIDEBAR_ONLY with max_level=2, sidebar=expanded, pagination=yes, audience=screen.

**Constraints**: max 15 blocks per project (suggest collection otherwise), always include title (Blueprint 1) and conclusion (Blueprint 10), no Lorem Ipsum (use `[TODO: ...]` placeholders).

**Collection mode** (`--collection`): Creates a collection directory with: `book.py` (uses `st_collection`), `collection.toml`, `blocks/bck_home.py` (home page with project cards), `custom/styles.py`, `custom/themes.py`, `.streamlit/config.toml`, and `static/images/covers/`. After scaffolding, asks about projects (names, descriptions, ports) and updates `collection.toml`.

---

## 3. /stx-designer:update -- Add, Modify, Migrate, Export

The `update` command covers all content modification operations: adding blocks/slides, customizing themes, upgrading structure, migrating HTML, exporting, and generating course books.

### Adding content

```
/stx-designer:update add block bck_intro_welcome - Welcome screen with title and subtitle
/stx-designer:update add block comparison VM vs Containers, 2-column grid
/stx-designer:update add slide bck_19_zoom - Zoom controls demo
```

**Block creation with blueprint matching**: Consults `block-blueprints.md` and matches the description to one of 12 blueprints. Common matches:
- "title slide" -> Blueprint 1 (Title)
- "comparison X vs Y" -> Blueprint 4 (Two-Column Comparison)
- "code demo" -> Blueprint 6 (Code + Result)
- "steps / process" -> Blueprint 7 (Timeline)
- "summary / conclusion" -> Blueprint 10 (Conclusion)
- "AI-generated image" -> Blueprint 11 (AI Image + Text)
- "interactive image lab" -> Blueprint 12 (Interactive Image Lab)

**Slide creation**: Reads `visual-design-rules.md` and `style-conventions.md`, creates block file with standard imports, `BlockStyles` (heading + sub), `bs` alias, `build()` function. Wraps content in `with st_block(s.center_txt):`, follows canonical section structure (subtitle -> explanation -> code -> rendering -> details), validates line length, `show_code()` placement, and body text size.

**Block naming**: `bck_NN_description.py` (NN = 2-digit sequence number)

### Customizing an existing project

```
/stx-designer:update change to light theme with green palette
/stx-designer:update add TOC sidebar with numbering, enable pagination
/stx-designer:update adapt for auditorium projection (large text)
```

**Customization domains**:
1. **Theme & Colors** -- palette (primary, accent, highlight, success, muted), dark/light base, background colors
2. **Typography** -- font sizes (screen: `s.large` body vs auditorium: `s.Large` body), title hierarchy
3. **Navigation** -- TOC (on/off, numbering mode, max level), sidebar state, pagination, marker, banner
4. **Features** -- HTML export, inspector, zoom, collection mode

Always reads current configuration, proposes a diff, and asks for confirmation before applying.

### Upgrading structure (`--upgrade`)

```
/stx-designer:update --upgrade
```

Compares project boilerplate files (`blocks/__init__.py`, `blocks/helpers.py`, `setup.py`, `.streamlit/config.toml`) against the template and applies safe updates. Does NOT modify `custom/styles.py`, `custom/themes.py`, or block content files.

### Generating course book.py (`course`)

```
/stx-designer:update course gai4as
/stx-designer:update course --all
```

Reads `blocks.csv` in the course directory, runs the book generator tool, and produces a wired `book.py`.

### Migrating HTML to StreamTeX (`--migrate`)

```
/stx-designer:update --migrate bck_overview
/stx-designer:update --migrate --all
```

The most comprehensive migration operation. Accepts raw HTML (from Google Docs export) inline or as a file path.

**Phase 1: Analysis** -- filter CSS class noise, identify defaults (black/white = theme-controlled), mandatory color audit (every color value enumerated and mapped), detect formatting (bold, italic), identify containers (tables -> `st_grid()`, lists -> `st_list()`).

**Phase 2: Implementation** -- create block file with `BlockStyles` (color-mapping summary + dropped-colors log), implement `build()` using StreamTeX components only: one `st_write()` with tuples for inline mixed-style text, `st_grid()` with `cell_styles` for tables, `st_list()` for lists, `st_br()` for line breaks.

**Phase 3: Second-pass verification** (mandatory) -- re-read source HTML top-to-bottom, re-read migration rules, fix mismatches, run checklist (no raw HTML, semantic style names, images renamed, inline content uses ONE `st_write`, font sizes on link styles, no hardcoded black/white, all colors mapped).

**Batch migration** (`--migrate --all`): Runs the batch converter pipeline on `exports/html/`, validates generated blocks, reports conversion stats (simple/medium/complex/errors).

**Single block migration** (`--migrate <block_name>`): Reads source HTML from `exports/html/<name>/index.html`, determines block family (`bckcp_*` = doc styles, `bck_*` = presentation styles), generates the StreamTeX block, runs second-pass verification, writes to `shared/blocks/`.

### Configuring HTML export (`--export`)

```
/stx-designer:update --export
/stx-designer:update --export projects/my-project
```

Verifies export readiness (`export=True` in `st_book()`), audits all blocks for export-aware widget usage (bare `st.*` calls that should be `stx.*`), checks image assets, and guides the user through the export process. Key reminders:
- `st.dataframe()` -> `stx.st_dataframe()`
- `st.line_chart()` -> `stx.st_line_chart()`
- `st.graphviz_chart()` -> `stx.st_graphviz()`
- For unsupported widgets: `with stx.st_export('<p>fallback</p>'): st.plotly_chart(fig)`

---

## 4. /stx-designer:audit -- Check Quality

```
/stx-designer:audit --target bck_04_text_styles
/stx-designer:audit --target styles
/stx-designer:audit --all
/stx-designer:audit presentation
```

### Block/slide audit (`--target <block>`)

**Checklist** (reports violations with line numbers):
- Block structure: `BlockStyles` class, `bs` alias, `build()` function
- Centered content: `with st_block(s.center_txt):`
- Heading: main heading uses `tag=t.div, toc_lvl="1"`
- Line length: no visible text > ~45 characters
- No multi-arg string concatenation in `st_write()`
- Code before rendering: every live example preceded by `show_code()`
- Multi-line strings: `show_explanation()`, `show_details()`, `show_code()` use `"""\..."""`
- Body text size: `s.large` (32pt), not `s.big`
- Spacing: `st_space("v", 2)` between sections, `st_space("v", 1)` within

Output: PASS/ERROR/WARNING per rule with suggested fixes.

**Structure and assets validation** (also performed by `--target <block>`):
1. **Structural** -- mandatory imports, `BlockStyles` class, `build()`, no raw HTML/CSS
2. **Asset** -- all `uri=` values in `st_image()` checked against `static/images/`
3. **Style** -- all referenced styles resolved (BlockStyles, custom/styles.py, streamtex.styles)
4. **TOC** -- heading hierarchy analysis, level jump detection
5. **Layout** -- grid/block/span/list/overlay counts, nesting depth check (warn if > 4)
6. **Report** -- structured summary with status, counts, and issues

### Style audit (`--target styles`)

```
/stx-designer:audit --target styles
/stx-designer:audit --target styles blocks/bck_example.py
```

**Critical issues**: raw HTML/CSS strings, hardcoded black/white, multiple `st_write` for inline text, missing font size on links.

**Warnings**: duplicate style definitions, non-English style names, unused styles, missing `BlockStyles` class, raw `st.*` for content.

**Recommendations**: dark mode compatibility, style reuse opportunities, missing TOC entries.

### Migration audit

```
/stx-designer:audit migration bck_ethics_overview
```

Reads original HTML and converted block side-by-side, runs validation tool, checks: color fidelity, no raw HTML/CSS, images referenced via registry, inline mixed-style uses ONE `st_write()`, links include font-size, tables use `st_grid()`, lists use `st_list()`, correct family (pres/doc), `BlockStyles` has color-mapping summary and dropped-colors log.

### Presentation audit (auto-detected with presentation profile)

When the **presentation** profile is active, audit automatically includes live projection compliance checks:

**CRITICAL checks** (must fix before presenting):
1. Body text uses `s.Large` (48pt) or above -- `s.large`, `s.big`, `s.medium` on body = CRITICAL
2. Section titles use `s.Huge` (96pt) or project title styles
3. No bullet exceeds 7 words, no section has more than 3 bullets
4. No `muted` or `subtle` color on body text (only on attribution/source)
5. No image below 400px width (except logos)

**ERROR checks**: generous spacing (`st_space(size=3)` minimum between sections), one idea per section, no helper boxes (`show_explanation`, `show_details`, `show_code`), chart label readability (>= 20px), visual anchor in every section.

**WARNING checks**: spacing consistency, style reuse, attribution size.

---

## 5. /stx-designer:fix -- Auto-Fix Issues

```
/stx-designer:fix --target bck_04_text_styles
/stx-designer:fix --target styles
/stx-designer:fix --all
```

### Block/slide fix (`--target <block>`)

Runs audit internally, then applies fixes:
- Long lines -> break into `st_write()` + `st_br()` pattern
- Missing `show_code()` -> add before live rendering
- String concatenation -> split into separate calls
- Wrong font size -> replace `s.big` with `s.large`
- Old varargs pattern -> convert to `"""\..."""`

Only modifies what violates the rules; preserves existing content and structure.

### Style fix (`--target styles`)

```
/stx-designer:fix --target styles blocks/bck_example.py
```

Identifies repeated style patterns, extracts them to `BlockStyles` or `custom/styles.py`, checks style naming conventions (English-only, generic, descriptive), applies refactoring, and runs tests to verify.

### Presentation fix (auto-detected with presentation profile)

When the **presentation** profile is active, fix automatically includes live projection corrections:

1. Small body fonts (`s.medium`, `s.big`, `s.large`) -> `s.Large` (48pt)
2. Small title fonts -> `s.Huge` (96pt)+
3. Long text -> keyword phrases (5-7 words, max 3 bullets)
4. Muted/subtle body -> primary/accent colors
5. Insufficient spacing -> `st_space(size=3)` or `st_space(size=4)`
6. Helper boxes -> direct `st_write()` content
7. Small images -> 400px+ width
8. Chart CSS -> 24px+ font sizes

---

## 6. /stx-designer:tool -- Specialized Tools

### survey-convert

```
/stx-designer:tool survey-convert                           # Interactive (list temp/ images)
/stx-designer:tool survey-convert --all                     # Batch convert all in temp/
/stx-designer:tool survey-convert --list                    # List images without converting
/stx-designer:tool survey-convert path/to/screenshot.png    # Convert specific image
/stx-designer:tool survey-convert --all /path/to/folder     # Batch from custom folder
```

Converts Stack Overflow Developer Survey screenshots into code-generated StreamTeX blocks. The screenshot is the source reference only -- the output is pure Python code that reproduces the chart (zero static image dependency).

Workflow: read image -> extract chart data (labels + percentages) -> extract metadata (title, description, question, tab, response count) -> distill keywords (2-3 stats, 5-7 words each) -> generate block with `SURVEY_DATA` and `_render_bars()` -> register in `book.py`.

---

## 7. Developer Commands

### /developer:test-run

```
/developer:test-run
```

1. Runs `uv run pytest tests/ -v` from the project root
2. Analyzes failures and suggests fixes
3. Reports total passed/failed count

### /developer:lint

```
/developer:lint
```

1. Runs `uv run ruff check` from the project root (targets `streamtex/` for library, `.` for projects)
2. If auto-fixable issues exist, runs `uv run ruff check --fix`
3. Reports remaining issues needing manual attention
4. Runs `uv run pytest tests/ -v` to confirm fixes did not break anything
5. Recommends `uv run pre-commit install` if not installed

---

## 8. AI Agents

### Project Architect

**Profile**: project | **Invoked by**: `/stx-designer:init` (implicit) or direct invocation

**Role**: Designs the structure of StreamTeX projects -- determines block count, content, order, and features (pagination, TOC, banner, export).

**Design principles**:
- One block = one idea/topic
- Logical order: introduction -> development -> conclusion
- Max 15 blocks per project (beyond that, suggest collection)
- Naming: `bck_NN_short_description.py`
- Pedagogical progression: context -> concepts -> demos -> exercises -> conclusion

**Feature selection by type**:

| Type | Pagination | TOC | Banner | Marker | Export |
|------|-----------|-----|--------|--------|--------|
| Auditorium presentation | yes | SIDEBAR_ONLY, max_level=2 | yes | yes | no |
| Screen presentation | yes | SIDEBAR_ONLY, max_level=2 | optional | yes | optional |
| Documentation | no (scroll) | SIDEBAR_ONLY, max_level=2 | no | no | yes |
| Collection | no | SIDEBAR_ONLY, max_level=2 | no | no | no |

**Text sizing by audience**:

| Audience | Body | Titles | Code |
|----------|------|--------|------|
| Auditorium (projection) | `s.Large` (48pt) min | `s.huge` (80pt) | 20pt |
| Screen (individual) | `s.large` (32pt) | `s.huge` (80pt) | 18pt |
| Documentation (reading) | `s.large` (32pt) | `s.Large` (48pt) | 16pt |

### Slide Designer

**Profile**: project | **Purpose**: Creates visually polished, well-structured slide content

**Core principles**:
- **L1/L2/L3 Grid System**: every slide uses a 3-row grid structure (L1 headline, L2 two-column content, L3 question/transition). Each slide may use 1, 2, or all 3 rows.
- **16:9 viewport**: every slide fits one screen, no scrolling
- **Telegraphic text**: 3-7 words per bullet, 3-5 bullets max
- **Bold colored keywords** for targeted emphasis (not overused)
- **Dark theme** by default, never hardcode light colors
- **Minimum 24pt** (`s.big`) for any text, prefer 32pt (`s.large`) for body

**Image strategy**:
- User provides images: use in L2 image cell
- AI generation configured: use `st_ai_image(prompt)` directly
- No image, no AI config: insert placeholder + generation prompt + filename suggestion
- Batch generation: use `generate_image(prompt)` then reference file with `st_image(uri=path)`

**Anti-patterns**: full sentences as bullets, fixed grid columns (`cols=2`), hardcoded light colors, font below 24pt, missing image placeholder, raw CSS in blocks.

### Slide Reviewer

**Profile**: project | **Purpose**: Reviews and validates completed slides

**Review checklist**:
- **Structure**: `BlockStyles` with heading/sub, `bs` alias, `build()`, content wrapped in `st_block(s.center_txt)`
- **Visual quality**: no text > ~45 chars, no multi-arg concatenation, body text `s.large`, proper spacing
- **Pedagogical completeness**: `show_code()` before renderings, `show_explanation()` before examples, WRONG boxes explain WHY, `show_details()` documents defaults
- **Text formatting**: all helper calls use `"""\..."""` (auto-dedented)
- **Style compliance**: no hardcoded colors, no raw HTML/CSS

Output: score X/Y, errors (must fix), warnings (should fix), suggestions.

### Presentation Designer

**Profile**: presentation (overlay) | **Purpose**: Specialist for live projection at 10-20m distance

**Key differences from Slide Designer**:
- Body text at `s.Large` (48pt) instead of `s.large` (32pt)
- Titles at `s.Huge` (96pt)+
- Max 5-7 words per bullet, max 3 bullets per section
- Never use `muted`/`subtle` on body text
- `st_space(size=4)` between major sections
- No helper boxes (`show_explanation`, `show_details`, `show_code`)
- Visual first: charts/images > bullet points > paragraphs

---

## 9. Block Blueprints (12 types)

Blueprints define the **structure** (which `stx.*` calls, in which order), not the exact content. Content is always adapted to the user's request.

| # | Blueprint | When to Use | Key Structure |
|---|-----------|-------------|---------------|
| 1 | **Title** | First slide, landing page | `st_space` + title (`s.huge`) + subtitle + author, centered |
| 2 | **Section Header** | Transition between major parts | Section number (`s.huge`) + title (`s.LARGE`) + description |
| 3 | **Text Content** | Explain a concept, list key points | Heading + `st_list` with bullet points |
| 4 | **Two-Column Comparison** | X vs Y, pros/cons, before/after | Heading + `st_grid(repeat(auto-fit,...))` with 2 bullet lists |
| 5 | **Image + Text** | Illustrate with diagram/photo | Heading + `st_grid`: image cell + text cell |
| 6 | **Code + Result** | Code demo, syntax examples | Heading + `st_grid`: `st_code` cell + result cell |
| 7 | **Timeline / Steps** | Process, workflow, methodology | Heading + numbered steps with `st_grid(cols="80px 1fr")` |
| 8 | **Quote / Highlight** | Key message, intermediate conclusion | `st_block` quote box + attribution |
| 9 | **Image Gallery** | Portfolio, screenshots | Heading + `st_grid(repeat(auto-fit, minmax(200px,...)))` |
| 10 | **Conclusion** | Last slide, key takeaways | Heading + bullet list + next steps |
| 11 | **AI Image + Text** | Illustration without image file | Like Blueprint 5 but uses `st_ai_image(prompt)` instead of `st_image()` |
| 12 | **Interactive Image Lab** | Workshop, hands-on demo | `st_ai_image_widget()` with default prompt and controls |

**Quick matching guide**:

| User requests... | Blueprint |
|------------------|-----------|
| "title slide", "landing page" | 1 -- Title |
| "section introduction", "transition" | 2 -- Section Header |
| "slide with bullets", "explain X" | 3 -- Text Content |
| "comparison X vs Y", "pros/cons" | 4 -- Comparison |
| "image with text", "diagram + explanation" | 5 -- Image + Text |
| "code demo", "syntax example" | 6 -- Code + Result |
| "steps", "process", "workflow" | 7 -- Timeline |
| "quote", "key message", "highlight" | 8 -- Quote |
| "gallery", "portfolio", "screenshots" | 9 -- Gallery |
| "conclusion", "summary", "key takeaways" | 10 -- Conclusion |
| "AI image", "generate image", "image from prompt" | 11 -- AI Image + Text |
| "image lab", "interactive generation", "prompt editor" | 12 -- Interactive Image Lab |

---

## 10. Coding Conventions

### Project Structure Standard

```
project_name/
  book.py                  # Entry point (imports setup, calls st_book())
  setup.py                 # PATH setup (adds parent dir to sys.path)
  blocks/                  # Content modules
    __init__.py            # ProjectBlockRegistry lazy loader
    helpers.py             # BlockHelperConfig (DI for show_code, show_explanation, etc.)
    bck_*.py               # Each block has a build() function
  custom/
    __init__.py            # Required (namespace package fix)
    styles.py              # Project-specific styles (inherits StxStyles)
    themes.py              # Theme overrides (dict)
  static/images/           # Image assets
  .streamlit/config.toml   # MUST have enableStaticServing = true
```

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Block files | `bck_[description]_[suffix].py` | `bck_intro_welcome.py` |
| Numbered blocks | `bck_NN_description.py` | `bck_01_title.py` |
| Image assets | `[block_name]_image_[00index].[ext]` | `bck_intro_welcome_image_00.png` |
| Style names | English-only, generic, descriptive | `title_giant_green`, `subtitle_blue_01` |
| Style classes | `BlockStyles` or `BStyles` | Always aliased as `bs = BlockStyles` |
| Variables | `snake_case` | `header_text` |
| Classes | `PascalCase` | `BlockStyles` |

> **Naming advice**: Use descriptive block names (`bck_docker_architecture`, `bck_intro_welcome`), NOT numbered prefixes (`bck_01_slide`, `bck_03_slide`). Numbered prefixes are not maintainable -- inserting a new block forces renaming all subsequent files and their image references. The block ordering is defined in `book.py`.

### Mandatory Imports (block files)

```python
import streamlit as st
from streamtex import *
import streamtex as stx
from streamtex.styles import Style as ns, StyleGrid as sg
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s
from blocks.helpers import show_code, show_explanation, show_details
```

### Mandatory Imports (book.py)

```python
import streamlit as st
import setup
import blocks
```

### Theme Injection (book.py)

```python
# Apply a custom theme before calling st_book()
from custom.themes import dark
import streamtex.styles as sts
sts.theme = dark
```

### Page Config (book.py)

```python
# Must be the first Streamlit call in the script
st.set_page_config(page_title="...", layout="wide", initial_sidebar_state="expanded")
```

### stx.* vs st.* (content vs interactivity)

| Use | API | Examples |
|-----|-----|---------|
| ALL layout and content | `stx.*` | `st_write`, `st_image`, `st_grid`, `st_list`, `st_block`, `st_span`, `st_space`, `st_br`, `st_overlay`, `st_html` |
| AI image generation | `stx.*` | `st_ai_image`, `st_ai_image_widget`, `generate_image` |
| Data visualization (export-aware) | `stx.*` | `st_dataframe`, `st_table`, `st_metric`, `st_json`, `st_graphviz`, `st_line_chart`, `st_bar_chart` |
| ONLY interactivity | `st.*` | `st.button`, `st.slider`, `st.selectbox`, `st.checkbox`, `st.text_input` |

### Block File Structure

```python
class BlockStyles:
    """Short description."""
    heading = s.project.titles.section_title + s.center_txt
    sub = s.project.titles.section_subtitle
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        st_write(bs.heading, "Title", tag=t.div, toc_lvl="1")
        st_space("v", 2)
        # ... sections follow canonical structure
```

### Dark Theme Defaults

```python
# custom/themes.py — Dark palette example
class DarkTheme:
    bg_main = Style("background-color: #0E1117;", "bg_main")
    bg_sidebar = Style("background-color: #262730;", "bg_sidebar")
    text_primary = Style("color: #FAFAFA;", "text_primary")
    text_secondary = Style("color: #B0B0B0;", "text_secondary")
    accent = Style("color: #FF4B4B;", "accent")
    border = Style("border-color: #333333;", "border")
```

> **Rule**: NEVER hardcode `color: black` or `background: white`. Use theme-aware styles.

### Style Composition

```python
# Combine styles with +
title_style = s.bold + s.Large + s.text.colors.blue

# Remove properties with -
no_bold = title_style - s.bold

# Create from CSS string
container = Style("background: linear-gradient(...); border-radius: 12px;", "container_modern")

# Copy with new ID
my_title = Style.create(s.Large + s.bold, "my_title")
```

### Style Hierarchy

```
s.text.*         -- text colors, sizes, weights, decorations, fonts, alignments
s.container.*    -- sizes, bg_colors, borders, paddings, margins, layouts, flex
s.project.*      -- project-specific custom styles (colors, titles, containers)
s.visibility.*   -- hidden, visible, invisible
```

### Image Editing (new in 0.5)

Use `st_image(editable=True)` for all editable images. `st_ai_image()` is deprecated — use `st_image(prompt=..., editable=True)` instead.

```python
# Old (deprecated)
st_ai_image("A sunset", provider="openai")

# New (recommended)
st_image(s.none, uri="path.png", editable=True, name="hero", prompt="A sunset", provider="openai")
```

### Common Gotchas

1. **`from streamtex import *` shadows `list()`**: Use `[*iterable]` instead of `list(iterable)`.

2. **Multiple `st_write()` calls stack vertically**: For inline mixed-style text, use ONE `st_write()` with tuple arguments:
   ```python
   # WRONG -- stacks vertically
   st_write(s.red, "Red")
   st_write(s.blue, "Blue")

   # CORRECT -- flows inline
   st_write(s.Large, (s.red, "Red"), (s.blue, "Blue"))
   ```

3. **`show_explanation()` is a function, not a context manager**: Call directly with a string argument. Auto-dedents `"""\..."""` content -- never wrap with `textwrap.dedent()`.

4. **Links default to 12pt**: Include font size in link style when surrounding text is larger.

5. **No hardcoded black/white**: Let Streamlit handle Light/Dark mode via style system.

6. **No raw HTML/CSS in Python**: Use `Style()` constructor, `Style.create()`, or style composition with `+`.

7. **Fixed grid columns break on narrow screens**: Always use `repeat(auto-fit, minmax(350px, 1fr))` for responsive layouts.

---

## 11. Testing & Linting

### Running Tests

```bash
# Via stx shortcuts
stx test                          # All tests
stx test -v                       # Verbose
stx test -- -k "test_write"      # Filter by name

# Via uv directly
uv run pytest tests/ -v           # All tests verbose
uv run pytest tests/test_export.py -v  # Specific file
```

### Running Linter

```bash
# Via stx shortcuts
stx lint                          # Check only
stx lint -- --fix                 # Auto-fix

# Via uv directly
uv run ruff check .               # Project-level check
uv run ruff check streamtex/      # Library-level check
uv run ruff check --fix .         # Auto-fix
```

### Mandatory Ruff Config

Every StreamTeX project `pyproject.toml` MUST include:

```toml
[tool.ruff.lint]
ignore = ["F403", "F405", "E701", "E741"]
```

Why these rules are suppressed:
- **F403/F405** -- `from streamtex import *` is the standard import pattern
- **E701** -- `with l.item(): st_write("text")` one-liner list items are idiomatic
- **E741** -- `as l` variable name in `with st_list(...) as l:` is standard

### Pre-commit Hooks

Every StreamTeX repo and project MUST have `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.2
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

Setup:

```bash
uv sync                       # Installs pre-commit (dev dep)
uv run pre-commit install     # Activates the git hook
```

`stx project new` generates `.pre-commit-config.yaml` and installs hooks automatically. `stx workspace update` installs hooks in all repos and projects.

### CI Configuration

Projects with `[tool.uv.sources]` (editable local sources) MUST use `UV_NO_SOURCES=1` in CI:

```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    env:
      UV_NO_SOURCES: 1    # Ignore [tool.uv.sources] -- resolve from PyPI
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync            # NOT --frozen (lock file encodes local path)
      - run: uv run ruff check .
```

---

## 12. Workspace Management

### Core Commands

```bash
stx workspace init [PATH]            # Initialize workspace (creates stx.toml + projects/)
stx workspace update                 # Pull + clone + sync + hooks + profiles + global commands
stx workspace status                 # Git status of all repos (branch, clean/dirty, ahead/behind)
stx workspace upgrade PRESET         # Upgrade to higher preset (cannot downgrade)
```

### Presets

| Preset | Repos Included | Audience |
|--------|---------------|----------|
| **basic** | none | Standalone projects |
| **user** | streamtex-claude | Users wanting Claude profiles only |
| **standard** | streamtex-docs + streamtex-claude | Default -- docs + profiles |
| **developer** | all 3 repos (library + docs + claude) | Library contributors |

```bash
stx workspace init . --preset user       # Lighter setup (Claude profiles only)
stx workspace init . --preset developer  # Full development setup
stx workspace upgrade developer          # Upgrade existing workspace
```

### stx workspace update Options

```bash
stx workspace update                    # Full update (pull + sync + hooks + profiles + commands)
stx workspace update --skip-sync        # Skip uv sync
stx workspace update --skip-profiles    # Skip Claude profile update
stx workspace update --dry-run          # Show steps without executing
stx workspace update --repair           # Enable repair checks (venv, __init__.py, paths)
```

### stx.toml Configuration

The `stx.toml` file at workspace root declares repos, their URLs, and types. It is created by `stx workspace init` and updated by `stx workspace upgrade`.

### pyrightconfig.json for IDE

For basedpyright/pyright to resolve `streamtex` imports in the dev workspace:

```json
// streamtex-dev/pyrightconfig.json
{"extraPaths": ["streamtex"]}
```

Each sub-project also needs `[tool.pyright] extraPaths` in `pyproject.toml`:
- `streamtex-docs/pyproject.toml`: `extraPaths = ["../streamtex"]`
- `projects/*/pyproject.toml`: `extraPaths = ["../../streamtex"]`

After changes, restart the language server: `Cmd+Shift+P` -> `basedpyright: Restart Server`.

---

## 13. Typical Workflows

### Create a project from scratch

```bash
# 1. Set up workspace (one-time)
mkdir streamtex-dev && cd streamtex-dev
stx workspace init .
stx workspace update

# 2. Scaffold project
stx project new my-course

# 3. Enter project and open Claude Code
cd projects/stx-my-course
claude

# 4. Use Claude to generate the full project
> /stx-designer:init "Introduction to Python, 10 slides, dark theme, for students"
# Claude proposes structure with blueprints, you approve, files are generated

# 5. Preview
> uv run streamlit run book.py

# 6. Refine individual slides
> /stx-designer:fix --target bck_03_variables
```

### Add blocks to an existing project

```bash
# In Claude Code, from the project directory:

# Create a new block using blueprint matching
> /stx-designer:update add block comparison Python vs Java, 2-column grid with pros/cons
# Claude matches Blueprint 4, creates the file, shows wiring instructions

# Or create a slide with full design rules
> /stx-designer:update add slide bck_08_demo - Live code demo with input/output

# Wire it into book.py manually:
# import blocks
# st_book([..., blocks.bck_08_demo], toc_config=toc)
```

### Audit and fix a project

```bash
# In Claude Code:

# 1. Check style consistency across all blocks
> /stx-designer:audit --target styles

# 2. Validate design rules on a specific block
> /stx-designer:audit --target bck_05_architecture

# 3. Auto-fix violations
> /stx-designer:fix --target bck_05_architecture

# 4. Refactor repeated styles
> /stx-designer:fix --target styles blocks/bck_05_architecture.py

# 5. Validate structure and assets
> /stx-designer:audit --target bck_05_architecture

# For presentation projects (presentation profile -- auto-detected):
> /stx-designer:audit --target bck_05_architecture
> /stx-designer:fix --target bck_05_architecture
```

### Maintain and update profiles

```bash
# After a new StreamTeX release:

# 1. Update CLI
uv tool install "streamtex[cli]" -U

# 2. Update everything in workspace
cd streamtex-dev/
stx workspace update

# 3. Verify all profiles are in sync
stx claude check

# Fine-grained control for a single project:
cd projects/stx-my-course/
stx claude diff .                 # See what changed
stx claude update .               # Update (preserves CLAUDE.md)
stx claude update . --force       # Override everything
```

### Migrate HTML content to StreamTeX

```bash
# In Claude Code, from the project directory:

# 1. Single block migration (provide HTML inline or as file path)
> /stx-designer:update --migrate bck_overview
# Claude reads HTML, extracts colors/formatting, generates StreamTeX block

# 2. Batch conversion (for large-scale migrations)
> /stx-designer:update --migrate --all
# Converts all HTML files in exports/html/, validates results

# 3. Audit conversion quality
> /stx-designer:audit migration bck_overview
# Compares original HTML with converted block, checks fidelity

# 4. Configure HTML export for the project
> /stx-designer:update --export
# Checks export readiness, audits widgets, guides through export

# 5. Generate book.py from CSV block list (after batch conversion)
> /stx-designer:update course --all
```

### Deploy a project

```bash
# Pre-flight checks
stx deploy preflight .

# Docker (local)
stx deploy docker . --port 8501

# Render (generate config)
stx deploy render . --name my-service --branch main
# Then: git push, connect repo on Render dashboard

# HuggingFace Spaces
stx deploy huggingface . --space https://huggingface.co/spaces/user/repo
```
