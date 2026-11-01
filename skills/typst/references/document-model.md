# Document model: structure, figures, tables, references, bibliography

## Document metadata and title

```typ
#set document(title: [Typst skill], author: ("Ada", "Bob"), description: [Short], keywords: ("typst", "docs"), date: datetime(year: 2025, month: 1, day: 31))
#title()          // renders the document title (set above) as a level-0 heading; or #title[Custom]
```

- `document.title` accepts content or string; it sets PDF title/HTML `<title>`. `date: auto` = compile time, `none` = omit. Authors/keywords also go into PDF/HTML metadata. PDF/UA requires a title.
- `#title()` is the semantic title (tagged `H1`/`Title`); style it with `#show title: set text(20pt)`. Headings should then start at level 1.

## Headings, outline

See `styling-and-layout.md` for numbering and show rules.

```typ
#outline()                                             // table of contents (headings)
#outline(title: [Contents], depth: 2, indent: auto)    // indent: auto | length | function
#outline(title: [Figures], target: figure.where(kind: image))
#outline(title: [Tables], target: figure.where(kind: table))
#outline(title: none, target: heading.where(supplement: [Appendix]))
#show outline.entry.where(level: 1): set text(weight: "bold")
#show outline.entry: it => link(it.element.location(), it.indented(it.prefix(), it.inner()))  // 0.13+ API: indented/prefix/inner/body/page
#set outline.entry(fill: repeat[ . ])  // fill is on outline.entry since 0.13
```

Heading with `outlined: false` is omitted. For an appendix, `#show: appendix` pattern or `#counter(heading).update(0)` + `#set heading(numbering: "A.1")`.

## Figures

```typ
#figure(
  image("a.png", width: 80%),
  caption: [Results for #lorem(3).],
  alt: "Bar chart of accuracy per model",    // image alt text (accessibility) — also on image(alt:)
  placement: auto,           // none | auto | top | bottom ; floats the figure
  supplement: [Figure],      // text in refs; auto from kind+language
  numbering: "1",
  gap: 0.65em, outlined: true, kind: auto, scope: "column",
) <fig:plot>

@fig:plot shows... // "Figure 1"
```

- `kind`: auto-detected (image → `image`, table → `table`, raw → `raw`, else `figure`... for own kinds use `kind: "algorithm", supplement: [Algorithm]`). Each kind has its **own counter**. `#figure(kind: "theorem", supplement: [Theorem], body)` is how theorem packages work.
- Caption control: `figure.caption(position: top, separator: [. ])`; `#show figure.caption: it => [*#it.supplement #context it.counter.display(it.numbering)#it.separator* #it.body]`; align: `#show figure.caption: set align(left)`; table captions on top: `#show figure.where(kind: table): set figure.caption(position: top)`.
- Subfigures: nested `figure`s don't share numbering — use `subpar` package or a grid of `figure`s with `kind: "subfigure"`.
- Multi-page / side figures: `figure(..., placement: top)` and `scope: "parent"` for column-spanning floats.
- Reference with custom supplement: `@fig:plot[Fig.]` or `#ref(<fig:plot>, supplement: [Fig.])`. Disable the figure number in refs: `#set figure(numbering: none)` (then use `ref` with explicit supplement).
- `#figure(table(...))`: wrap tables in figures for captions + numbering + refs. Tables may break across pages unless `show figure: set block(breakable: false)`.

## Tables

```typ
#table(
  columns: (auto, 1fr, 1fr),          // int, or array of auto | length | fr
  align: (left, right, right),        // or (x, y) => ...
  inset: (x: 8pt, y: 6pt),
  stroke: none,                       // or 0.5pt, (x, y) => ...
  fill: (_, y) => if y == 0 { luma(230) },
  table.header([*Item*], [*Qty*], [*Price*]),
  [Apples], [3], [1.20],
  [Pears], table.cell(colspan: 2, align: center)[sold out],
  table.hline(stroke: 1pt),
  table.footer([Total], [3], [1.20]),
)
```

