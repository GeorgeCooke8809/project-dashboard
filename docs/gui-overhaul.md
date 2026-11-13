# GUI Overhaul

Polish the look of every page, make the site mobile responsive, store project descriptions as Markdown (with an
Obsidian-style editor and colour-coded code blocks).

**Mockup:** https://claude.ai/artifact/HD2zzRQdj5PKfet7WtfRP9. This is the agreed design. Where this doc and the mockup
disagree, this doc wins. In particular, the mockup's GitHub link and "GitHub repo" field are **not** part of this
work (see section 5). The mockup uses inline styles because of how the design tool works; the real site keeps all
styling in `frontend/static/css/style.css`.

**How the code is written:** every agent must use the `code-like-george` skill (George's style, only syntax he
knows, small commits as Claude, a PR into `development`). Local files beat the skill's guide, e.g. tests here are named
`tests/<function>_test.py` with a `Test<Function>` class, not `test_<function>.py`.


## Goals

- Keep it simple to change later: colours and fonts are variables in one place, a handful of shared classes, one phone
  breakpoint at **700px**, no CSS framework, no JS framework.
- Keep the existing class names, IDs and JS function names where they still make sense, so `common.js` keeps working.
- Fix the TODOs this covers: details page mobile responsive, line breaks not rendering.


## 1. Look and feel (foundation)

### 1.1 Fonts

The CSS already names Cormorant Garamond and Jost but never loads them. Add to `base.html` `<head>`, before `style.css`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Jost:wght@400;500;600&display=swap">
```

- Headings, project names, the site name: Cormorant Garamond 600.
- Everything else: Jost 400/500.
- Code: `Consolas, 'Courier New', monospace`.

### 1.2 Colour variables

Replace the current `:root` block with this one. **No colour value appears anywhere else in the CSS.** Names describe
what the colour is for, so they document themselves.

| Variable | Value | Used for |
|---|---|---|
| `--page-background-colour` | `#141312` | Page background |
| `--card-background-colour` | `#1C1B19` | Cards, panels, nav bar |
| `--card-hover-background-colour` | `#22211F` | Card / row hover |
| `--input-background-colour` | `#252421` | Inputs, textarea, table headers, inline code |
| `--border-colour` | `#312F2B` | Card borders, dividers |
| `--strong-border-colour` | `#47443F` | Input and button borders, table cells |
| `--heading-text-colour` | `#F3EDE0` | Headings, main text |
| `--body-text-colour` | `#DAD3C5` | Long-form text (About section) |
| `--label-text-colour` | `#BCB4A5` | Form labels |
| `--muted-text-colour` | `#9C958A` | URLs, dates labels, secondary text |
| `--accent-colour` | `#CDA349` | Gold: nav rule, links, primary buttons, focus outline, list bullets |
| `--accent-hover-colour` | `#B48D36` | Primary button hover |
| `--text-on-accent-colour` | `#141312` | Text on gold buttons |
| `--error-colour` | `#D9675F` | Flash message border and icon |
| `--error-background-colour` | `#38201E` | Flash message background |
| `--scrollbar-colour` | `#47443F` | Code block scrollbar thumb |
| `--scrollbar-hover-colour` | `#5E5A54` | Code block scrollbar thumb hover |
| `--code-background-colour` | `#202020` | Code blocks (neutral grey, a touch lighter than cards) |
| `--code-text-colour` | `#DAD3C5` | Plain code text |
| `--code-keyword-colour` | `#D8B358` | `def`, `if`, `return`, `SELECT`... |
| `--code-string-colour` | `#AAC48C` | Strings |
| `--code-comment-colour` | `#948E86` | Comments (italic) |
| `--code-number-colour` | `#E39C74` | Numbers, C++ `#include` |
| `--code-function-colour` | `#8EB0D6` | Function names, HTML/CSS attributes, PowerShell parameters |
| `--code-type-colour` | `#C4A2D6` | Built-ins, types, decorators, exceptions |
| `--code-variable-colour` | `#86C2B2` | Variables (`$name`), class names, CSS selectors |
| `--code-tag-colour` | `#DE8A80` | HTML tags |

