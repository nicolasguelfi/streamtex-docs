# Multi-Theme Implementation Plan

**Strategy A: Fixed `primaryColor` + N Custom Themes**

Status: **Planned** — Not yet implemented
Date: 2026-03-06
Applies to: streamtex library (all modules) + streamtex-docs (all manuals/templates)

---

## 1. Architecture Overview

### Current State

- Each project has a `config.toml` with `[theme]` section setting `base = "dark"`, forcing dark mode
- Each project has a `custom/themes.py` defining a single `dark` dict: `{ "style_id": "css_string" }`
- The global `theme` dict in `streamtex/styles/core.py` (line 6) drives `Style.__repr__()` (line 107)
- At render time, `Style.__repr__()` returns `theme.get(self.style_id, self.css)` — if a theme override exists, it replaces the default CSS
- Export HTML hardcodes `background: #fff` in `streamtex/export.py` (line 84)
- Code highlighting uses hardcoded `style="monokai"` (dark theme only) in `streamtex/code.py`

### Target State

- **N custom themes** per project (e.g. "dark", "light", "print", "corporate")
- **Runtime theme selector** in the sidebar (user picks from available themes)
- **Export respects the selected theme** (HTML and PDF match what's on screen)
- **Streamlit chrome** (sidebar bg, page bg, text color) overridden via CSS injection
- **`primaryColor`** stays in `config.toml` (fixed accent for widgets — eliminates all risky CSS selectors)
- **`base` removed** from `config.toml` to allow Streamlit's light/dark toggle + our selector on top

### Core Mechanism

```
User selects theme "corporate"
       |
       v
themes["corporate"]["styles"]  -->  core.theme = {...}  -->  Style.__repr__() resolves overrides
themes["corporate"]["chrome"]  -->  CSS injection via st.html()  -->  .stApp, sidebar bg/color
```

---

## 2. New `themes.py` Format (BREAKING CHANGE)

### Current Format (single theme)

```python
# custom/themes.py
dark = {
    "title_style": "color: #fff; font-size: 2em;",
    "body_style": "color: #ccc; font-size: 1em;",
}
```

### New Format (N themes)

```python
# custom/themes.py
themes = {
    "dark": {
        "chrome": {
            "page_bg": "#0e1117",
            "page_text": "#fafafa",
            "sidebar_bg": "#1a1a2e",
            "sidebar_text": "#e0e0e0",
        },
        "code_highlight": "monokai",          # Pygments style name
        "styles": {
            "title_style": "color: #fff; font-size: 2em;",
            "body_style": "color: #ccc; font-size: 1em;",
        },
    },
    "light": {
        "chrome": {
            "page_bg": "#ffffff",
            "page_text": "#333333",
            "sidebar_bg": "#f0f2f6",
            "sidebar_text": "#333333",
        },
        "code_highlight": "default",
        "styles": {
            "title_style": "color: #1a1a2e; font-size: 2em;",
            "body_style": "color: #333; font-size: 1em;",
        },
    },
}

default_theme = "dark"
```

### Migration Guide

All 9 existing `themes.py` files must be migrated:

| Location | Current `primaryColor` | Action |
|---|---|---|
| `stx_manual_intro` | `#667eea` | Migrate |
| `stx_manual_advanced` | `#667eea` | Migrate |
| `stx_manual_ai` | `#8B5CF6` | Migrate |
| `stx_manual_deploy` | `#667eea` | Migrate |
| `stx_manual_developer` | `#667eea` | Migrate |
| `stx_manuals_collection` | `#667eea` | Migrate |
| `shared-blocks` | `#667eea` | Migrate |
| `template_project` | `#667eea` | Migrate |
| `template_collection` | `#1f77b4` | Migrate |

---

## 3. `config.toml` Changes (BREAKING CHANGE)

### Current (locks dark mode)

```toml
[theme]
base = "dark"
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#fafafa"
```

### New (only fixes accent color)

```toml
[theme]
primaryColor = "#667eea"
```

All other colors removed. `base` removed to allow theme switching. Background/text/sidebar colors are now controlled by Python themes + CSS injection.

Affected files (10 total):
- `manuals/stx_manual_intro/.streamlit/config.toml`
- `manuals/stx_manual_advanced/.streamlit/config.toml`
- `manuals/stx_manual_ai/.streamlit/config.toml`
- `manuals/stx_manual_deploy/.streamlit/config.toml`
- `manuals/stx_manual_developer/.streamlit/config.toml`
- `manuals/stx_manuals_collection/.streamlit/config.toml`
- `manuals/shared-blocks/.streamlit/config.toml`
- `templates/template_project/.streamlit/config.toml`
- `templates/template_collection/.streamlit/config.toml`
- Root `.streamlit/config.toml` (if exists)

---

## 4. CSS Injection for Streamlit Chrome

### Selectors Used

| Target | CSS Selector | Risk Level |
|---|---|---|
| Page background | `.stApp` | Safe — documented root container |
| Page text color | `.stApp` | Safe — inherited by all children |
| Sidebar background | `[data-testid="stSidebar"]` | Moderate — semi-stable test ID |
| Sidebar text | `[data-testid="stSidebar"]` | Moderate — same selector |

### CSS Template

```python
_CHROME_CSS_TEMPLATE = """
<style>
.stApp {{
    background-color: {page_bg} !important;
    color: {page_text} !important;
}}
[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    color: {sidebar_text} !important;
}}
</style>
"""
```

Injected via `st.html()` (zero-height, direct DOM — NOT iframe).

### What We Do NOT Override (kept in primaryColor)

All widget accent colors (buttons, sliders, checkboxes, radio, selectbox focus ring, download button) are handled by Streamlit's native `primaryColor`. This eliminates all 8 risky `data-baseweb` selectors.

---

## 5. Module-by-Module Impact Analysis

### No Changes Needed (5 modules)

| Module | Why |
|---|---|
| `streamtex/space.py` | Pure layout, no colors |
| `streamtex/container.py` | Delegates to Style — already theme-aware |
| `streamtex/write.py` | Delegates to Style — already theme-aware |
| `streamtex/bib.py` | Uses styles from user — already theme-aware |
| `streamtex/link_preview.py` | Uses styles from user — already theme-aware |

### Simple Parameter Addition (8 modules)

| Module | Change Required |
|---|---|
| `styles/core.py` | Add `apply_theme(theme_dict)` function that sets `theme` global + injects chrome CSS |
| `book.py` | Add theme selector widget in sidebar; call `apply_theme()` on change; pass theme to export |
| `export.py` | Replace hardcoded `background: #fff` with theme's `page_bg`; replace `color` with theme's `page_text` |
| `marker.py` | Accept theme-aware colors for slide-break rule (currently hardcoded `#444`) |
| `banner.py` | Background gradient colors should come from theme (currently from style, already OK if styles are theme-aware) |
| `search.py` | Highlight color is hardcoded yellow — make it configurable or accept from theme |
| `toc.py` | Link colors and hover colors — should inherit from `.stApp` color or accept from theme |
| `zoom.py` | Button colors in JS — should respect theme or use neutral colors |

### Significant Changes (4 modules)

| Module | Change | Details |
|---|---|---|
| `code.py` | Pygments style per theme | Currently hardcoded `style="monokai"`. Must read `theme["code_highlight"]` and use appropriate Pygments style. Light themes need light styles (e.g. `"default"`, `"friendly"`). |
| `mermaid.py` | Diagram theme per theme | Mermaid has its own theme system (`dark`, `default`, `forest`). Must map StreamTeX theme to Mermaid theme. Diagrams render in iframes — CSS injection doesn't reach them. |
| `plantuml.py` | Diagram colors | PlantUML uses skin parameters. Must pass appropriate colors based on current theme. |
| `tikz.py` | Background color | TikZ renders to SVG/PNG. Background must match theme. Currently may hardcode white. |

### Collection System (1 module)

| Module | Change |
|---|---|
| `collection.py` | Must propagate theme selection across sub-projects. When a collection loads a sub-project, the theme selector should apply to the sub-project too. |

### Inspector (1 module)

| Module | Change |
|---|---|
| `inspector.py` | The ace editor theme should match the current theme (dark ace theme for dark, light for light). |

### CLI (1 module)

| Module | Change |
|---|---|
| `cli/project_cmd.py` | Template scaffolding must generate the new `themes.py` format with at least dark + light themes. |

---

## 6. New API Surface

### `streamtex/themes.py` (NEW module)

```python
from typing import TypedDict, Optional

class ChromeConfig(TypedDict):
    page_bg: str
    page_text: str
    sidebar_bg: str
    sidebar_text: str

class ThemeConfig(TypedDict):
    chrome: ChromeConfig
    code_highlight: str        # Pygments style name
    styles: dict[str, str]     # style_id -> CSS

def apply_theme(name: str, themes: dict[str, ThemeConfig]) -> None:
    """Apply a named theme: update core.theme dict + inject chrome CSS."""
    ...

def get_current_theme() -> Optional[str]:
    """Return the name of the currently active theme."""
    ...

def theme_selector(themes: dict[str, ThemeConfig], default: str) -> str:
    """Render a sidebar selectbox and return the chosen theme name."""
    ...
```

### `streamtex/styles/core.py` Changes

```python
# Existing (unchanged)
theme = {}   # line 6

# New helper
def set_theme(styles_dict: dict[str, str]) -> None:
    """Replace the global theme dict with the given style overrides."""
    global theme
    theme.clear()
    theme.update(styles_dict)
```

### `book.py` Integration Point

In both `_render_continuous()` and `_render_paginated()`, before rendering blocks:

```python
from .themes import theme_selector, apply_theme

# In sidebar
selected = theme_selector(project_themes, default=project_default_theme)
apply_theme(selected, project_themes)
```

---

## 7. Export Pipeline Changes

### HTML Export

`export.py` `generate_export_html()` must accept a theme parameter:

```python
def generate_export_html(
    blocks_html: list[str],
    title: str,
    theme: Optional[ThemeConfig] = None,  # NEW
    ...
) -> str:
```

When `theme` is provided:
- Use `theme["chrome"]["page_bg"]` instead of `#fff`
- Use `theme["chrome"]["page_text"]` instead of hardcoded text color
- Include theme-specific CSS in the `<style>` block

### PDF Export

`pdf_export.py` already receives the HTML from `generate_export_html()`. No changes needed in the PDF module itself — the HTML it receives will already have the correct theme colors.

### `default.css` Changes

The `@media (prefers-color-scheme: dark)` rules (lines 54-59) for link colors may conflict with theme CSS injection. Options:
1. Remove the media query entirely and control link colors from the theme
2. Keep it as fallback but ensure theme CSS has higher specificity

Recommended: Option 1 — remove and let themes control everything.

---

## 8. Implementation Phases

### Phase 1: Core Infrastructure (no breaking changes)

1. Create `streamtex/themes.py` with `apply_theme()`, `theme_selector()`, `get_current_theme()`
2. Add `set_theme()` helper to `styles/core.py`
3. Add chrome CSS injection function
4. Add `theme` parameter to `generate_export_html()` (backward-compatible — defaults to None which preserves current behavior)
5. Detect Streamlit theme via `st.context.theme.type` (Streamlit 1.54+)

### Phase 2: Module Updates (no breaking changes)

1. `code.py` — read `code_highlight` from active theme, fallback to `"monokai"`
2. `mermaid.py` — map theme to Mermaid theme parameter
3. `plantuml.py` — pass skin parameters based on theme
4. `tikz.py` — set background from theme
5. `book.py` — add theme selector in sidebar, wire `apply_theme()`
6. `export.py` — use theme colors when provided
7. `default.css` — remove `@media (prefers-color-scheme: dark)` for link colors
8. `inspector.py` — match ace editor theme to active theme

### Phase 3: Migration (BREAKING CHANGES)

1. Migrate all 9 `themes.py` files to new format
2. Simplify all 10 `config.toml` files to keep only `primaryColor`
3. Update CLI templates to generate new format
4. Update documentation and cheatsheet
5. Update tests
6. Bump minor version (breaking change in themes.py format)

---

## 9. Risks and Limitations

### Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| `primaryColor` is fixed across all themes | Widget accent color (buttons, sliders, focus rings) same for dark and light | Choose a color that works on both backgrounds (e.g. `#667eea` works well) |
| `data-testid` selectors are semi-stable | May break on major Streamlit updates | Monitor Streamlit changelogs; only 2 selectors used |
| Iframe content is isolated | Mermaid/TikZ/PlantUML diagrams don't receive parent CSS | Handle via Python re-rendering with theme parameters |
| `st.context.theme.type` returns only "dark"/"light" | Cannot detect custom theme names directly | We manage theme state ourselves via `st.session_state` |

### Risks

| Risk | Probability | Mitigation |
|---|---|---|
| Streamlit removes `data-testid` attributes | Low (used by their own tests) | Fallback to class-based selectors |
| Streamlit changes `.stApp` class name | Very Low (documented, stable) | Simple find-replace if it happens |
| Pygments style mismatch with theme | Medium | Validate style/theme combinations in tests |
| Collection sub-project theme conflicts | Medium | Propagate theme via session_state key |

### What This Does NOT Cover

- Per-widget accent color changes (kept uniform via `primaryColor`)
- Animated theme transitions
- User-defined themes at runtime (themes must be defined by the project author in `themes.py`)
- Third-party Streamlit component theming

---

## 10. Testing Plan

### Unit Tests

- `test_themes.py` — `apply_theme()` sets `core.theme`, `set_theme()` clears/replaces, chrome CSS generation
- `test_code.py` — Pygments style selection per theme
- `test_export.py` — Export HTML respects theme colors

### Integration Tests

- Theme switching preserves session state
- Export in dark theme produces dark HTML
- Export in light theme produces light HTML
- Collection propagates theme to sub-projects

### Manual Tests

- Visual check: switch between themes, verify all elements update
- Export PDF in each theme, verify colors match screen
- Check widget accent color stays consistent across themes
- Test with OS dark/light mode toggle

---

## 11. File Checklist

### Library (`streamtex/`)

| File | Action | Phase |
|---|---|---|
| `themes.py` | **CREATE** — theme engine module | 1 |
| `styles/core.py` | ADD `set_theme()` helper | 1 |
| `book.py` | ADD theme selector + `apply_theme()` calls | 2 |
| `export.py` | ADD `theme` param, remove hardcoded `#fff` | 2 |
| `code.py` | READ theme's `code_highlight` | 2 |
| `mermaid.py` | MAP theme to Mermaid theme | 2 |
| `plantuml.py` | PASS skin params from theme | 2 |
| `tikz.py` | SET background from theme | 2 |
| `inspector.py` | MATCH ace editor theme | 2 |
| `static/default.css` | REMOVE `prefers-color-scheme` media query | 2 |
| `collection.py` | PROPAGATE theme across sub-projects | 2 |
| `__init__.py` | EXPORT new public API | 1 |
| `cli/project_cmd.py` | UPDATE template generation | 3 |
| `tests/test_themes.py` | **CREATE** | 1 |

### Docs (`streamtex-docs/`)

| File | Action | Phase |
|---|---|---|
| 9x `custom/themes.py` | MIGRATE to new format | 3 |
| 10x `.streamlit/config.toml` | SIMPLIFY to `primaryColor` only | 3 |
| `references/coding_standards.md` | ADD theme section | 3 |
| `references/streamtex_cheatsheet_en.md` | ADD theme API reference | 3 |
| `CLAUDE.md` | ADD theme-related rules | 3 |
