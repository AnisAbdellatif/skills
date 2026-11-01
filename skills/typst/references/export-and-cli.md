# Export formats, accessibility, and the CLI

## CLI

```
typst compile|c  INPUT [OUTPUT]   one-shot build (INPUT `-` = stdin; OUTPUT `-` = stdout)
typst watch|w    INPUT [OUTPUT]   rebuild on change (HTML/bundle: serves with live reload on :3000-3005)
typst eval       EXPR [--in FILE] evaluate code (optionally in the context of a document) → JSON/YAML
typst init       TEMPLATE [DIR]   scaffold from a template, e.g. @preview/charged-ieee[:ver]
typst fonts      [--variants]     list fonts (0.15: shows file paths and variation axes)
typst info                         debug info about paths, caches and environment
typst completions SHELL            shell completions
```

(`typst query` was removed in 0.15 → `typst eval --in doc.typ 'query(<label>)'`; `typst update` self-update exists only in release binaries.)

Common options (compile/watch):

| Flag | Meaning |
| --- | --- |
| `-f, --format pdf\|png\|svg\|html\|bundle` | default inferred from output extension (PDF if none) |
| `--root DIR` (`TYPST_ROOT`) | project root for `/absolute` paths; every read file must live inside it |
| `--input key=value` | string for `sys.inputs` (repeatable) |
| `--font-path DIR` (`TYPST_FONT_PATHS`) | extra font directories (recursive); `--ignore-system-fonts`, `--ignore-embedded-fonts` |
| `--package-path DIR`, `--package-cache-path DIR` | local `@local` packages / download cache |
| `--creation-timestamp N` (`SOURCE_DATE_EPOCH`) | fix the document date (reproducible builds) |
| `--pages 1,3-5,8-` | export only these (physical, 1-based) pages |
| `--ppi N` | PNG resolution (default 144) |
| `--pdf-standard LIST` | `1.4 1.5 1.6 1.7 2.0 a-1b a-1a a-2b a-2u a-2a a-3b a-3u a-3a a-4 a-4f a-4e ua-1`, comma-separated, e.g. `a-2a,ua-1` |
| `--no-pdf-tags` | disable tagged PDF (smaller, but not accessible) |
| `--pretty` | human-readable PDF/SVG/HTML (0.15 minifies by default) |
| `--features html,bundle,a11y-extras` (`TYPST_FEATURES`) | enable in-development features |
| `--deps PATH --deps-format json\|zero\|make` | dependency list (json includes outputs in 0.15) |
| `--diagnostic-format human\|short` | `short` = `file:line:col: message` (editor integration) |
| `-j N`, `--timings out.json` | threads; Perfetto trace (0.15: needs explicit file) |
| `--open [viewer]` | open output after compile |
| `--port/--no-serve/--no-reload` | (watch, HTML/bundle) dev server controls |
| `--cert PATH` (`TYPST_CERT`) | custom CA for package downloads; `--color auto\|always\|never` |

Examples:

```bash
typst compile main.typ                              # main.pdf
typst compile main.typ build/out.pdf --root .
typst compile main.typ 'page-{0p}-of-{t}.png' --ppi 200          # {p} number, {0p} zero-padded, {t} total
typst compile main.typ - -f svg --pages 1 > first.svg
typst compile main.typ out.pdf --pdf-standard a-2b --creation-timestamp 1700000000
typst compile main.typ - -f html --features html      # HTML to stdout
typst watch main.typ --open
typst eval '"a,b".split(",")'                          # → ["a","b"]
typst eval --in main.typ 'query(heading).len()'
echo '#set page(width: auto, height: auto); $x^2$' | typst compile - out.png -f png
```