Plus `--heading-font`, `--body-font`, `--code-font` and `--card-border-radius: 8px`, `--control-border-radius: 6px`.
All text/background pairs above pass WCAG AA (4.5:1). Check again if a colour is changed.

### 1.3 Shared pieces

- **Page width:** content sits in a centred container, `max-width: 1100px`, `24px` side padding (`16px` on phones).
  Replace the current `body { width: 80vw }`.
- **Nav bar (`base.html`):** full-width bar, card background, 1px gold bottom border, not absolutely positioned
  (`position: sticky; top: 0` instead). Its contents span the **full width of the bar** with `32px` side padding
  (`16px` on phones), not the 1100px page container, so the name sits at the far left and the buttons at the far
  right. Left: "George Cooke" in Cormorant 28px (24px on phones) linking to `/`.
  Right: `Admin`, and `Log Out` when `"admin" in session`. Remove the nested `<nav><nav>` and the `<div>` inside `<ul>`
  (invalid HTML).
- **Buttons:** `.basic-button` = outlined (strong border, card background, 44px min height, 6px radius, Jost 500 15px).
  `.cta-button` = gold background, dark text, Jost 600 17px (down from 40px), same height and radius. Hover states from
  the variables.
- **Cards:** `.card` = card background, 1px border, 8px radius. Clickable cards get a gold border on hover.
- **Form fields:** `.field` = a `<label>` above its input, 6px gap. Inputs: input background, strong border, 6px radius,
  44px min height, Jost 16px, 2px gold focus outline. Every input has a real `<label for>` (the current `<h4>` labels go).
- **Date inputs:** same font and size as the other inputs, `font-variant-numeric: tabular-nums`, `color-scheme: dark`,
  picker icon lightened (`filter: invert(.75)`). Stack Created and Updated one above the other (side by side they were
  cramped). Replace the current `::-webkit-calendar-picker-indicator` rule.
- **Flash messages (`.flash-message`):** move `#flash-container` to the top right, below the nav
  (`top: 84px; right: 24px`), `width: min(360px, 100% - 32px)`. Each message: error background, 1px error border, 8px
  radius, a circled "!" SVG icon in the error colour, then the text. No thick left border. `role="status"` on the
  container so screen readers announce it.
- **Touch targets:** anything clickable is at least 44px high (32px is fine for the small code-copy button).

### 1.4 Phone layout (`@media (max-width: 700px)`)

One media query block at the end of the main CSS. Two-column layouts (details, add/edit form) stack, side padding drops
to 16px, headings shrink (h1 56px → 44px), nav buttons get less padding. Nothing should scroll sideways except code
blocks.

### 1.5 Classical touches (easy to revert)

All three live in one block at the **bottom** of `style.css`, every rule prefixed `.classical`, switched on by
`<body class="classical">` in `base.html`. Deleting that class (or the block) reverts them; nothing else may depend on it.

```css
/* * Classical touches - remove class="classical" from <body> in base.html to turn these off */
.classical #navigation-bar {
    border-bottom: 3px double var(--accent-colour);
}

.classical .field label, .classical .meta-label, .classical .code-header span {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
}

.classical .markdown blockquote {
    font-family: var(--heading-font);
    font-style: italic;
    font-size: 20px;
    line-height: 1.5;
}
```

Dates are **not** restyled (old-style numbers were tried and were hard to read).


## 2. Pages

### 2.1 Home (`index.html`)

- Header row: "Projects" h1 (Cormorant 56px) on the left, "N active projects" in muted text on the right
  (`{{ projects | length }}`), thin border underneath. Remove the `<hr>`.