- Children: strings/content cells are placed row-major; `table.cell(x:, y:, colspan:, rowspan:, fill:, align:, stroke:, inset:, breakable:)`; `table.header(level: n, repeat: true)`, `table.footer`, `table.hline`/`table.vline(x:, y:, start:, end:, stroke:, position:)`.
- Build from data: `table(columns: 3, ..rows.flatten().map(c => [#c]))`, `..for r in rows { r.map(c => [#c]) }`, `csv("data.csv").flatten()`.
- Style via show rules instead of per-cell: `#show table.cell.where(y: 0): strong`, `#show table.cell: set text(9pt)`, `#set table(stroke: (x, y) => (top: if y <= 1 { 1pt } else { 0.5pt }))`.
- Booktabs look: `stroke: none`, `table.hline()` above header, below header, and at the end (`table.hline(stroke: 0.8pt)`), plus `inset: (y: 5pt)`.
- Accessibility: always use `table.header` for header rows; for PDF/UA with complex headers, experimental `pdf.header-cell` / `pdf.data-cell` need `--features a11y-extras`.
- Vertical alignment: `align: horizon`, or `(left + horizon, ...)`. Number alignment: right-align and use `number-width: "tabular"`.
- Rotated header text: `rotate(-90deg, reflow: true)[...]`.
- `table` ≠ layout: for page-layout grids use `grid`.
- **Tables across pages**: tables break across pages by default and `table.header`/`table.footer` repeat (`repeat: false` to stop). A table inside a `figure` can't break by default → `#show figure: set block(breakable: true)` (or `#show figure.where(kind: table): set block(breakable: true)`).
- Per-cell logic in show rules: `#show table.cell.where(y: 0): strong`, `#show table.cell.where(x: 0): set text(style: "italic")`, `#show table.cell: it => if it.x == 0 and it.y > 0 { strong(it) } else { it }` (cells expose `x`, `y`, `colspan`, `rowspan`, `body`).
- Set rules on table parts: `#set table.hline(stroke: 0.6pt)`, `#set table.vline(...)`, `#set table.cell(inset: 4pt)`. Cell-specific `fill`/`stroke` override the table-level function. Individual strokes: `table.cell(stroke: (bottom: 2pt + red))`; double rules: two `table.hline`s with `y:` the same and offset, or `stroke: (bottom: (paint: black, thickness: 2pt, dash: ...))`.
- Merge cells: `table.cell(colspan: 2)[..]` / `rowspan`; positioned cells: `table.cell(x: 1, y: 3)[..]`.
- Rotating a wide table: `rotate(-90deg, reflow: true, table(...))` or put it on its own `#page(flipped: true)[...]`.
- Importing data: `csv("f.csv")` returns an array of arrays of strings — header row is the first element; `moore.slice(1)` skips it; `..moore.flatten()` splats all cells.

## Lists, quotes, dividers, links

```typ
#quote(block: true, attribution: [Donald Knuth])[Premature optimization is the root of all evil.]
#divider()    // thematic break (0.15); style: #show divider: line.with(length: 30%, stroke: 0.5pt)
#link("https://typst.app")[typst.app] #link("mailto:a@b.c") #link((page: 2, x: 0pt, y: 0pt))[page 2]
#show link: underline
#show link: set text(blue)
```

`quote(attribution: <key>)` may cite a bibliography entry. `link` destinations: URL string, label, location (from `locate`/`query`), or dict `(page:, x:, y:)`. Links appear as annotations in PDF. Use `#set link(...)`? (no parameters besides `dest`; style with show rules).

## References and labels

`@label` → `ref`. Target kinds and default supplements: heading ("Section"), figure/table/raw ("Figure"/"Table"/"Listing"), equation ("Equation"), footnote (number), custom elements with `supplement`. Referencing a heading needs heading numbering (or give a supplement and numbering). `ref(form: "normal" | "page")` (`page` gives "page 3"). `#ref(<l>, supplement: none)` prints only the number. Missing target = compile error "label does not exist"; ambiguous label = error; `#show ref: it => ...` customizes (`it.element`, `it.supplement`).

## Footnotes

See `styling-and-layout.md`. `#footnote[...]`, `#footnote(<label>)`.

## Bibliography and citations

```typ
As shown by @knuth and @knuth[p. 12], also #cite(<knuth>, form: "prose").  // prose: "Knuth (1968)"
// `cite` takes ONE key; consecutive @a @b are grouped automatically by the style.
#bibliography("refs.bib", title: [References], style: "ieee", full: false)
```

