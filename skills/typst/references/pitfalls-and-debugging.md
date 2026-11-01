# Pitfalls, diagnostics, and debugging

## Verification loop for agents

1. `typst compile main.typ 2>&1` — errors stop the build (exit 1); warnings don't. Read the first error first; later ones are often consequences.
2. Look at the output:
   - Visual: `typst compile main.typ 'p-{0p}.png' --ppi 80` then open/view the images (check overflow, clipped tables, wrong fonts, blank pages).
   - Text: `pdftotext -layout main.pdf -`, or HTML (`typst compile main.typ - -f html --features html 2>/dev/null`) for structure.
   - Structure: `typst eval --in main.typ 'query(heading).map(h => (level: h.level, page: h.location().page()))'`.
   - Pages: `typst eval` can't evaluate `context` itself, so export values from inside the document: `#context [#metadata(counter(page).final().first()) <pages>]` then `typst eval --in main.typ 'query(<pages>).first().value'` (or `pdfinfo main.pdf`).
3. Probe language behaviour without files: `typst eval 'repr((1, 2).sorted())'`, `typst eval 'type(auto)'`, `typst eval '"abc".matches(regex("[a-b]")).len()'`. Inside a document context: `printf '#metadata(1 + 2) <p>\n' | typst eval --in - 'query(<p>).first().value'`.
4. In-document debugging: `#repr(x)` (shows value/type), `#type(x)`, `#x.fields()` for content, `#raw(repr(x))`, `#assert(cond, message: "...")`, `#panic("..")` (0.15 prints strings as-is), `#show: it => { repr(it) }`. Add visible guides: `#set page(background: grid(...))`, `#set block(stroke: 0.5pt + red)` temporarily, `#box(stroke: red, inset: 0pt)[..]` to see boxes.
5. Run the repo's snippet checker: `python3 scripts/check-snippets.py doc.md`.
6. `typst compile ... --timings t.json` (Perfetto) for slow documents; see Performance below.

## Frequent errors (exact 0.15 messages) and fixes