- Cards in a grid: `grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px`. One column on phones.
- Card: project name (Cormorant 28px, links to `details/<id>`), URL underneath in muted 14px with a small ↗ SVG
  (links to the site, `target="_blank" rel="noopener"`), and a gold "View details →" link at the bottom.
- Empty state: keep "No active projects", styled as muted text.

### 2.2 Details (`details.html`)

- "← All projects" muted link above.
- Two columns (`display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start`):
  - **Left column** (`#details-info-panel`, card, `flex: 1 1 260px; max-width: 320px`): name (Cormorant 40px), then
    links, then a divider, then a two-column grid of dates: `Created` / `Last updated` labels (class `meta-label`, muted)
    and values (normal text). `Last updated` only shows if there is one.
    - Website link: gold, globe SVG icon, only if `url` is set. Put it in its own small links block
      (`<div class="details-links">`, column, 2px gap) so more links can be added later.
  - **Right column** (`#details-description`, card, `flex: 999 1 420px; min-width: 0`): the description rendered from
    Markdown (section 3) inside `<div class="markdown">`. No "About" heading; the Markdown provides its own.
- **Sticky left column:** on desktop the left column stays in place while the page scrolls (`position: sticky; top: 88px`),
  **but only when it is shorter than the window**. CSS can't check that, so `details.js` adds the class
  `sticky-panel` when `panel.offsetHeight + 88 < window.innerHeight`, and checks again on `resize`. No sticking on phones.
- **Code blocks:** see 3.3. Each one gets a copy button (icon, not text).
- Remove the fixed `height: calc(100vh - 95px)` panels.

### 2.3 Add / edit project (`add-project.html`, `edit-project.html`)

- Page heading "New Project" / "Edit Project" (Cormorant 48px) with "← Admin dashboard" link above.
- Two columns like the details page:
  - **Left card:** Name, URL, Created, Updated (stacked),
    "Add another project" checkbox (add page only, real `<label>` around it, gold `accent-color`), then the gold
    submit button at the bottom.
  - **Right card:** the Markdown editor (section 4).
