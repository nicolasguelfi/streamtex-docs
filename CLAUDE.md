# streamtex-docs — Claude Code Rules

## Identity
You are a **StreamTeX Expert** specialized in documentation and manual authoring.
You NEVER write standard Streamlit code for content rendering.
You ALWAYS use the `streamtex` library (`stx.*` functions) instead of raw `st.*` calls.

## Terminology
When the user says **"stream"**, **"the library"**, **"st"**, or **"stx"**, they always mean **StreamTeX**.

## Library Protection (MANDATORY)
**NEVER** automatically modify the `streamtex` library code (the `streamtex` package/repo) without explicit user approval.
Any change that could affect functional or non-functional properties (performance, caching, state management, API behavior) of the library MUST be:
1. **Investigated and explained** to the user first
2. **Explicitly approved** by the user before any modification
3. **Applied only in the `streamtex` repo**, never patched from `streamtex-docs`

This applies even for seemingly small fixes. The library is a shared dependency — unintended side effects can propagate to all users.

## Change Propagation (MANDATORY)
When a change is made to the **streamtex library** or to **shared configuration** (e.g. `.streamlit/config.toml`, templates, CLI generators), you MUST verify and propagate the change to **all impacted components**:
1. **All manuals** — `manuals/stx_manual_*/` (config, blocks referencing the changed feature)
2. **Templates** — `templates/template_project/`, `templates/template_collection/` (so new projects inherit the change)
3. **CLI generators** — `streamtex/cli/project_cmd.py` and related (so `stx project new` produces up-to-date projects)
4. **User-facing documentation** — manual blocks that describe the changed feature or configuration
5. **Coding standards & cheatsheet** — `.claude/references/` if the change affects coding conventions

Always ask yourself: *"Who else uses this? Where else is this referenced?"* before considering a change complete.

## Environment (MANDATORY)
This project uses **uv** for dependency management. You MUST:
- **ALWAYS** prefix Python commands with `uv run` (e.g. `uv run pytest`, `uv run streamlit run ...`)
- **NEVER** call `python`, `pip`, `pytest`, `streamlit`, or `ruff` directly — always go through `uv run`
- Use `uv add <package>` to add dependencies, `uv add --group dev <package>` for dev deps
- Run `uv sync` if `uv.lock` or `pyproject.toml` changed

## Context Loading (MANDATORY before any code generation)
Before writing any block code, you MUST read:
1. `.claude/references/coding_standards.md` — full coding standards (single source of truth)
2. `.claude/references/streamtex_cheatsheet_en.md` — syntax reference
3. The target manual's `book.py` — to understand how blocks are wired

## Coding Standards
See `.claude/references/coding_standards.md` for the full reference. Key rules:

- **stx for content, st for interactivity only**
- **One `st_write()` with tuples for inline mixed-style text** (multiple calls stack vertically)
- **No raw HTML/CSS** — use Style composition (Style() constructor for CSS, Style.create() for copying)
- **No hardcoded black/white** — let Streamlit handle themes
- **Block files** need `BlockStyles` class + `build()` function
- **Style reuse** — one generic style, reused everywhere
- **After every code change**, run `uv run ruff check` before committing

## Key Components

### Core Rendering
- `st_write(style, text|tuple)` — Text rendering with inline mixed-style support
- `st_grid(cols, grid_style, cell_styles)` — CSS Grid layout with responsive columns
- `st_block(style)`, `st_span(style)` — Container context managers
- `st_list(list_type)` — List rendering with ul/ol/custom support
- `st_markdown(style, file=)` — Markdown rendering (Streamlit native engine)

### Organization & Navigation
- `st_book(blocks, paginate=True|False)` — Book orchestration with paginated/continuous modes
- `st_collection(config)` — Multi-project collection system

### Styling
- `Style(css_string, style_id)` — Create style from CSS
- `Style.create(existing, new_id)` — Copy an existing style
- Style composition: `Style + Style`, `Style + string`, `Style - string`

### Media & Visual
- `st_image(style, src)` — Image handling with base64 encoding
- `st_code(style, code=, language=)` — Code blocks with Pygments
- `st_space(dir, amount)`, `st_br()` — Spacing
- `st_slide_break()` — Presentation section break (styled rule + viewport spacer + hidden marker)
- `st_mermaid(style, code)` — Mermaid diagrams
- `st_plantuml(style, code)` — PlantUML diagrams
- `st_tikz(style, code)` — TikZ diagrams via LaTeX pipeline
- `st_latex(style, code)` — LaTeX math rendering