| Message | Cause → fix |
| --- | --- |
| `error: unknown variable: ab` (in math) | multi-letter names are symbols in math → `a b`, `"ab"`, or `italic("ab")` |
| `error: unknown variable: f` | misspelt, not imported, or defined later/in another scope; `#let` must precede use |
| `error: expected function, found array` for `a[0]` | index with `a.at(0)` |
| `error: expected length, found integer` (+ hint) | lengths need units: `12pt`, `1em`, `0.5cm`; ints only for counts |
| `error: expected relative length or auto, found string` | `width: "3cm"` → `width: 3cm` |
| `error: unexpected argument: foo` | parameter doesn't exist/typo, or not a set-rule-able parameter; check `api-signatures.md` |
| `error: unexpected argument` / `missing argument: x` | wrong arity; `with()` partial application; spread `..args` |
| `error: variables from outside the function are read-only and cannot be modified` | closures can't mutate outer variables → use `fold`, loops in the same scope, `state`, `counter` |
| `error: can only be used when context is known` | wrap in `#context ...` (counter/state/query/measure/text.size) |
| `error: cannot join integer with string` | `.join()` needs strings/content → `arr.map(str).join(", ")` |
| `error: cannot add string and integer` / type mismatches | convert: `str(n)`, `int(s)`, `[#x]` |
| `error: expected content, found string`/`vice versa` | `[#s]` / `str(c)` / `eval(s, mode: "markup")` |
| `error: label `<x>` does not exist in the document` | label not attached (blank line, after `#let`, inside unlabeled block) or typo; `@x` where `x` is meant as a literal `@` → escape `\@` |
| `error: label `<x>` occurs multiple times` | duplicate labels; they must be unique |
| `error: cannot reference heading without numbering` | `#set heading(numbering: "1.")` or use `#link(<x>)[text]` / `@x[Intro]`-style supplement |
| `error: file not found (searched at …)` | path relative to the *current file*, `/path` relative to `--root`; no `..` above root; case-sensitive on Linux |
| `error: failed to load file (access denied)` / outside root | set `--root` to a common ancestor |
| `error: package not found (searched for @preview/x:ver)` | wrong name/version or offline: check `scripts/search-packages.py`, network, `--package-cache-path` |
| `error: maximum show rule depth exceeded` | show rule recreates its own element → use `it` or `block(it.body)`; use `set` instead |
| `error: maximum function call depth exceeded` | unbounded recursion → iterate |
| `error: unclosed delimiter` | missing `]`, `)`, `}`, `$` or a stray `*`/`_` marker |
| `error: the character `#` is not valid in code` | don't write `#` inside code mode |
| `error: expected expression` after `#` | stray `#` followed by space/symbol; escape `\#`; or inside code mode `#` |
| `error: this selector cannot currently be used with show` | `.within(...)`/`before/after` selectors are for `query`/counters only |
| `error: the document does not contain a bibliography` | `cite`/`quote(attribution: <key>)` used without `#bibliography(...)` |
| `error: label `<key>` does not exist in the document` for `@key` | citation key missing from the loaded `.bib`/`.yml`, typo, or no `bibliography(...)` loaded |
| `error: PDF/UA-1 error: missing alt text` / `missing document title` / `PDF/A-2a error: document contains an attached file` / `PDF/A-4 and PDF/UA-1 are mutually incompatible` | add `alt:`, `set document(title:)`; remove attachments (A-1/A-2) or use A-3/A-4f; pick compatible standards (see `export-and-cli.md`) |
| `error: CSL style "X" is not suitable for bibliographies` / `unknown style` | choose a bibliography style (not citation-only like `alphanumeric`) or supply a `.csl` |
| `error: html export is only available when --features html is passed` | add `--features html` |
| `warning: unknown font family: x` | font not installed → `typst fonts`, `--font-path`, check spelling; Typst falls back silently otherwise |
| `warning: document did not converge within five attempts` | feedback loop through counters/state/query; make dependents fixed-size; see `introspection.md` |
| `warning: … was ignored during HTML export` | element unsupported in HTML; wrap in `context target()` branches or `html.frame` |
| `warning: style X has been deprecated in favor of Y` | rename (CSL styles, symbols) |
| `error: condition is always true` | `while true` without side effects (compile-time guard); restructure |
| `error: number must be positive` | `heading(level: 0)`; levels start at 1 (the title uses `title`) |

## Gotchas by category

**Syntax / modes**
- `#f (x)` (space) is not a call; `#f(x)[body]` trailing content must follow immediately.
- `#let` with content in markup: `#let c = [text]` — no `#` inside.
- A paragraph ends with a blank line; a `#let` or `#set` line between paragraphs doesn't break it (use `#parbreak()`).
- `_` and `*` start emphasis; underscores inside words (`snake_case`) are OK; inside math `_` is subscript. Escape or wrap in raw: `` `snake_case` ``.
- `\` at end of line = line break; `\ ` before a space is escaped space. In code strings `"\n"` is a newline, `"\\"` backslash, `"\u{..}"` unicode.
- `//` inside URLs: auto-link handles `https://...`; in other text it starts a comment (write `https:/\/`).
- A reference swallows trailing label characters (`_ - : .` inside a name): `_see @a._` fails (`<a._>` is read as the label) → put markers outside (`_see_ @a.`) or write `#ref(<a>)`/`@a[]`; a trailing `.` or `,` alone is fine.
- `@` in email-like text triggers references: write `user\@example.com` or `#link("mailto:...")`.
- `$` in prices: `\$5` or `"$5"` in a string; `<` `>` in text: escape `\<` to avoid label start.
- Apostrophes/quotes become smart quotes; use `\'` / `\"` for straight.

**Scoping and order**
- `set`/`show` affect only what comes after, inside the current block; wrap local style changes in `[#set text(red); text]` or `#[...]`.
- Included files cannot change the includer's styles. Imports at the top of a file are fine; imported names are lexically visible after the import.
- `show: tpl.with(...)` must be at the top level and **before** the content; any content before it bypasses the template.

