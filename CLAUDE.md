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

## Gotchas critiques (generation de code)

### `show_explanation()` est une fonction, PAS un context manager
`show_explanation("texte")` cree un cadre, ecrit le texte, et **ferme le cadre** en retournant.
Tout ce qui suit (st_list, st_write, etc.) est rendu **en dehors** du cadre.
- **MAUVAIS** : `show_explanation("intro")` suivi de `st_list(...)` → liste hors du cadre
- **BON** : `with st_block(s.project.containers.explanation_box):` puis `st_write(...)` + `st_list(...)` a l'interieur
- Meme logique pour `show_details()` et `show_code()` — ce sont des fonctions, pas des context managers

### `from streamtex import *` masque `list()`
`st_list` ecrase le builtin Python `list()`. Utiliser `[*iterable]` au lieu de `list(iterable)`.

### Styles inline multiples : UN seul `st_write` avec des tuples
Plusieurs appels `st_write` s'empilent verticalement. Pour du texte inline avec des styles differents :
`st_write(s.Large, (s.red, "Rouge "), (s.blue, "Bleu"))` — un seul appel.

## Release workflow (publication PyPI)
1. Bumper la version dans `pyproject.toml` + `streamtex/__init__.py` (dans le repo `streamtex`)
2. `uv run pytest tests/ -v && uv run ruff check streamtex/`
3. `uv lock && git add pyproject.toml streamtex/__init__.py uv.lock && git commit && git push`
4. `gh release create vX.Y.Z -R nicolasguelfi/streamtex` → declenche publish.yml → PyPI

## Render Deploy — Mode Manuel Actif
Le trigger `push` est **desactive** dans `.github/workflows/render-deploy.yml` (free tier limits).
- Les deploys se font **uniquement** via : `gh workflow run render-deploy.yml -R nicolasguelfi/streamtex-docs`
- **Apres une serie de commits importants sur les manuels**, propose a l'utilisateur de declencher un deploy manuel
- Pour reactiver l'auto-deploy quand la doc est stable : decommenter les lignes `push` dans le workflow

## CLI — Commande unifiee install/upgrade
Toujours utiliser `uv tool install "streamtex[cli]" -U` dans la doc et les instructions utilisateur.
Cette commande fonctionne pour l'installation ET la mise a jour. Ne PAS utiliser `uv tool upgrade` (echoue si pas deja installe).

## Workflows
1. **New Block** -> Read coding_standards.md, inspect existing blocks (`/designer:block-new`)
2. **New Slide** -> Read designer skills (`/designer:slide-new`)
3. **Generate Course** -> Generate book.py from blocks.csv (`/project:course-generate`)
4. **Testing** -> `uv run pytest tests/ -v` (`/developer:test-run`)
5. **Linting** -> `uv run ruff check` (`/developer:lint`)