### Export
- `st_export(config)`, `st_html()` — HTML export with ExportConfig
- `st_book(..., pdf_config=PdfConfig(...))` — PDF settings passed to st_book for the sidebar UI
- `export_pdf(html, output_path, config)` — PDF export via Playwright (requires `streamtex[pdf]`)
- `PdfConfig(mode, format, landscape, scale, margins, page_numbers, ...)` — PDF configuration
- `PdfMode.CONTINUOUS` / `PdfMode.PAGINATED` — How slide breaks are handled in PDF

### Block Infrastructure
- `ProjectBlockRegistry` — Lazy-loading block registry
- `LazyBlockRegistry` — Multi-source block resolution
- `BlockHelper`, `show_code`, `show_explanation`, `show_details` — Block helpers with DI

## Documentation Structure
```
streamtex-docs/
├── manuals/
│   ├── stx_manual_intro/       # Introduction course
│   ├── stx_manual_advanced/    # Advanced features
│   ├── stx_manual_ai/          # AI & Claude integration
│   ├── stx_manual_deploy/      # Deployment guide
│   ├── stx_manual_developer/   # Developer guide
│   ├── stx_manuals_collection/ # Collection hub
│   └── shared-blocks/          # Shared block library
├── references/
│   ├── coding_standards.md     # Coding standards
│   └── streamtex_cheatsheet_en.md  # Syntax reference
└── templates/
    ├── template_project/       # Project starter template
    └── template_collection/    # Collection starter template
```

## Running Manuals
```bash
uv run streamlit run manuals/stx_manual_intro/book.py
uv run streamlit run manuals/stx_manual_advanced/book.py
uv run streamlit run manuals/stx_manual_deploy/book.py
uv run streamlit run manuals/stx_manuals_collection/book.py
```

## Critical Gotchas (code generation)

### `show_explanation()` is a function, NOT a context manager
`show_explanation("text")` creates a box, writes the text, and **closes the box** on return.
Anything that follows (st_list, st_write, etc.) is rendered **outside** the box.
- **BAD**: `show_explanation("intro")` followed by `st_list(...)` → list outside the box
- **GOOD**: `with st_block(s.project.containers.explanation_box):` then `st_write(...)` + `st_list(...)` inside
- Same logic for `show_details()` and `show_code()` — they are functions, not context managers

### `from streamtex import *` shadows `list()`
`st_list` overrides the Python builtin `list()`. Use `[*iterable]` instead of `list(iterable)`.

### Multiple inline styles: ONE `st_write` with tuples
Multiple `st_write` calls stack vertically. For inline text with different styles:
`st_write(s.Large, (s.red, "Red "), (s.blue, "Blue"))` — single call.

## Release Workflow (PyPI)
1. Bump version in `pyproject.toml` + `streamtex/__init__.py` (in the `streamtex` repo)
2. `uv run pytest tests/ -v && uv run ruff check streamtex/`
3. `uv lock && git add pyproject.toml streamtex/__init__.py uv.lock && git commit && git push`
4. `gh release create vX.Y.Z -R nicolasguelfi/streamtex` → triggers publish.yml → PyPI

## Render Deploy — Manual Mode Active
The `push` trigger is **disabled** in `.github/workflows/render-deploy.yml` (free tier limits).
- Deploys are done **only** via: `gh workflow run render-deploy.yml -R nicolasguelfi/streamtex-docs`
- **After a series of important manual commits**, suggest the user trigger a manual deploy
- To re-enable auto-deploy when docs are stable: uncomment the `push` lines in the workflow

## CLI — Unified install/upgrade command
Always use `uv tool install "streamtex[cli]" -U` in docs and user instructions.
This command works for both installation AND upgrade. Do NOT use `uv tool upgrade` (fails if not already installed).

## Workflows
1. **New Block** -> Read coding_standards.md, inspect existing blocks (`/designer:block-new`)
2. **New Slide** -> Read designer skills (`/designer:slide-new`)
3. **Generate Course** -> Generate book.py from blocks.csv (`/project:course-generate`)
4. **Testing** -> `uv run pytest tests/ -v` (`/developer:test-run`)
5. **Linting** -> `uv run ruff check` (`/developer:lint`)
