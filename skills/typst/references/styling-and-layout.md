# Styling and layout

## Set rules

`#set element(param: value, ...)` changes defaults of **settable** parameters (those not marked required/positional-only in `api-signatures.md`) for everything after it in the current scope (file, `[...]`, `{...}`).

```typ
#set page(paper: "a4", margin: (x: 2.5cm, y: 3cm), numbering: "1 / 1", number-align: center)
#set text(font: ("Libertinus Serif", "Noto Serif"), size: 11pt, lang: "en", region: "gb", hyphenate: true)
#set par(justify: true, leading: 0.65em, spacing: 1.2em, first-line-indent: (amount: 1.5em, all: true))
#set heading(numbering: "1.1.")
#set list(marker: ([•], [–]), indent: 1em)
#set enum(numbering: "1)")
#set math.equation(numbering: "(1)")
#set figure(supplement: [Fig.])
#set table(stroke: 0.5pt + gray, inset: 6pt)
#set document(title: [My Title], author: ("A", "B"), keywords: ("x", "y"), date: auto)
Hello.
```

- `set text(red)` — one positional shortcut exists for common first parameters (`text(size)`, `text(font)`…: `#text(14pt)[big]`, `#text(red)[x]`, `#text("Fira Sans")[x]`).
- Conditional set: `#set text(fill: red) if draft`.
- `par.first-line-indent`: `1.5em` or `(amount: 1.5em, all: true)` (`all: true` also indents the first paragraph and paragraphs after headings; partial dicts fold in 0.15).
- `par.justification-limits` (0.14+) enables character-level justification: `(tracking: (min: -0.012em, max: 0.012em), spacing: (min: 75%, max: 120%))` — noticeably better justified text.
- `par.linebreaks: "optimized"` (Knuth–Plass, default for justified) or `"simple"`.
- `par.hanging-indent`, `par.line(numbering: "1", number-clearance: ...)` for line numbers (`#set par.line(numbering: "1")`).

## Show rules

```typ
#set heading(numbering: "1.")

// 1. show-set: apply a set rule to selected elements
#show heading: set text(navy)
#show heading.where(level: 1): set align(center)

// 2. transform: replace with a function of the element
#show heading.where(level: 1): it => block(width: 100%, above: 2em, below: 1em)[
  #set text(18pt, weight: "bold")
  #counter(heading).display() #it.body
]

// 3. text / regex show rules
#show "Typst": name => text(weight: "bold", fill: eastern, name)
#show regex("\b[A-Z]{2,}\b"): set text(tracking: 1pt)

// 4. show everything (templates): function receives the rest of the document
#let article(body) = { set par(justify: true); body }
#show: article

// 5. label selector, within-selector, or / and
#show <important>: set text(red)
#show selector(heading).or(figure): set block(breakable: false)
#show figure.where(kind: table): set figure.caption(position: top)

= Title
Typst is great. <important>
```

Selector forms: element function (`heading`), `elem.where(field: value, ...)`, label `<l>`, string/regex, `selector.or/and/before/after` (`.within(...)` works in `query` but **cannot be used in `show` rules** yet), `selector(heading).after(<start>)`, `elem.where(...)`; `show: f` for "everything else". A show rule replaces the element; inside the body use `it.fields` / `it.body` / `it.level` / `it.numbering` / `it.supplement` etc. To keep the default rendering plus tweaks use show-set or call the original with `set`s inside: `show heading: it => { set text(red); it }`.

Pitfalls:
- A show rule can recurse only if the body doesn't re-produce the same element in a loop (e.g. `show heading: it => heading(it.body)` loops — use `it` itself or `block(it)`).
- Show rules run in **document order, last defined wins** (later rules wrap earlier ones); a show rule is applied to elements created *after* its definition, including those produced inside templates.
- Show rules on text match across styled/spans poorly; regex matches only within a single text run (no matching across `*bold*` boundaries).
- `#show page` is unsupported (warning in 0.15).
- `#show: it => ...` is the idiom for templates (must be at file top, before content).

## Page setup

```typ
#set page(
  paper: "a4",                         // "us-letter", "a5", "a3", "presentation-16-9", ... or width:/height:
  flipped: false,                      // landscape
  margin: (inside: 3cm, outside: 2cm, y: 2.5cm), // x, y, top, bottom, left, right, inside, outside, rest
  binding: auto,                       // left/right (affects inside/outside)
  columns: 2,
  fill: white,                         // background
  numbering: "1",                      // page counter format; none to disable
  number-align: center + bottom,
  header: context [ #h(1fr) #counter(page).display() ],
  footer: [Confidential],
  header-ascent: 30%, footer-descent: 30%,
  background: place(top + right, image("a.png", width: 3cm)),   // behind content each page
  foreground: none,
  bleed: 3mm,                          // 0.15, print bleed
)
```