Exit status is 1 on errors (warnings don't fail). Diagnostics include source spans, hints, and 0.15 traceback frames. Environment variables mirror flags (`TYPST_ROOT`, `TYPST_FONT_PATHS`, `TYPST_PACKAGE_PATH`, `TYPST_PACKAGE_CACHE_PATH`, `TYPST_FEATURES`, `SOURCE_DATE_EPOCH`, `TYPST_IGNORE_SYSTEM_FONTS`).

### Package locations

- Cache (downloaded `@preview`): macOS `~/Library/Caches/typst/packages/`, Linux `~/.cache/typst/packages/`, Windows `%LOCALAPPDATA%\typst\packages\`.
- Local (`@local/name:ver`): macOS `~/Library/Application Support/typst/packages/local/name/ver/`, Linux `~/.local/share/typst/packages/local/name/ver/`, Windows `%APPDATA%\typst\packages\local\name\ver\`.
- Offline CI: pre-populate the cache or set `--package-cache-path`; Typst downloads from `packages.typst.org` on first import.

### Fonts

`typst fonts` lists everything discovered; `--font-path ./fonts` adds a folder; embedded defaults: Libertinus Serif, New Computer Modern (+Math), DejaVu Sans Mono. System fonts are used by default. Unknown font → warning + fallback (check output for `unknown font family`). Variable fonts supported in 0.15 (family name without "Variable"). CJK/emoji need fonts installed (e.g. Noto Sans CJK, Noto Color Emoji). Font features via `text(features: ("liga", "ss01": 1))`.

### Reproducible / CI builds

```bash
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) typst compile main.typ out.pdf --root . \
  --package-cache-path .typst-cache --deps deps.json
```

## Output formats

| Format | Status | Notes |
| --- | --- | --- |
| **PDF** | stable, default | tagged (accessible baseline) by default since 0.14; standards via `--pdf-standard` |
| **PNG** | stable | one file per page, needs `{p}` placeholder if >1 page; `--ppi` |
| **SVG** | stable | one file per page; text as outlines or fonts; minified (0.15) |
| **HTML** | experimental (`--features html`) | semantic HTML, no CSS output yet; equations as MathML (0.15) |
| **Bundle** | experimental (`--features bundle`) | many output files from one project |

### PDF details

- Metadata from `#set document(title:, author:, keywords:, description:, date:)`; PDF/UA needs a title and `lang`.
- Bookmarks come from headings (numbered since 0.14); named destinations for labelled headings (0.15).
- Attachments: `#pdf.attach("data.csv", relationship: "data", mime-type: "text/csv", description: "Source data")` (renamed from `pdf.embed`; PDF 1.7+, allowed in PDF/A-3/A-4f; `data:` may be bytes).
- Mark decorative content: `#pdf.artifact(kind: "page")[...]`; headers/footers/hyphens are automatic artifacts.
- Selecting a standard: archival with accessibility → `a-2a` (or `a-3a` if you need attachments, `a-4` for PDF 2.0); archival without accessibility → `a-2u`; only accessibility → `ua-1`; both → `a-2a,ua-1`. `ua-1` and `a-4*` are incompatible (UA-1 needs PDF ≤1.7, A-4 needs 2.0). Rules of thumb: prefer `u` over `b`; `a` levels require tagged PDF and no Private-Use code points.
- Embedding PDFs as images requires the output version ≥ the image's version.
- Text copy/paste works with correct Unicode; hyphenation artifacts are mapped.
- Page labels follow page numbering; `--pages` selects physical pages.
- Features: spot/separation colors (0.15), CMYK, ICC, blend modes in imported PDFs, JPEG2000/JBIG2 images.

### PNG / SVG

- Transparent PNG: `#set page(fill: none)`; crop to content: `#set page(width: auto, height: auto, margin: 5pt)`.
- Both formats are **not accessible** (no tags/alt text) and one file per page.
- Page sizes: `paper:` or width/height; `--ppi` scales pixel dimensions.

### HTML (experimental)

```bash
typst compile doc.typ doc.html --features html          # or -f html
```

