# Maintenance Plan: Profile Buttons Visible in Sidebar

**Status:** Open
**Priority:** Medium (cosmetic issue, no functional impact on profile switching)
**Created:** 2026-03-20
**Affects:** All deployed manuals (Hetzner/Coolify) + local (intermittent)
**Component:** `streamtex` library — `streamtex/book.py` lines 524-550

---

## Problem Description

Three buttons (`stx_prof_Default`, `stx_prof_Desktop`, `stx_prof_Mobile`) appear visibly in the sidebar, below the Settings expander. They should be hidden — they exist only as DOM relay targets for the floating navigation bar's profile switching mechanism.

### Observed behavior

| Environment | Buttons visible? | After hard refresh (Ctrl+Shift+R)? |
|-------------|-----------------|-------------------------------------|
| Local (dev) | Sometimes | Usually hidden |
| Hetzner (production) | Always | Sometimes hidden |

### Why these buttons exist

The floating navigation bar (marker.py) runs in a `components.html` iframe. JavaScript inside an iframe cannot directly trigger a Streamlit rerun. The workaround:

1. Hidden `st.button()` widgets in the sidebar with `on_click` callbacks
2. Floating bar JS finds these buttons via `parent.document.querySelectorAll()` and calls `.click()`
3. The click triggers the Streamlit callback which sets `session_state["_stx_profile_pending"]`
4. Streamlit reruns and applies the profile

The buttons must remain in the DOM and be clickable (`pointer-events: auto`), but visually hidden.

---

## Current Hiding Mechanism

**File:** `streamtex/streamtex/book.py`, lines 524-550

```python
# 1. CSS class defined via st.html (injected in main document, no layout impact)
st.html(
    '<style>.stx-hidden-btns { position:absolute !important;'
    ' left:-9999px !important; height:0 !important;'
    ' overflow:hidden !important; pointer-events:auto !important; }</style>'
)

# 2. Buttons rendered in a container
_prof_ctr = st.container()
with _prof_ctr:
    for _p in all_profiles:
        st.button(f"stx_prof_{_p.name}", ...)

# 3. JS in components.html iframe adds the CSS class to the buttons
components.html("""<script>
    var btns = parent.document.querySelectorAll('[data-testid="stBaseButton-secondary"]');
    for (var i = 0; i < btns.length; i++) {
        var txt = (btns[i].textContent || '').trim();
        if (txt.indexOf('stx_prof_') === 0) {
            var w = btns[i].closest('[data-testid="stButton"]');
            if (w) w.classList.add('stx-hidden-btns');
        }
    }
</script>""", height=0)
```

### Why it fails

The `components.html` JavaScript executes **once** inside an iframe. It must:
1. Access `parent.document` (cross-iframe)
2. Find buttons that React has already rendered in the DOM

**Race condition:** If the iframe JS executes before React renders the buttons, `querySelectorAll` returns nothing and the buttons stay visible. There is no retry mechanism.

---

## Failed Fix Attempts (2026-03-20)

### Attempt 1: `st.html(unsafe_allow_javascript=True)` + MutationObserver

Replace `components.html` with `st.html()` which runs in the main document (no iframe).

**Result:** Completely broke the sidebar — TOC, markers, search, and floating bar all disappeared. Page became extremely slow.

**Root cause:** `st.html()` with non-style content (script tags) creates a **layout element** in the sidebar. Streamlit reserves vertical space for it, pushing other elements and disrupting the sidebar rendering pipeline.

### Attempt 2: `st.html(unsafe_allow_javascript=True)` + requestAnimationFrame

Same approach but with lighter retry logic instead of MutationObserver.

**Result:** Same layout destruction.

**Root cause:** Same — any `st.html()` call with non-`<style>` content creates a layout element.

### Key learning

In the Streamlit sidebar, the only safe injection methods are:
- `st.html('<style>...</style>')` — goes to "event container", **no layout impact**
- `components.html('...', height=0)` — creates an iframe with zero height, **no layout impact**
- `st.markdown('...', unsafe_allow_html=True)` — native widget, **predictable layout**
- `st.caption()` — native widget, **predictable layout**

`st.html()` with `unsafe_allow_javascript=True` is **unsafe in the sidebar** for anything containing `<script>` or non-style HTML.

---

## Diagnostic Procedure

### Phase 1: Remote diagnosis on Hetzner (5-10 minutes)

Open `https://docs.streamtex.org` in Chrome. Open DevTools (F12).

#### 1.1 Check if the iframe exists