- Per-section page changes: `#pagebreak()` then `#set page(...)` — a new `set page` implicitly starts a new page. `#pagebreak(weak: true)` avoids blank pages; `#pagebreak(to: "odd")` for books.
- Different first page: `#set page(header: context { if counter(page).get().first() > 1 [ ... ] })`. Better: use `#page(header: none)[ ... ]` for a standalone page.
- Page numbering style per section: `#set page(numbering: "i")`, then `#counter(page).update(1)` + `#set page(numbering: "1")`.
- `numbering` accepts a pattern string (`"1"`, `"1 / 1"`, `"i"`, `"I"`, `"a"`, `"A"`, `"一"`, `"(1)"`) or a function `(n, ..totals) => ...`. Total pages: `#context counter(page).final().first()`.
- Landscape/single wide page inside a document: `#page(flipped: true)[...]` (page-scoped element).
- Columns: `#set page(columns: 2)` (preferred; footnotes/line numbers keep working) or `#columns(2, gutter: 8pt)[...]`; `#colbreak()`; one-column title spanning: `#place(top + center, scope: "parent", float: true, title-content)`; `#set columns(gutter: ...)`.
- Header/footer content is a `content` or a function in `context`. For "chapter name in header" use `query`/`hydra` (see `introspection.md`).
- Page size units: `paper` names are case-insensitive strings; US: `"us-letter"`, `"us-legal"`.

### More page-setup recipes (from the official guide)

- `#set page("a5")` / `#set page("us-letter")`: the first positional argument is the paper. `margin: auto` scales margins with the page size (≈ 2.5/21 of the shorter side) and is the default; `margin: (inside: 2.5cm, outside: 2cm, y: 1.75cm)` + `binding: left|right` for books (binding defaults from `text.lang`: right for RTL languages).
- **Setting a custom `footer`/`header` disables automatic `numbering` output** — print the number yourself: `#set page(footer: context [ *Org* #h(1fr) #counter(page).display("1/1", both: true) ])` (`both: true` makes the pattern show current **and** final page number).
- Per-page header logic: `header: context { if here().page() == 1 { none } else [ ... ] }`, or choose by element: query headings on the current page (`query(heading).any(h => h.location().page() == here().page())`).
- Skip/shift numbers: `#counter(page).update(1)` (place at the start of a page or it forces a break) or `update(n => n + 5)`; the physical page is `#context here().page()`; numbering pattern of a location: `loc.page-numbering()`.
- Fun footers/ornaments: `let (num,) = counter(page).get()` then build `num * (box(circle(radius: 2pt)),)` and `.join(h(1pt))`.
- **Columns**: no automatic balancing on the last page — balance by hand with `#colbreak()`. For a spanning title in a 2-column page use `place(top + center, float: true, scope: "parent", title())`. Use the `columns()` function only inside nested layouts (e.g. a `rect`), not for whole pages. `#set columns(gutter: 12pt)`.
- **One-off pages**: `#page(flipped: true)[ big table ]`, `#page(margin: 0pt, fill: black)[ cover ]`, `#page(columns: 1)[...]` apply the overrides to those pages only and then revert.

## Text

```typ
#text(font: "Fira Sans", size: 12pt, weight: "bold", style: "italic", fill: blue,
      stretch: 90%, tracking: 0.5pt, spacing: 100%, lang: "de", hyphenate: false,
      features: ("smcp",), number-type: "old-style", number-width: "tabular", ligatures: false,
      stylistic-set: 1, slashed-zero: true, fractions: true, kerning: true, baseline: 2pt,
      top-edge: "ascender", bottom-edge: "descender", fallback: true, overhang: true)[sample]
```