**Layout**
- Overfull tables/boxes silently overflow: set `columns: (1fr, ..)`, `width: 100%`, or wrap text.
- Images larger than the page are clipped/overflow → `width: 100%`/`fit`.
- `v(1fr)`/`h(1fr)` don't work in `auto`-sized containers.
- `block(breakable: false)` on tall content causes jumps to the next page / overflow; `sticky: true` for headings.
- Page numbering shows "1" only if `numbering` is set; `#set page(numbering: "1")` before the first page content (otherwise a new page is created).
- Setting `page` mid-document creates a page break; `#set page(margin: ...)` right after content breaks the page — use `#page(margin: ..)[...]` for local pages or place early.
- `place` doesn't take space; reserve with `v` or use `float: true` figures.
- Footnotes inside tables/grids/`block`s may not appear (0.15 improved, still prefer footnotes in running text).
- Baseline change in 0.15: boxes/equations/list items align by first-line baseline; remove old manual `baseline:` hacks.

**Text**
- Missing glyph boxes (□/tofu) → font lacks the script → add fallback fonts: `#set text(font: ("Libertinus Serif", "Noto Sans CJK SC", "Noto Color Emoji"))`.
- Wrong hyphenation/quotes → set `lang`/`region`.
- Ligatures breaking in code → `#show raw: set text(ligatures: false)`.
- Justified text with big gaps → `par.justification-limits`, `hyphenate: true`, narrower measure, `linebreaks: "optimized"`.
- Small caps/old-style numerals need font support (`features: ("smcp",)`/`number-type: "old-style"`).

**Math**
- See `math.md`. Never use LaTeX macros; no `\left`; no `\\` ending lines except in aligned/multiline equations (`\` alone).

**Data / strings**
- All CSV cells are strings; convert before math/sorting (`int(c)`, `float(c)`). JSON null → `none`.
- `str.at(i)` is by **byte** index; use `.clusters()` for characters; non-ASCII breaks naive slicing.
- Array/dict values are immutable *values*: `let b = a; b.push(1)` doesn't change `a`.
- Dict ordering preserved; keys are strings; `dict.at("a b")` for odd keys.
- `calc.rem` vs `calc.rem-euclid`; `/` makes floats; `calc.quo` int division.
- Regexes: Rust `regex` crate syntax; no lookaround/backreferences.

**Packages**
- Version drift: package pinned to old API may break on new compiler; read changelog; try newer version.
- Show-rule packages must be initialized once at the top (`#show: codly-init`).
- Packages cannot read files from your project unless you pass bytes/paths.
- `@preview` downloads need network the first time; CI should cache.

**Export**
- PNG/SVG one file per page — use `{p}` placeholder if >1 page.
- `--pages` uses physical page numbers.
- HTML/bundle are experimental → output and APIs may change.
- Reproducibility: `datetime.today()` and PDF dates follow compile time; set `--creation-timestamp`/`SOURCE_DATE_EPOCH`.
- PDF/A/UA constraints: see `export-and-cli.md`.

## Performance

- Use `typst compile --timings t.json` (experimental; load in <https://ui.perfetto.dev>) and look at layout/eval hotspots.
- Typical slow spots: huge `table`s (thousands of cells; set explicit `columns` widths, avoid `auto` columns, simplify `fill/stroke` functions), many `query()`/`counter.final()` calls (cache once with `let`), heavy `context` in `show` rules of frequent elements, large SVG/PNG images (downscale), packages doing heavy layout (cetz with thousands of elements), text show rules with big regexes, runaway convergence iterations (5 passes max).
- Avoid computing the same thing per cell; precompute arrays; use `array.fold`/`map` instead of manual loops with `+=` on big arrays (quadratic).
- Split work across `include`d files — comemo caching is function-level and incremental; `typst watch` reuses unchanged results.
- Large documents: `--jobs N`; fonts: `--ignore-system-fonts` + `--font-path` makes lookups faster and reproducible.

## When to stop and ask / check docs

- If the answer depends on a package version or an experimental feature, state the version/flag used.
- If a behaviour differs from this skill, trust the compiler (`typst eval` probes), then the official docs at <https://typst.app/docs/> (reference, guides, changelog).