In the Console, run:
```javascript
document.querySelectorAll('iframe').length
```
Expected: several iframes (one per `components.html` call). If 0, the iframe mechanism is completely broken.

#### 1.2 Check if buttons are in the DOM

```javascript
document.querySelectorAll('[data-testid="stBaseButton-secondary"]').forEach(btn => {
    console.log(btn.textContent.trim(), btn.closest('[data-testid="stButton"]')?.classList.toString())
})
```
Expected output:
```
stx_prof_Default stx-hidden-btns
stx_prof_Desktop stx-hidden-btns
stx_prof_Mobile stx-hidden-btns
```

If the class `stx-hidden-btns` is missing, the JS never ran or didn't find the buttons.

#### 1.3 Check if the CSS class is defined

```javascript
document.querySelectorAll('style').forEach(s => {
    if (s.textContent.includes('stx-hidden-btns')) console.log('CSS found:', s.textContent.substring(0, 200))
})
```
If nothing prints, the `st.html('<style>...</style>')` is not being injected.

#### 1.4 Check cross-iframe access

Find the hiding iframe and test `parent.document` access:
```javascript
// In the Console, select an iframe manually via Elements panel,
// then in its console context:
parent.document.querySelectorAll('[data-testid="stBaseButton-secondary"]').length
```
If this throws a security error, CSP headers are blocking cross-iframe access.

#### 1.5 Check CSP headers

In the Network tab, look at the response headers for the main page:
- `Content-Security-Policy`
- `X-Frame-Options`

If `frame-ancestors 'none'` or restrictive CSP is set (by Coolify/Caddy reverse proxy), it may block iframe → parent access.

### Phase 2: Determine root cause

Based on Phase 1 results:

| Finding | Root cause | Fix direction |
|---------|-----------|---------------|
| CSS missing | `st.html` style injection broken | Check Streamlit version on Hetzner |
| CSS present, class not on buttons | JS ran but buttons not in DOM yet | Add retry mechanism |
| JS security error | CSP blocks iframe→parent | Configure Coolify/Caddy headers |
| `data-testid` different | Streamlit version mismatch | Update selector |
| Buttons not in DOM at all | Rendering failure | Investigate Streamlit rendering |

### Phase 3: Implement fix based on root cause

#### If timing issue (most likely):

**Option A — Retry with `setInterval` in `components.html`**

Replace the one-shot JS with a polling retry:

```javascript
(function(){
    var attempts = 0;
    var timer = setInterval(function(){
        var found = 0;
        parent.document.querySelectorAll('[data-testid="stBaseButton-secondary"]')
            .forEach(function(btn) {
                if ((btn.textContent || '').trim().indexOf('stx_prof_') === 0) {
                    var w = btn.closest('[data-testid="stButton"]');
                    if (w) { w.classList.add('stx-hidden-btns'); found++; }
                }
            });
        if (found >= 3 || ++attempts > 100) clearInterval(timer);
    }, 50);
})();
```

This stays inside `components.html(height=0)` — no layout impact. Retries every 50ms for up to 5 seconds.

**Risk:** Low — same iframe mechanism, just adds retry. The `height=0` ensures no layout disruption.

**Option B — CSS-only approach (no JS at all)**

If the `data-testid` and DOM structure are stable, hide buttons purely with CSS by targeting their container position in the sidebar. This would go in the existing `st.html('<style>...')` call.

**Risk:** Medium — CSS structural selectors break if Streamlit changes its DOM.

#### If CSP issue:

Configure the Coolify service or Caddy reverse proxy to allow `frame-ancestors 'self'` or equivalent.

#### If `data-testid` mismatch:

Update the selector in both `book.py` (hiding) and `marker.py` (clicking) to match the actual attribute.

---

## Files Involved

| File | Role |
|------|------|
| `streamtex/streamtex/book.py:524-550` | CSS + buttons + hiding JS |
| `streamtex/streamtex/marker.py:461-473` | Floating bar profile click (uses same selector) |
| `streamtex/streamtex/presentation_profile.py` | Profile data model |
| `streamtex-docs/.github/workflows/hetzner-deploy.yml` | Deploy workflow |

## Constraints

Any fix MUST:
- Keep buttons in the DOM and clickable via JS (`.click()` must fire)
- NOT use `display:none` (blocks click events in some browsers)
- NOT use `st.html(unsafe_allow_javascript=True)` in the sidebar (breaks layout)
- NOT modify `marker.py` profile switching mechanism
- Work in both paginated and continuous modes
- Work on all 6 manuals