- **Sources**: BibLaTeX/BibTeX `.bib` or Hayagriva `.yml`/`.yaml`; can be an array (`("a.bib", "b.yml")`) or raw `bytes` (0.13+). Keys are labels: `@key`. A key may contain `: . - _`.
- **`cite` forms**: `"normal"` (default), `"prose"`, `"full"`, `"author"`, `"year"`, `none` (adds to the bibliography without showing a citation). Supplement via `@key[p. 12]`.
- **Styles** (`style:`): built-in CSL names such as `"ieee"` (default), `"apa"`, `"chicago-author-date"`, `"chicago-notes"` (footnote style), `"mla"` (0.15; `"modern-language-association"`), `"harvard-cite-them-right"`, `"american-chemical-society"`, `"american-medical-association"`, `"american-physics-society"`, `"nature"`, `"springer-basic-author-date"`, `"nlm-citation-sequence"` (renamed from `vancouver` in 0.15), `"cse-name-year"`, `"iso-690-author-date"` … or your own `.csl` file path/bytes. Old names (`vancouver`, `mla-8`, `council-of-science-editors*`) warn in 0.15. Browse styles at <https://typst.app/docs/reference/model/bibliography/>.
- **Multiple bibliographies (0.15)**: several `bibliography(...)` calls in one document; control which citations go where with `target:` (a selector, default `auto` = closest following/preceding bibliography containing the key) and numbering continuity via `group:` (`auto` shared, `none` isolated, or a string). Per-section references: `bibliography("refs.bib", title: none, target: selector(cite).within(here()), ...)` inside `context` (see docs example).
- `bibliography(full: true)` lists uncited works too.
- Titles: `title: auto` → localized "Bibliography"/"References"; `title: none` hides it (place your own heading). Heading level of the title follows `offset`; restyle with `#show bibliography: set heading(numbering: none)` / `#show bibliography: set text(9pt)`.
- Bibliography entry layout: `#show bibliography: set par(first-line-indent: 0em)`; for grid-based styles (numbered) the `enum`-like look comes from the style.
- Custom citation text: not directly; choose another CSL or use packages: `pergamon` (BibLaTeX-style control), `citegeist` (bib as dictionary), `alexandria` (older multi-bib; superseded in 0.15 by native support).
- Language of entries follows `text(lang:)` and the entry's `language` field.
- Check: bibliography requires at least one cite (or `full: true`) to show entries; unused `bibliography()` with no citations prints nothing.
- In `.bib` files: `month = 5` or `may` both work (0.15); BibLaTeX name options supported; `@online`, `@software`, `@thesis`, `@misc` fine; `url`, `doi` rendered as links by the style. Escape LaTeX accents are decoded (`{\"u}` → ü). Use `{Title in Braces}` to preserve case.

## Numbering, counters and supplements

- `numbering("1.", 3)` formats a number; every numbered element (`heading`, `page`, `figure`, `equation`, `footnote`, `enum`) takes `numbering:` (pattern or function). `counter(heading).display()`, `counter(figure.where(kind: image)).get()`. Details: `introspection.md`.
- `supplement:` is the word shown in refs (`auto`, `none`, content, or function `(element) => content`).

## Terms, quotes, paragraphs (semantics)

- `par` is a real element since 0.13 — only block-level contexts create paragraphs. `#set par(first-line-indent: ...)` affects only real paragraphs.
- `terms` (`/ Term: description`) → definition lists; `terms.item(term, desc)`.
- `smartquote` handles quote characters; disable with `#set smartquote(enabled: false)`; custom: `#set smartquote(quotes: (single: ("‘", "’"), double: ("“", "”")))`.

## Raw / code listings

```typ
#figure(caption: [Hello], kind: raw)[
  ```rust
  fn main() { println!("hi"); }
  ```
]
#show raw.where(block: true): it => block(fill: luma(245), inset: 8pt, radius: 3pt, width: 100%, it)
```

Custom highlight theme: `#set raw(theme: "my.tmTheme")` (path to a `.tmTheme`, bytes, or `none`).

Line numbers: `#show raw.where(block: true): it => grid(columns: (auto, 1fr), column-gutter: 8pt, row-gutter: 4pt, ..it.lines.map(l => (text(gray)[#l.number], l.body)).flatten())` or packages `codly`/`zebraw`. Show-rule `raw.line` exists for per-line tweaks. `read("script.py")` + `raw(..., lang: "python")` to include source files.

## Misc model facts

- Labels: `#heading[...] <x>` or `= Heading <x>`; labels in math: `$ ... $ <eq>`.
- `#set text(lang: "de")` localizes automatic words ("Abbildung", "Kapitel"...).
- Table/figure supplements in non-English: set `lang` and they follow.
- `document()` element in bundle export defines separate output files (experimental) — see `export-and-cli.md`.
- Hyperlinked PDF bookmarks are generated from headings (with numbering since 0.14). `heading(bookmarked: false)` hides one.
