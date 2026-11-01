---
name: typst
description: Write, edit, debug, compile and package Typst (.typ) documents — papers, reports, theses, CVs, letters, slides, posters, math-heavy notes, data-driven docs. Covers markup/math/code syntax, set/show rules, layout, tables, figures, bibliographies, introspection (counters/state/query), data loading, PDF/HTML/PNG/SVG export, PDF/A and PDF/UA accessibility, CLI (compile/watch/eval/init/fonts), templates, Typst Universe packages, and LaTeX/Markdown conversion. Use whenever the task involves Typst, typst.toml, .typ files, "typst compile", or turning content into a typeset document and Typst is an option.
---

# Typst

Typst is a markup-based typesetting system with a built-in scripting language. One binary compiles `.typ` → PDF (default), PNG, SVG, HTML (experimental), or a multi-file bundle (experimental). This skill targets **Typst 0.15.x** (verified against 0.15.1); notes mark behaviour that differs in older versions.

> Training data about Typst is often stale (0.11–0.13 era). When unsure about a function, parameter or default, **check `references/api-signatures.md`, then compile a probe** (`typst eval '<expr>'` or a 5-line file) instead of guessing.

## Workflow

1. **Clarify the output**: PDF (default), HTML, PNG/SVG, accessible PDF (PDF/UA), archival PDF (PDF/A)? Page size, language, fonts, citation style, template/journal?
2. **Start from a skeleton** (below) or from `examples/`. For a journal/thesis/CV/slide deck, search a package first: `python3 scripts/search-packages.py "ieee paper"` (see `references/packages-and-ecosystem.md`).
3. **Write the file**: put `set`/`show` rules and imports at the top, content below. Split large projects with `#include` and `#import`.
4. **Compile and check**: `typst compile main.typ` — read the diagnostics (they have line:col and hints). Verify visually via PNG (`typst compile main.typ 'p-{p}.png'`), or textually via `typst compile main.typ - -f html --features html` / `pdftotext`. Details in `references/pitfalls-and-debugging.md`.
5. **Format** (if available): `typstyle -i file.typ`. Only when the diff is limited to your own edits.
6. Report which files were created/changed and how to rebuild.

## Minimal skeleton

```typ
#set document(title: "My Document", author: "Name")
#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(font: "New Computer Modern", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")

#title()

= Introduction <intro>
Typst supports *bold*, _italic_, `raw`, math $E = m c^2$ and references like @intro.

== A subsection
#lorem(30)

$ integral_0^1 x^2 dif x = 1/3 $
```

Always-safe defaults: `#set text(lang: "...")` (hyphenation, quotes, supplements, a11y), `#set document(title: ...)` + `#title()` for the visible title, `#set par(justify: true)` for body text.

## Syntax in 60 seconds

| Mode | Enter with | Example |
| --- | --- | --- |
| Markup (default) | — | `= Heading`, `*strong*`, `_emph_`, `- item`, `+ numbered`, `/ Term: desc`, `@label`, `<label>` |
| Code | `#` (one expression) or `#{ ... }` block | `#let x = 3`, `#f(1)[body]`, `#if a [yes] else [no]`, `#for i in range(3) [#i ]` |
| Math | `$...$` (`$ x $` with spaces = display) | `$a^2 + b_i$`, `$sum_(i=1)^n i$`, `$ vec(1, 2) $` |
| Content block | `[...]` inside code | `#box[hi]`, `let c = [*x*]` |

- Inside code, **do not repeat `#`**: `#figure(image("a.png"), caption: [Hi])`. Inside `[...]` content blocks you are back in markup: `[Total: #x]`.
- Arrays `(1, 2)`, dictionaries `(a: 1, b: 2)`, empty `()` / `(:)`, one-element `(1,)`. There are **no tuples**. Index with `.at(i)`, not `[i]`.
- Named args use `:` (`f(width: 2cm)`); `=` is assignment only inside `let`/code.
- Strings `"..."`, content `[...]`, raw `` `...` ``. Convert with `str(x)`, `[#s]`, `eval(s, mode: "markup")`.
- Comments: `// line`, `/* block */`. Escape specials with `\` (`\#`, `\$`, `\@`, `\*`, `\_`, `\<`); unicode `\u{1F600}`.
- Length units: `pt mm cm in em`, `fr` (fraction), `%`, angles `deg rad`. `auto` and `none` are values.
- `set` = default arguments for an element from here on; `show` = re-style/replace elements. `context` is required to read styles/counters/positions (see `references/introspection.md`).
- Paths: forward slashes only (0.15). `"/x.typ"` is project-root-relative (default root: directory of the main file; change with `--root`), `"x.typ"` is relative to the current file.
- Method syntax everywhere: `"abc".len()`, `(1,2,3).map(x => x*2)`, `rgb("#f00").lighten(30%)`.

## Where to look