- Use `target()` (available without the flag in 0.15; **requires `context`**) to branch: `#context if target() == "html" [...] else [...]`.
- Typed API: every standard tag exists as `html.<tag>` (`a abbr article aside audio blockquote br button canvas caption code col details div dl em figure footer form h1–h6 header hr i iframe img input kbd label li main mark nav ol p pre q ruby s section small span strong sub summary sup table tbody td th thead tr u ul video …`), e.g. `html.div(class: "box")[...]`, `html.span`, `html.img(src: ..., alt: ...)`, `html.elem("custom-tag", attrs: (data-x: "1"))[...]`, `html.frame[...]` (render content as inline SVG), `html.script("...")`/`html.style("css")` take **strings only** (0.15). Attributes are typed (`width: 400` integer, `controls: true`).
- Semantic elements map automatically: headings, paragraphs, lists, tables, figures/captions, quotes, links, footnotes, outlines, bibliography, `raw` (with syntax highlighting), sub/super, underline/strike/highlight, smallcaps, math (MathML).
- Styling: Typst emits no CSS for your document's `set`/`show` styling (only a small built-in `<style>` block that makes MathML/tables render) — add a stylesheet via `html.elem("link", attrs: (rel: "stylesheet", href: "style.css"))` inside a `show: ...` that adds to the head, or `html.style(...)`. `<html lang>` follows `text.lang` (0.15). Minified by default; `--pretty` for readable output.
- Unsupported-in-HTML elements produce warnings ("was ignored during HTML export"); wrap with show rules: `#show math.equation.where(block: false): it => html.span(role: "math", html.frame(it))` (not required for MathML in 0.15).
- `box` = inline-level container, `block` = block-level; custom elements should wrap block-level output in `block` so paragraphs are grouped consistently (0.15).
- Share content between PDF and HTML by writing templates with `target()` branches.

### Bundle (experimental)

```bash
typst compile site.typ dist -f bundle --features bundle,html
typst watch site.typ dist -f bundle --features bundle,html      # dev server (port 3000+)
```

```typ-x
#document("index.html", title: [Home])[ #title() - #link(<blog>)[Blog] ]
#document("blog.html", title: [Blog])[ Hello! ] <blog>
#document("blog.pdf", title: [Blog])[ ... ]
#asset("favicon.ico", read("favicon.ico", encoding: none))
```

`document(path, format:, title:, ..)` produces one output per call (HTML/PDF/PNG/SVG by extension); `asset(path, data)` writes raw bytes/strings. Labels, counters, states, queries are global across the bundle (except the `page` counter). Links between documents resolve relative paths automatically.

## Accessibility checklist (PDF/UA-1, WCAG-ish)

1. `#set document(title: ...)` (+ `#title()`); `#set text(lang: "xx")` first in the file (switch with `#text(lang: "fr")[...]`).
2. Use semantic elements: `heading` (no skipped levels, start at 1 under `title`), `list`/`enum`/`terms`, `table` with `table.header` (not `grid`), `figure` + `caption`, `quote`, `link`, `footnote`, `outline`.
3. `alt:` for every `image` and for non-text figures; PDF/UA export fails if alt text is missing. Math: provide `math.equation(alt: "...")` (UA-1 can't derive it automatically).
4. Decorative content → `pdf.artifact(...)`.
5. Reading order = source order; position `place`/floats at the logical spot in the markup.
6. Don't convey meaning by color/layout alone; contrast ≥ 4.5:1 (text) / 3:1 (large/graphics); avoid images of text.
7. Use `--pdf-standard ua-1` to get automatic checks; verify with veraPDF (conformance), PAC (PDF/UA), Acrobat accessibility check; try a screen reader (VoiceOver/NVDA).
8. Consider also shipping HTML (`--features html`) for the best AT support.
9. Complex tables: experimental `pdf.header-cell`, `pdf.data-cell`, `pdf.table-summary` (`--features a11y-extras`).

## Testing the output

```bash
typst compile doc.typ doc.pdf && pdftotext -layout doc.pdf -         # text check
typst compile doc.typ 'p-{p}.png' --ppi 100                           # then view images
typst eval --in doc.typ 'query(heading).map(h => h.body.text)'        # structural check (text-only bodies)
typst eval --in doc.typ 'query(<pages>).first().value'                # page count, if doc has #context [#metadata(counter(page).final().first()) <pages>]
typst eval --in doc.typ 'query(figure).len()'
```

(`typst eval --in` prints JSON; content values serialize as `{"func": ..., fields}` objects. Use `.text`, `repr()`, or a `to-string` helper.)