- `font`: family string or array (fallback order). Variable fonts (0.15): use the family name without "Variable/VF"; select weights with `weight:` and extra axes with `variations: ("wght": 450)`; `weight` accepts `"regular" "bold" "light" 100–900`, `stretch` a ratio, `style` `"normal" "italic" "oblique"`.
- `font` with `covers`: `(name: "Noto Sans CJK SC", covers: "latin-in-cjk")` to scope a font to a script subset.
- `lang`/`region` drive hyphenation, smart quotes, figure supplements ("Abbildung"), date formats, and accessibility. Set it first.
- `size` accepts length; `em` is relative to current size. `#text(1.2em)[...]`.
- `top-edge`/`bottom-edge`: `"cap-height" "x-height" "baseline" "bounds"`, change line-box size (use `bounds` + `par(leading)` to tighten).
- `text.script`, `dir: rtl` for RTL text (auto-detected via lang/script).
- Decorations: `underline(offset:, stroke:, evade:)`, `overline`, `strike`, `highlight(fill:, extent:, radius:)`, `smallcaps(all: true)`, `sub`, `super`, `upper`, `lower`, `strong`, `emph`, `smartquote`, `raw`.
- Lorem: `#lorem(40)`.
- `h(1fr)` / `h(2em)` horizontal space (`weak: true` collapses at line edges); `v(1em)` vertical.
- Linebreak: `\`, `#linebreak(justify: true)`; no-break: `~`, `#box[...]`; `#sym.wj` word joiner.

Fonts in the web app are limited to bundled ones; the CLI uses system fonts plus embedded defaults (Libertinus Serif, New Computer Modern(+Math), DejaVu Sans Mono). Default text font: **Libertinus Serif**, 11pt, black.

## Paragraphs and blocks

Paragraph spacing is `par.spacing` (between paragraphs) vs `par.leading` (between lines). Block-level things (headings, figures, tables, lists, `block`) use `block.spacing` (default `1.2em`) — set `#set block(spacing: 0.8em)`; per-element `above`/`below`.

```typ
#block(fill: luma(245), inset: 10pt, radius: 4pt, stroke: 0.5pt + gray, width: 100%, breakable: true)[
  Block-level container.
]
#box(fill: yellow, inset: (x: 3pt, y: 0pt), outset: (y: 3pt), radius: 2pt)[inline]
#rect(width: 4cm, height: 1cm, fill: red)   // see visuals.md for shapes
#pad(x: 1cm, y: 4pt)[padded]
#align(center + horizon)[centered]    // left/center/right/start/end + top/horizon/bottom
#align(right)[#text(8pt)[Right-aligned note]]
```

- `box` is inline (sits in a line; since 0.15 its baseline is that of its first line), `block` is its own paragraph-level container. `block(sticky: true)` keeps a heading with the next block. `block(breakable: false)` keeps content on one page. Use `clip: true` to crop content to the box.
- Sizes: `width`/`height` accept lengths, ratios (`50%` of the container), relative (`100% - 2cm`), fractions (`1fr` in `block.height` or grid tracks; `box.width: 1fr`).
- `h(1fr)` fills; `#h(1fr) text #h(1fr)` centers; `repeat[.]` fills a width with dots (leaders): `Chapter #box(width: 1fr, repeat[.]) 12`.
- `#v(1fr)` pushes subsequent content to the bottom of the page/container.
- `#stack(dir: ltr, spacing: 1em, a, b, c)`; `dir` is `ltr rtl ttb btt`.
- `#hide[x]` keeps the space but not the ink. `#place(...)` takes content out of flow (see below).

## Grid

```typ
#grid(
  columns: (1fr, 2fr, auto),     // auto | length | fr | array; an int = that many auto columns
  rows: auto,
  gutter: 8pt,                   // or column-gutter / row-gutter
  align: (left, center + horizon, right),   // single value, array per column, or (x, y) => ...
  fill: (x, y) => if calc.odd(y) { luma(245) },
  stroke: (x, y) => (bottom: 0.5pt),
  inset: 6pt,
  [A], [B], [C],
  grid.cell(colspan: 2)[wide], [D],
  grid.cell(rowspan: 2, fill: yellow)[tall], [E], [F],
  grid.hline(stroke: 1pt), grid.vline(x: 1),
)
```

- Children fill row by row; `grid.cell(x:, y:, colspan:, rowspan:, align:, fill:, stroke:, inset:, breakable:)`.
- `grid.header(repeat: true, level: 1, ..)` / `grid.footer(...)` repeat on page breaks; multiple levels (0.14+).
- `align`, `fill`, `stroke`, `inset` accept functions `(x, y) => value` (0-based; subtract 1 to skip header rows).
- A grid is layout only (no accessibility semantics); use `table` for data.
- Common layout: two-column caption `#grid(columns: (auto, 1fr), column-gutter: 1em, [Label], [Text])`; image + caption row; signature lines `line(length: 5cm)`.

## Placement and transforms