| Need | Read |
| --- | --- |
| Syntax, types, operators, string/array/dict methods, modules, closures, `context` basics | `references/syntax-and-scripting.md` |
| `set`/`show` rules, selectors, page setup, text, paragraphs, blocks, grids, columns, alignment, spacing, placement, transforms | `references/styling-and-layout.md` |
| Headings, lists, figures, tables, references, footnotes, outlines, quotes, bibliography/citations/CSL, numbering, links, metadata | `references/document-model.md` |
| Equations, math syntax, symbols, matrices, alignment, fonts, numbering | `references/math.md` |
| Shapes, curves, images, colors, gradients, tilings, strokes, spot colors | `references/visuals.md` |
| Counters, state, `query`, `locate`, `metadata`, `within`, layout convergence, running headers, `measure`/`layout` | `references/introspection.md` |
| CSV/JSON/YAML/TOML/XML/CBOR, `read`, `bytes`, `sys.inputs`, `eval`, WASM plugins, data-driven docs | `references/data-and-io.md` |
| CLI flags, fonts, PDF/A/UA, accessibility, HTML, bundle, PNG/SVG, `typst eval`, CI/reproducible builds | `references/export-and-cli.md` |
| Slide decks (Touying/Polylux, animations, handouts, speaker notes, pdfpc) | `references/slides.md` |
| Templates, `typst.toml`, publishing packages, Universe package picks (cetz, fletcher, touying, codly, ...), editor tooling | `references/templates-and-packages.md`, `references/packages-and-ecosystem.md` |
| LaTeX → Typst translation, Markdown/pandoc conversion, upgrading from 0.11–0.14 | `references/migration.md` |
| Errors, warnings, probes, visual verification, performance, common gotchas | `references/pitfalls-and-debugging.md` |
| Exact parameters/defaults of every element (verified against 0.15.1 source) | `references/api-signatures.md` |
| Ready-to-compile starters | `examples/*.typ` |

## Top pitfalls (read before writing)

1. **Set/show rules apply forward and only inside their scope**; put them before the content they should affect. A `set` inside `[...]`/`{...}` ends with the block.
2. **Reading anything that depends on position/style needs `context`**: `#context counter(page).get()`, `#context text.size`. Without it: "can only be used when context is known".
3. **Variables captured by closures are read-only copies**; accumulate via `fold`, loops in a single code block, `state`, or `counter`.
4. **`#` is needed once**; `#(a + b)` for expressions with operators in markup; `#f(x).g` works but `#f (x)` (space) does not call.
5. **Math is not text**: multi-letter words are symbols/variables (`alpha`, `sin`); write text as `"text"` or `upright(...)`. Single letters are italic variables.
6. **Strings are not content**: a heading body is content; use `.body`, `str()`, or helper `to-string` (see syntax reference) to get text.
7. **Fonts**: only installed/embedded/`--font-path` fonts work; an unknown family only warns and falls back. List with `typst fonts`. For variable fonts omit "Variable"/"VF" in the name (0.15).
8. **Packages** are imported with exact versions: `#import "@preview/cetz:0.5.3"` — look up the latest at Typst Universe (`scripts/search-packages.py`) rather than trusting memory. Packages may lag behind a new compiler.
9. **0.15 removals**: `path()` → `curve()`, `pattern` → `tiling`, `pdf.embed` → `pdf.attach`, `*.decode(...)` → pass `bytes` to `json(...)` etc., `typst query` → `typst eval`, no backslashes in paths.
10. **HTML/bundle export are experimental** and need `--features html` / `--features bundle`.

## Quick idioms

```typ
// Reusable template: show rule with function
#let conf(title: none, authors: (), body) = {
  set page(margin: 2cm)
  set par(justify: true)
  align(center, text(17pt, weight: "bold", title))
  v(1em)
  body
}
#show: conf.with(title: [My Paper])

// Style one heading level
#show heading.where(level: 1): set text(navy)
#show heading.where(level: 1): it => block(above: 1.5em, below: 1em, it)

// Cross-references & figures
#figure(table(columns: 2, [A], [B], [1], [2]), caption: [Data]) <tab:data>
See @tab:data.

// Data-driven content
#for (name, score) in (("Ann", 3), ("Bo", 5)) [- #name: #score]

// Run-time input from CLI: typst compile --input mode=draft main.typ
#let draft = sys.inputs.at("mode", default: "final") == "draft"
```

## Compile cheatsheet

```bash
typst compile main.typ                 # → main.pdf
typst compile main.typ out.pdf --root .
typst compile main.typ 'page-{0p}.png' --ppi 144
typst watch main.typ                   # recompile on change
typst eval 'calc.pow(2, 10)'           # evaluate an expression, JSON output
typst eval --in main.typ 'query(heading).len()'
typst init @preview/charged-ieee       # new project from a template
typst fonts --variants                 # installed fonts
```

## Examples (all compile on 0.15.1)

| File | Shows |
| --- | --- |
| `examples/memo.typ` | short memo, header grid, simple styling |
| `examples/report.typ` | title page, outline, running header, figures/tables/footnotes, show rules |
| `examples/academic-paper.typ` (+ `refs.bib`) | equations, theorem environments, cross-refs, citations |
| `examples/data-report.typ` (+ `data.csv`) | CSV → table, computed columns, `--input`, plain-shape bar chart |
| `examples/template.typ` + `template-usage.typ` | reusable template function + components |
| `examples/accessible.typ` | PDF/A-2a + PDF/UA-1 (`--pdf-standard a-2a,ua-1`) |
| `examples/dual-target.typ` | one source → PDF and HTML (`context target()`, `html.*`) |
| `examples/query-export.typ` | `metadata` + `typst eval` structure export |
| `examples/slides-plain.typ`, `examples/letter.typ` | package-free slides and a formal letter |
| `examples/packages-demo.typ` | cetz, fletcher, lilaq, theorion, codly (pinned, verified versions) |

## Scripts

- `scripts/check-snippets.py FILE.md…` — compiles every ```` ```typ ```` block (use ```` ```typ-x ```` for illustrative/non-compiling blocks). Run it on any Markdown you write that contains Typst.
- `scripts/search-packages.py "keywords" [--category cv] [--name cetz --versions]` — query the Typst Universe index for current package names/versions.