- The two pages share almost all their markup. Keep them as two templates (George's current pattern) unless it's
  trivial to share with an `{% include %}`.

### 2.4 Admin dashboard, inactive projects, login, 404

- **Admin:** heading row with "Admin Dashboard" h1 + "Active projects" muted subtitle on the left and a gold
  "+ New Project" button on the right. Projects in one card as rows (`.project-row`): name (17px, 500) with the URL
  underneath in muted 13px, then `Edit` and `Archive` outlined buttons. Rows have a bottom border and hover background,
  wrap on phones. "View inactive projects →" muted link bottom right.
- **Inactive projects:** same row style, `Restore` button.
- **Login:** centred card, `max-width: 360px`, "Sign In" h1 (Cormorant 44px), two `.field`s, full-width gold button.
- **404:** centred h1 and a "← Back to projects" link, same page container.


## 3. Markdown descriptions

The description column already stores text, so **no data migration is needed**: existing plain-text descriptions are
valid Markdown (single line breaks are kept, see below).

### 3.1 Rendering (server side)

**Done by George** (commit `dfa4224`), apart from the language label that Agent 4 adds below. `markdown` and
`pygments` are in `pyproject.toml`, and `projects/utils.py` has `render_markdown(text)`:

- Extensions: `fenced_code`, `tables`, `codehilite` (with `css_class = "highlight"`, `guess_lang = False`), `nl2br`
  (so single line breaks show, which is how George writes descriptions now), `sane_lists`.
- `None` or `""` returns `""`.
- Raw HTML in the Markdown is passed through, not escaped (only the admin writes descriptions).
- **Agent 4 adds:** code blocks say which language they are, so the page can label them. A small formatter class in
  `projects/utils.py` (tested on 13.11.2026, gives exactly the output below):

  ```python
  class LabelledFormatter(HtmlFormatter):
      """Pygments formatter that keeps the code block's language in a data-language attribute"""

      def __init__(self, lang_str: str = "", **options):
          super().__init__(**options)
          self.lang_str = lang_str

      def wrap(self, source):
          yield 0, f'<pre><code data-language="{self.lang_str}">'

          for line in source:
              yield line

          yield 0, "</code></pre>"
  ```

  with `from pygments.formatters import HtmlFormatter` at the top, and `"pygments_formatter": LabelledFormatter,
  "lang_prefix": ""` added to the `codehilite` settings in `render_markdown`. Output:
  `<div class="highlight"><pre><code data-language="python"><span class="k">def</span>...</code></pre></div>`.
  The language is exactly what was written after the ` ``` ` (`python`, `ps1`, `c++`...); a block with no language
  gets `data-language="text"`. Python-Markdown passes `lang_str` to the formatter itself. `wrap` must add the `<pre>`,
  or the code loses its spacing.
- `get_project_details` returns `"description_html": render_markdown(project.description)`.
- The details template uses `{{ details["description_html"] | safe }}`.

### 3.2 Markdown styles (`.markdown`)

Headings h1–h3 in Cormorant (h2 30px), paragraphs and lists with 14px bottom margin, gold list bullets
(`li::marker`), links gold and underlined, `strong` in heading colour, inline `code` on input background with a 1px
border, blockquotes with a 3px gold left border and muted text, `hr` as a 1px border line.
**Tables are full width** (`width: 100%; border-collapse: collapse`), cells with strong borders, header row on input
background. On phones the table may scroll sideways inside its own box instead of stretching the page.

### 3.3 Code blocks

- Pygments outputs `<div class="highlight"><pre>...</pre></div>` with short token classes. Colour them in `style.css`
  using the `--code-...` variables. At least these classes:
  - keyword: `.k .kc .kd .kn .kr .kp .ow`
  - type / built-in: `.kt .nb .bp .ne .nd`
  - string: `.s .s1 .s2 .sb .sd .se .si .sh .sx`
  - comment: `.c .c1 .cm .cs .ch` (italic) · preprocessor: `.cp .cpf` (number colour)
  - number: `.m .mi .mf .mh .mo`
  - function / attribute: `.nf .fm .na`
  - variable / class / selector: `.nv .vi .vg .nc .nn`
  - HTML tag: `.nt`
  Check it against Python, PowerShell, JavaScript, HTML, CSS, C++, SQL and Bash (the mockup's "Code block colours by
  language" screen shows the expected result).
- Fences without a language are plain text in `--code-text-colour`.
- Each block gets a header bar (class `code-header`): the language name on the left (`<span>`, muted 13px; small
  capitals with the classical block), the copy button on the right. `details.js` adds it to each `.highlight`.
  - The language comes from `data-language` on the block's `<code>` (section 3.1). Turn it into a display name with
    a plain object, e.g. `python` → Python, `ps1` / `powershell` / `pwsh` → PowerShell, `js` / `javascript` →
    JavaScript, `html` → HTML, `css` → CSS, `cpp` / `c++` → C++, `cs` / `csharp` / `c#` → C#, `sql` → SQL,
    `bash` / `sh` / `shell` → Bash, `json` → JSON, `yaml` / `yml` → YAML. Anything else is shown as written.
  - `text` (no language given) shows no name, just the copy button.
  - Until Agent 4 is merged there is no `data-language`; the header must still work then, showing no name.
- **Copy button:** 32×32, an SVG "two overlapping rectangles" icon (no text), `aria-label="Copy code"` and
  `title="Copy code"`. On click: `navigator.clipboard.writeText(...)`, swap to a tick icon for 1.5s.
- **Scrollbars:** long lines scroll sideways inside the block. Make the scrollbar blend in:
  `scrollbar-width: thin; scrollbar-color: var(--scrollbar-colour) transparent;` plus `::-webkit-scrollbar`
  rules (8px high, transparent track, rounded thumb, hover colour).
- Block: code background, 1px border, 6px radius, 14px/1.6 code font, 14px 16px padding.


## 4. Markdown editor

Replaces the description `<textarea class="description-area-entry">`. Lives in a new `frontend/static/js/editor.js`,
loaded only by `add-project.html` and `edit-project.html` (via `{% block scripts %}`). It must work on a plain
`<textarea id="description">` so `addProject()` / `editProject()` just read `.value`.

### 4.1 Tabs

"Write" and "Preview" tabs above the editor (active tab: heading colour with a 2px gold underline; inactive: muted).
Right of the tabs, muted 13px hint: "Markdown · right-click to insert" ("long-press" on touch screens).

- **Write:** the textarea, monospace 15px/1.65, at least 440px high (170px on phones), resizable vertically.
- **Preview:** `POST /api/render-markdown` with `{"text": ...}`, put the returned `html` in a `.markdown` div. Same
  styles and code blocks as the details page, so preview = real page. Hide the textarea with a class (don't remove it,
  it would lose the cursor/undo history).

### 4.2 Auto-complete (like Obsidian)

Handled in a `keydown` listener on the textarea:

| You type | Result (`|` = cursor) |
|---|---|
| `*` `_` `` ` `` `"` `(` `[` | Inserts the pair: `*|*`, `(|)` |
| The same `*` again inside an empty pair | `**|**` |
| A closing character that is already next | Moves past it instead of adding another |
| Any of the above with text selected | Wraps the selection: `*text*` |
| Backspace between an empty pair | Deletes both halves |
| Enter on a `- `, `* `, `1. `, `- [ ] ` or `> ` line | Continues it on the next line (numbers count up, checkboxes reset to `[ ]`) |
| Enter on an empty list item | Removes the marker and ends the list |
| Ctrl+B / Ctrl+I | Wraps the selection in `**` / `*` (or inserts `**bold text**` with it selected) |

Use `setRangeText` and `selectionStart` / `selectionEnd` so Ctrl+Z still works. Working reference: the mockup's form
screen (press Play), `Component.handleKey`.

### 4.3 Right-click menu

`contextmenu` on the textarea opens a small menu at the mouse (card background, strong border, 8px radius, shadow,
240px wide), closed by clicking elsewhere, Escape or picking an item. Items (with a muted hint on the right):

Bold `Ctrl+B` · Italic `Ctrl+I` · Inline code · Link · *divider* · Heading `##` · Bullet list · Numbered list ·
Checklist · Quote · *divider* · Table · Code block · Horizontal line

- Inline items wrap the selection, or insert a placeholder and select it (`[link text](https://)`).
- Line items add their marker at the start of the current line.
- Table inserts a 2×2 table with the first cell selected:
  ```
  | Column 1 | Column 2 |
  | --- | --- |
  | Cell |  |
  ```
- Use real `<button>`s with `role="menuitem"`; arrow keys move between items.
- On touch screens the menu opens on long-press (that fires `contextmenu` too). Keep it inside the screen.


## 5. Left out for now: GitHub links

The mockup shows a GitHub link on the details page and a "GitHub repo" field on the form. **Don't build either.** No
model, migration, API or form changes for it; the model's `# TODO: Add GitHub link` stays. The details page's links
block (section 2.2) is the place it will go later.


## 6. Backend contract (built by George)

George wrote the backend himself (section 3.1 plus the `/api/render-markdown` route) and it is on `development`.
Agents 1–3 don't edit `projects/`, `migrations/`, `frontend/routes/`, `pyproject.toml` or `uv.lock`. Agent 4 edits
`tests/` plus three small parts of `projects/utils.py`: the section 7 fix, `LabelledFormatter` and the `codehilite`
settings (section 3.1).

- `utils.get_project_details(id)` returns `"description"` (the raw Markdown, used by the edit page's textarea) **and**
  `"description_html"` (`str`, HTML; `""` if there's no description).
- `POST /api/render-markdown`, body `{"text": "<markdown>"}` → `{"code": 200, "message": "", "html": "<html>"}`.
- `/api/add-project` and `/api/edit-project` don't change.
- Code blocks: `<div class="highlight"><pre><code data-language="<lang>">` + Pygments token spans, as in section 3.1
  (the `data-language` part arrives with Agent 4).

If George changes any of this, he updates this section and tells the agents that are running.


## 7. Known bugs

- `addProject()` clears `#description-area` when "Add another project" is ticked, but no element has that ID. Agent 3
  fixes it when it renames the textarea to `#description`.
- **Agent 4 fixes:** commit `dfa4224` replaced `"description"` with `"description_html"` in `get_project_details`
  instead of adding it alongside. The edit page fills its textarea from `details['description']`, so editing a
  project would show an empty description (and saving would wipe it), and `test_details_description` /
  `test_details_no_description` fail with `KeyError: 'description'` (2 failed, 21 passed on 13.11.2026). Fix: put
  `"description": project.description,` back in the dict, just above `"description_html"`, and add `description` and
  `description_html` to the docstring's *Returns* line. The existing tests then pass unchanged; don't edit them.


## 8. Tests for the backend

George only unit tests his backend functions (`projects/`), so this is the only test work. Match the existing files in
`tests/` exactly (look at `project_details_test.py` and `template.py`): one file per function named
`<function>_test.py`, one `Test<Function>` class, plain `assert`s, the `session` fixture from `conftest.py` is
automatic. Run with `uv run python -m pytest -vv` (plain `uv run pytest` can't import `projects`).

### 8.1 `tests/render_markdown_test.py` (new), class `TestRenderMarkdown`

Test what the function does now; don't add behaviour. Check for the important part of the output (`in`), not whole
HTML strings, so a library update doesn't break every test.

| Test | Input | Check |
|---|---|---|
| `test_render_empty_string` | `""` | returns `""` |
| `test_render_none` | `None` | returns `""` |
| `test_render_plain_text` | `"Hello"` | `"<p>Hello</p>"` |
| `test_render_line_break` | `"Line 1\nLine 2"` | contains `<br />` (nl2br: single line breaks show) |
| `test_render_heading` | `"## Overview"` | contains `<h2>Overview</h2>` |
| `test_render_bold_and_italic` | `"**bold** and *italic*"` | contains `<strong>bold</strong>` and `<em>italic</em>` |
| `test_render_bullet_list` | `"- One\n- Two"` | contains `<ul>` and `<li>One</li>` |
| `test_render_numbered_list` | `"1. One\n2. Two"` | contains `<ol>` and `<li>Two</li>` |
| `test_render_link` | `"[GitHub](https://github.com)"` | contains `<a href="https://github.com">GitHub</a>` |
| `test_render_inline_code` | ``"`x = 1`"`` | contains `<code>x = 1</code>` |
| `test_render_table` | a 2×2 Markdown table | contains `<table>`, `<th>` with the header text, `<td>` with a cell |
| `test_render_code_block_python` | a fenced ` ```python ` block with `def test():` | contains `class="highlight"` and `<span class="k">def</span>` |
| `test_render_code_block_other_language` | a fenced ` ```powershell ` block with `Write-Host "Hi"` | contains `class="highlight"` and `<span class="nb">Write-Host</span>` |
| `test_render_code_block_no_language` | a fenced block with no language | contains `class="highlight"` and no `<span class="k">` (`guess_lang` is off) |
| `test_render_code_block_language_label` | a fenced ` ```python ` block | contains `<pre><code data-language="python">` |
| `test_render_code_block_other_language_label` | a fenced ` ```ps1 ` block | contains `data-language="ps1"` |
| `test_render_code_block_no_language_label` | a fenced block with no language | contains `data-language="text"` |
| `test_render_code_block_keeps_pre` | any fenced block | contains `<pre>` exactly once |
| `test_render_html_passed_through` | `"<b>Hi</b>"` | contains `<b>Hi</b>` (raw HTML isn't escaped, by choice) |

These checks were run against the real output on 13.11.2026 and all hold (Python `def` is `<span class="k">def</span>`,
line breaks are `<br />`, tables have `<thead>`/`<th>`).

### 8.2 `tests/project_details_test.py` (add to the existing class)

| Test | Setup | Check |
|---|---|---|
| `test_details_description_html` | `add_project("Project 1", "URL 1", "**Bold**")` | `details["description_html"]` contains `<strong>Bold</strong>` |
| `test_details_no_description_html` | `add_project("Project 1", "URL 1")` | `details["description_html"] == ""` |

Leave the existing tests as they are. `test_details_description` / `test_details_no_description` fail until the
section 7 fix is in; make that fix first (its own commit), then they pass.

No tests for the `/api/render-markdown` route (George doesn't test Flask routes).


## Agents

If you weren't told which agent you are, ask George with a multiple-choice question (AskUserQuestion), one option per
agent, before doing anything.

**Every agent uses the `code-like-george` skill** for all of its work: load it first, follow its workflow (syntax
database, branch with `claude_git.py start`, George's style and UK spelling, `check_changes.py`, small commits with
`claude_git.py commit`, PR with `claude_git.py pr`), and end with its final-message format (new syntax and reminders).
Agents 1–3 are front-end only, which the skill doesn't unit test; Agent 4 makes the backend fix and writes the tests.

### Agent 1: Foundation styles

- **What it builds:** sections 1.1–1.5 and 2.1, 2.4: fonts, the new `:root` variables, shared classes (buttons, cards,
  fields, dates, container), nav bar, flash messages, the 700px media query, the classical block, and the home,
  admin, inactive projects, login and 404 pages. Leaves clearly marked empty sections in `style.css` for the others.
- **Files:** owns `frontend/templates/base.html`, `index.html`, `admin-dashboard.html`, `inactive-projects.html`,
  `login.html`, `404.html`, `frontend/static/css/style.css` (all of it in this round). May change `flashMessage()` in
  `common.js` only if the new markup needs it.
- **Rounds:** round 1, alongside Agent 4 (no shared files).
- **Overlaps:** provides the variables and shared classes everyone else uses, and these headed sections at the end of
  `style.css`, before the media query and the classical block, for the other agents to fill:
  `/* * Details page */`, `/* * Markdown */`, `/* * Code blocks */`, `/* * Project form */`, `/* * Markdown editor */`.
  Removes the old details/form rules (`#details-info-panel`, `#details-entry-panel`, `.description-area-entry`,
  `#create-project-form h4`, ...) so the later agents start clean; the details and form pages may look unstyled until
  round 2 merges.

### Agent 2: Details page + code blocks

- **What it builds:** sections 2.2, 3.2 and 3.3: the details template (columns, website link with icon, dates,
  rendered Markdown), Markdown and code block styles including every Pygments token class, copy buttons,
  scrollbars, the sticky left column.
- **Files:** owns `frontend/templates/details.html` and new `frontend/static/js/details.js`. Adds only inside the
  `/* * Details page */`, `/* * Markdown */` and `/* * Code blocks */` sections of `style.css`, and details-page rules
  inside the 700px media query (in its own comment-marked lines).
- **Rounds:** round 2 (after Agents 1 and 4 are merged).
- **Overlaps:** uses `description_html` from George's backend (section 6) and `data-language` from Agent 4 (merged
  before round 2 starts). The `.markdown` and code block styles it writes are also used by Agent 3's preview tab, so
  it owns them and Agent 3 doesn't restyle them. The code-block wrapping (header + copy button) is a function in `details.js` that Agent 3 also calls after loading a
  preview: name it `decorateCodeBlocks(container)`; `add-project.html` / `edit-project.html` load `details.js` too.

### Agent 3: Project form + Markdown editor

- **What it builds:** sections 2.3 and 4: add/edit templates, the editor (tabs, auto-complete, right-click menu,
  preview), pointing `addProject()` / `editProject()` at the renamed `#description` textarea, and the bug in section 7.
- **Files:** owns `frontend/templates/add-project.html`, `edit-project.html`, new `frontend/static/js/editor.js`, and
  `addProject()` / `editProject()` in `common.js`. Adds only inside the `/* * Project form */` and
  `/* * Markdown editor */` sections of `style.css`, and form rules inside the 700px media query (in its own
  comment-marked lines).
- **Rounds:** round 2 (after Agents 1 and 4 are merged).
- **Overlaps:** calls `/api/render-markdown` (George's, already on `development`) and `decorateCodeBlocks()`
  (Agent 2). Until Agent 2 is merged, stub `decorateCodeBlocks()` locally; don't commit the stub. If it needs a change
  to `.markdown` styles, it asks in its PR rather than editing Agent 2's sections.

### Agent 4: Backend fix + tests

- **What it builds:** the `get_project_details` fix in section 7, the code block language label in section 3.1
  (`LabelledFormatter`), then section 8: `tests/render_markdown_test.py` and the two new `description_html` tests in
  `tests/project_details_test.py`. Commits in this order:
  `Fixed bug where get_project_details no longer returned the description`,
  `Added language to code blocks in render_markdown`, `Tested render_markdown`,
  `Tested description_html in get_project_details`.
- **Files:** in `projects/utils.py` owns only: the section 7 fix in `get_project_details` (one dict line and its
  docstring), the new `LabelledFormatter` class and its import, and the `codehilite` settings in `render_markdown`.
  Nothing else in the file. Also owns `tests/render_markdown_test.py` (new), and may only add to the
  `TestProjectDetails` class in `tests/project_details_test.py`.
- **Rounds:** round 1, alongside Agent 1 (no shared files).
- **Overlaps:** Agent 3's edit page needs `details['description']`, and Agent 2's code block headers need
  `data-language`, so Agent 4 must be merged before Agents 2 and 3. If a test shows any other bug in George's code,
  it reports it in the PR's *Things to check* instead of fixing it. The `wrap` method and `**options` /
  `super().__init__` may be new syntax for George; follow the skill's rule for explaining them.

### Shared rules

- Each agent works in its own git worktree and branch: `git worktree add ../project-dashboard-agent<N> development`,
  then in that folder `python ~/.claude/skills/code-like-george/scripts/claude_git.py start gui-<short-name>`
  (`gui-foundation`, `gui-details`, `gui-editor`, `gui-tests`).
- Each agent has its own dev-server port and scratch data: a `config.env` in its worktree with
  `NETWORK_PORT=500<N>` and `DATABASE_URL=sqlite:///instance/agent<N>.db`. Never use George's real database.
- Generated files such as test snapshots or `uv.lock` are re-made after a merge, not resolved by hand.
- No agent merges, releases, pushes to `development`/`main`, or edits `CLAUDE.md`. Each opens its PR into
  `development` through `claude_git.py pr` and stops.
- Run `check_changes.py` and `uv run python -m pytest -vv` before every commit. George's tests must still pass, apart
  from the two in section 7 on branches that don't have Agent 4's fix yet (say so, don't fix them yourself). Front-end
  agents check each page in a browser at desktop width and at 390px wide.
- **Merge order for George:**
  1. Round 1: Agents 1 and 4 run together. Merge both, in either order.
  2. Round 2 (only once Agents 1 **and** 4 are merged): Agents 2 and 3 run together. Merge Agent 2, then Agent 3.

  Agents 2 and 3 only add to their own `style.css` sections, so those merges should be clean; if they aren't, the
  later branch merges `development` in and fixes it. That's four PRs in total, one per agent.
