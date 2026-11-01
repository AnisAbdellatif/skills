# Introspection: context, counters, state, query, locations

Typst compiles in **iterations** until the layout converges (the document "knows" itself). Anything that depends on where/what the document is — style values, counters, page numbers, other elements — must be read inside `context`.

## `context`

```typ
#context text.size                       // style at this point
#context text.lang                       // current language
#set text(14pt)
#context [Size is #text.size]            // 14pt (reads style *at the call site*)

#let word-count-heading = context {
  let n = query(heading).len()           // query needs context
  [This document has #n headings.]
}
#word-count-heading
```

Rules
- `context expr` returns **content**; you can't use its result in non-context computation. Compute inside the context block and display there.
- Inside a function: `let f() = context { ... }` is the usual pattern for helpers needing context.
- `here()`, `locate(selector)`, `counter(...).get()/at()/final()`, `state(...).get()/at()/final()`, `query(...)`, `measure(...)`, `length.to-absolute()`, `text.size`, `par.leading` etc. all require context.
- `set` rules affect later content, not the already-evaluated context.
- Converge issues (0.15): if values oscillate between iterations (e.g. a counter value changing the layout that determines the counter), Typst warns "layout did not converge within 5 attempts" with a detailed diagnostic. Avoid feedback loops (e.g. displaying `final()` of something that depends on the displayed text's length).
- A label cannot be attached to a `context` block to be queried; label the element inside.

### Context details worth remembering

- **Nested contexts see the innermost context**: in `#context [ #set text(lang: "fr"); #text.lang \ #context text.lang ]` the first read ignores the `set` (it was evaluated in the outer context), the nested one sees it. Place the `context` *after* the rules whose effect you want to observe (e.g. inside the template, not around it).
- A context expression is **opaque, reactive content**: `#let value = context text.lang` can be reused; each use resolves in its own surroundings, and its body may be evaluated zero, one or many times.
- Context is **implicit** in show rules (style context always; location context only for show rules on locatable elements such as headings, figures, labels) and in outline entries — so `show heading: it => counter(heading).display()` needs no `context`, while a top-level `#counter(heading).get()` does.
- Even `counter(x).at(<label>)` needs context: its value can change between compiler iterations.
- `locate(<label>).position()` / `.page()` give physical placement; `here().page()` is the physical page, `counter(page).get()` the *logical* page number (they differ after `counter(page).update(..)`).
- Typst re-runs the document until it converges (max 5 passes). Many stateful updates or position-dependent layout can need several passes, and non-convergence prints `warning: document did not converge within five attempts`.

## Counters

```typ
#context counter(page).display()         // current page number, formatted (display needs context too)
#context counter(page).get().first()     // int
#context counter(page).final().first()   // total pages
#counter(page).update(1)                 // restart
#counter(heading).update(0)
= Intro <intro>
#counter("mycounter").step()             // custom named counter; step() / update(n) / update(n => n + 1)
#context counter("mycounter").display("A.1")  // with numbering; display(at: <loc>) in 0.15
#context counter(heading).at(<intro>)    // value at a label/location (array)
#context counter(figure.where(kind: image)).get()  // kind-specific figure counter
#counter(math.equation).update(0)
```

- Built-in counters: `page`, `heading`, `figure` (per `kind`), `math.equation`, `footnote`, `enum` items (internal), line numbers. `counter(page)` counts per **document**.
- A counter value is an **array** of ints (`(2, 3)` for heading 2.3). `.get().first()` gets the first.
- `counter.display(numbering)` auto-selects the element's numbering (improved in 0.15) — with no numbering given it uses the counted element's numbering.
- Update only has effect if it appears in the layout flow (it's content! `#counter(x).step()` places an invisible element).
- Custom numbered items: 
```typ
#let task = counter("task")
#let todo(body) = {
  task.step()
  block(context [*Task #task.display()*: #body])
}
#todo[Write skill] #todo[Test skill]
```

## State

```typ
#let notes = state("notes", ())                       // key, initial value
#notes.update(l => l + ("first",))                     // functional update
#notes.update(("a",))                                  // direct set
#context notes.get()                                   // current (array)
#context notes.final()                                 // value at end of doc
#metadata(none) <here-mark>
#context notes.at(<here-mark>)                        // at a label/location
```

State updates are ordered by position in the document (not evaluation order). Use for: glossaries, "seen" flags, collecting data for a list at the end, mode switches (`state("mode", "body")`), appendix numbering. State functions must be **pure** (same input → same output) since they may be re-run.

## Query

```typ
#context query(heading).map(h => h.body)                       // all headings
#context query(heading.where(level: 1))                         // filter
#context query(<my-label>)                                      // label selector
#context query(figure.where(kind: image)).len()
#context query(selector(heading).after(here()))                 // things after here
#context query(selector(heading).before(here()))                // headings before this point
#context query(heading.where(level: 2).within(<appendix>))     // 0.15: only descendants of matching ancestors
#context query(selector(heading).or(figure))
```

- Returns an array of elements; read fields (`it.body`, `it.level`, `it.numbering`, `it.caption`), `it.location()` gets the location (for `counter.at(loc)`, `link(loc)`, `page`).
- Page of an element: `loc.page()`; display with numbering: `counter(page).at(loc)` / `numbering(loc.page-numbering(), loc.page())`; position: `loc.position()` → `(page, x, y)`.
- Limit queries: don't call `query` in a hot loop; cache results in a `let`.

### Running headers (chapter title in header)

```typ
#set page(header: context {
  let hs = query(selector(heading.where(level: 1)).before(here()))   // last heading before this page
  let page-start = counter(page).get().first()
  if hs.len() > 0 and counter(page).get() != counter(page).at(hs.last().location()) {
    align(right, emph(hs.last().body))     // no header on the chapter's first page
  }
})
= Intro
#lorem(300)
= Next
#lorem(300)
```

(`hydra` package implements this robustly.)

### Table of figures / custom indexes

```typ
#context {
  let figs = query(figure.where(kind: image))
  for f in figs {
    let loc = f.location()
    [#link(loc)[Figure #numbering("1", ..counter(figure.where(kind: image)).at(loc))]: #f.caption.body #h(1fr) #loc.page() \ ]
  }
}
```

`#outline(target: figure.where(kind: image))` is built-in; use `query` for bespoke layouts. Dotted leaders: `box(width: 1fr, repeat[.])`.

## Metadata

`#metadata(value) <label>` stores any value invisibly; `query(<label>).first().value` reads it. Used for: exporting data via `typst eval --in doc.typ 'query(<label>)'`, pass values between pages/sections, store config.

```typ
#metadata((version: "1.0", authors: ("A", "B"))) <meta>
#context query(<meta>).first().value.version
```

Label placement: the label must follow `metadata(...)` directly (not a `context` block).

## Locations

`here()` (in context) gives the current `location`; `locate(<label>)` resolves a label that matches exactly one element; locations support `.page()`, `.position()`, `.page-numbering()`; they are valid args to `link`, `counter.at`, `state.at`.

```typ
#context {
  let target = locate(<end>)
  [Last page: #target.page()]
}
#lorem(50)
#metadata(none) <end>
```

## Measuring and layout

```typ
#context {
  let s = measure([Hello world], width: 5cm)    // content measured with current styles
  s.width
}
#layout(size => [Container is #size.width wide])   // only inside containers with known width
#context [#(1em).to-absolute()]
```

`measure` returns `(width, height)`; `layout(size => ...)` supplies `size` (width/height may be lengths); use inside `block`/`box` for fitted text: shrink text until it fits by looping with `measure`.

## Selectors cheat sheet

`heading`, `heading.where(level: 1, outlined: true)`, `<label>`, `selector(heading).or(figure)`, `.and(...)`, `.before(loc, inclusive: false)`, `.after(loc)`, `.within(selector)` (0.15, query only), `regex(..)` / string (show rules only), `figure.where(kind: table)`, `raw.where(block: true)`, `text.where(...)` no.

## Multi-pass workflows from the CLI

```bash
# count pages/headings → feed back into the next build
# main.typ contains: #context [#metadata(counter(page).final().first()) <pages>]
N=$(typst eval --in main.typ 'query(<pages>).first().value')
typst compile main.typ --input total=$N
typst eval --in main.typ 'query(heading).map(h => (level: h.level, page: h.location().page()))' --pretty
```

`typst eval --in file.typ '<expr>'` evaluates in the document (it can `query`, but `counter`/`state`/`here` need `context`, whose result can't be printed — export such values with `metadata` first) and prints JSON (or YAML via `--format yaml`); it replaces the removed `typst query` (`typst eval --in x.typ 'query(<l>)'`). Add `--target html` to introspect HTML export.

## Pitfalls

- "can only be used when context is known" → wrap in `context`.
- Non-convergent layouts (warning): e.g. header text depending on total pages that changes layout. Make the dependent element fixed size (`box(width: 2cm)`).
- `counter(...).get()` returns an array — don't compare with ints directly (`.first() == 1`).
- Label on `context` doesn't work; label the element inside.
- `state` updates inside `show` rules or functions executed multiple times are fine only if idempotent in position.
- Queries are executed **after layout** so they see all pages; they see elements even hidden or out of page.
- Bundle export: introspection spans all documents of the bundle, except the page counter.