```typ
#place(top + right, dx: -1cm, dy: 1cm, rotate(-20deg)[DRAFT])       // overlay, out of flow
#place(bottom + center, float: true, clearance: 1em)[#figure(rect(), caption: [Floats to the bottom])]   // floating figure
#place(top, scope: "parent", float: true)[...]                       // span all columns
#rotate(90deg, reflow: true)[sideways]   // reflow:true makes layout use rotated size
#scale(x: 80%, y: 100%, origin: left)[squeezed]    // scale(150%)[big]
#move(dx: 3pt, dy: -2pt)[nudged] #skew(ax: 15deg)[slanted]
#layout(size => { let w = size.width; box(width: w / 2, [half]) })   // inspect container size
#context measure(text("hello")).width     // natural size of content
```

`place` without `float` is relative to the parent container (page content area for top-level); `alignment` default `start`; `scope: "parent"` + `float: true` spans columns; `flush()` forces pending floats to be placed. `layout(size => ...)` gives the available `width`/`height` (lengths or `auto`→ may be `auto`-free here); `measure(content)` needs `context`, honours current styles, and returns `(width:, height:)`. Use `measure(..., width: x)` to measure at a given width.

## Lists

```typ
#set list(marker: [•], body-indent: 0.5em, indent: 1em, spacing: 0.6em, tight: true, marker-align: top)  // marker-align 0.15
#set enum(numbering: "1.a)", start: 3, full: true, reversed: false, number-align: start)
#set terms(hanging-indent: 3em, separator: [: ], tight: false)
- A
+ B
/ Term: Desc
#enum.item(5)[Explicit number]
```

`tight: true` uses `par.leading`-like spacing; blank lines between items make the list loose. `enum(full: true)` shows `1.1.1` multi-level numbers. Markers cycle per nesting level when `marker` is an array. 0.15: `list.marker-align` (default aligns marker baseline with first line, end-aligned horizontally) and centering in list items now relative to full width.

## Numbering patterns

Counting symbols: `1 a A i I α Α 一 壹 あ い ア イ א 가 ㄱ * ① ⓵ ...` plus Armenian/Arabic-abjad/Tibetan (0.15). Pattern examples: `"1."`, `"(a)"`, `"I.1"`, `"1.1.1"`, `"A.1"`, `"§1"`. A function `(..nums) => ...` allows custom formats. Symbol `*` cycles `* † ‡ § ¶ ‖` (footnotes).

## Headings

`#set heading(numbering: "1.1", supplement: [Section], outlined: true, bookmarked: auto, hanging-indent: auto, offset: 0)`. Appendix: `#counter(heading).update(0)` then `#set heading(numbering: "A.1")` (and a label like `<appendix>` on a heading to use `within`). `heading(level: 2)[...]` explicit level; `#heading(outlined: false, numbering: none)[Unnumbered]`; `offset:` shifts all levels (for `include`d chapters). Heading numbering in the reference text uses `supplement` + number: `@intro` → "Section 1".

Show rule skeleton with numbering:

```typ
#set heading(numbering: "1.1")
#show heading: it => {
  let num = if it.numbering != none { counter(heading).display(it.numbering) + h(0.5em) }
  block(above: 1.4em, below: 0.8em, sticky: true, text(weight: "bold", size: 1.2em, [#num#it.body]))
}
= Chapter
```

## Footnotes

`#footnote[text]`; `#set footnote(numbering: "*")`; separate styling via `#show footnote.entry: set text(8pt)`; `#footnote(<label>)` re-uses a note; reference same note again with `@label` after labeling the footnote (`#footnote[..] <fn1>`). Separator: `#set footnote.entry(separator: line(length: 30%, stroke: 0.5pt))`.

## Visibility, grouping, utilities

- `#set text(hyphenate: true)` plus `lang` for automatic hyphenation; manual soft hyphen `-?`.
- `#h(0pt, weak: true)` removes surrounding spaces (also in HTML in 0.14+).
- `#pagebreak()`, `#colbreak()`, `#parbreak()`; `#box(height: 1fr)`; `#line(length: 100%, stroke: 0.5pt)`; `#divider()` (0.15, thematic break `---`-like; style via show rule).
- `style` (old) is gone; use `context`.
- Dark/colored page: `#set page(fill: rgb("#1e1e2e")); #set text(fill: white)`.
- Draft toggles: `#let draft = sys.inputs.at("draft", default: "0") == "1"`, `#set page(background: if draft { rotate(45deg, text(80pt, gray.lighten(80%))[DRAFT]) })`.

## Consistency tips for generated documents

- Define colors, fonts and spacing once at the top (`#let accent = rgb("#0b6e99")`) and reuse.
- Prefer `show` rules and template functions over per-use formatting.
- Use semantic elements (headings, figures, lists, tables) not manual spacing — gives structure for PDF tags, outlines, HTML.
- Keep text language-aware: set `lang`, use smart quotes, non-breaking spaces `~` before units/citations.
