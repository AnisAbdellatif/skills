# Slides and presentations

Options: **Touying** (`@preview/touying`, most capable; verified here with 0.8.0 on Typst 0.15.1), **Polylux** (`@preview/polylux`, simpler `#slide[...]` functions), small wrappers (`typslides`, `diatypst`, `minideck`, `presentate`), or **plain Typst** (see `examples/slides-plain.typ`). 0.8.0 requires Typst ≥ 0.15; older Touying (0.6/0.7) APIs differ slightly (`touying-recall(subslide:)` → `subslides:`, `semi-transparent-cover` deprecated, `show-bibliography-as-footnote` is now boolean, `magic.bibliography()` removed).

## Touying quick start

```typ
#import "@preview/touying:0.8.0": *
#import themes.metropolis: *          // aqua, default, dewdrop, metropolis, simple, stargazer, university, article(0.8)

#show: metropolis-theme.with(
  aspect-ratio: "16-9",               // or "4-3"
  footer: self => self.info.institution,
  config-info(
    title: [Title], subtitle: [Subtitle], author: [Author],
    date: datetime.today(), institution: [Institution],
  ),
  config-common(slide-level: 2),      // heading level that creates slides
)
#set text(size: 20pt)

#title-slide()
== Outline <touying:hidden>
#components.adaptive-columns(outline(title: none, indent: 1em))

= Section                             // level 1 → section (slide with new-section title)
== Slide with pauses                  // level 2 → slide
First #pause second #pause third.

== Alternatives and columns
#slide(repeat: 3, self => [
  #let (uncover, only, alternatives) = utils.methods(self)
  Subslide #self.subslide: #uncover("2-")[from 2] #only("3")[only at 3]
])
#slide(composer: (1fr, 1fr))[Left column][Right column]

#show: appendix                       // freeze slide counters for backup slides
= Appendix
== Extra
Backup.
```

Compile like any document: `typst compile slides.typ` (one PDF page per subslide unless `handout: true`).

## Structure rules

- **Headings make slides**: `=` section, `==` slide title (default `slide-level: 2`); with `slide-level: 3`, `=` section, `==` subsection, `===` slide. Content between a heading and the next heading is the slide body. `---` or `#pagebreak()` splits slides without a new heading. `== <touying:hidden>` makes a slide without visible title (also clears the heading context). Labels `<touying:unnumbered>`, `<touying:unoutlined>`, `<touying:unbookmarked>` tune headings.
- **Custom slides**: `#slide[...]` (content) or `#slide(repeat: n, self => [...])` (callback; inside use `utils.methods(self)` to get `uncover`, `only`, `alternatives`); `#empty-slide[...]` has no header/footer. Always wrap own slide functions with `touying-slide-wrapper`.
- **Numbering/TOC**: `#set heading(numbering: "1.1")`, `#show heading.where(level: 1): set heading(numbering: "1.")` or `numbly("{1}.", default: "1.1")`; progress outlines `components.progressive-outline`, `components.custom-progressive-outline`; `components.adaptive-columns(outline(...))` fits the TOC.
- **Configuration functions** (pass to the theme `.with(...)` or `touying-set-config`): `config-info(title:, subtitle:, author:, date:, institution:)`, `config-common(slide-level:, handout:, datetime-format:, new-section-slide-fn: none | fn, show-notes-on-second-screen:, show-only-notes:, notes-fn:, show-bibliography-as-footnote:)`, `config-page(margin:, header:, footer:, background:, fill:)` (use instead of `set page`), `config-colors(primary:, secondary:, neutral-lightest: …)`, `config-methods(init:, alert:, cover:)`, `config-store(…)`. Global `set text(...)`/`show` rules go before or after the `#show: theme.with(...)` line; theme-specific globals live in `config-methods(init: (self: none, body) => {...; body})`.
- **Multi-file decks**: `globals.typ` (imports theme, exports `#let slides = ...` or config), `main.typ` (`#import "globals.typ": *`, `#show: theme.with(...)`, `#include "sections/a.typ"`), content files without their own `show`. Use `#import` for definitions and `#include` for slide content to avoid cycles.

## Animations

| Need | Use |
| --- | --- |
| Reveal step by step | `#pause`, `#meanwhile` (parallel track), `#pause` inside lists/math/`touying-reducer`s |
| Reserve space and show on certain subslides | `#uncover("2-")[...]`, `uncover("1,3-")` |
| Show/remove from layout | `#only("2")[...]` |
| One of several | `#alternatives[a][b][c]`, `alternatives-match`, `alternatives-fn`, `alternatives-cases` |
| Highlight | `#effect(text.with(fill: red), "2-")[...]` |
| Relative jumps/waypoints | `#jump(n, relative: true)`, `#waypoint(<w>)`; `item-by-item` helper for lists |
| Recall a slide/element | `#touying-recall(<label>, subslides: auto)` (0.8) |
| Animate cetz/fletcher | `#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))`, `#let fletcher-diagram = touying-reducer.with(reduce: fletcher.diagram, cover: fletcher.hide)` then `(pause,)` inside the drawing |
| Handout (last subslide only) | `config-common(handout: true)` |
| Cover style | default `hide`; `config-methods(cover: utils.alpha-changing-cover)` / `utils.color-changing-cover` (0.8; `semi-transparent-cover` deprecated); lists need `cover: (self: none, body) => box(scale(x: 0%, body))` to hide markers |

Pitfalls: `#pause` inside `context`/show-rule output may not register (use callback-style `slide(repeat:)`); in 0.8 `#pause` after `uncover/only/alternatives` no longer skips reserved subslides; mixed `pause` + `only` in one slide needs consistent subslide counts — set `repeat` explicitly.

## Speaker view, notes, pdfpc, handouts

- `#speaker-note[...]` / `#pdfpc.speaker-note("text")` attach notes. `config-common(show-notes-on-second-screen: right)` doubles the page for a presenter view; `config-common(show-only-notes: true)` renders notes; panel customizable with `notes-fn` (0.8).
- `pdfpc` (presenter console): `#pdfpc.config(duration-minutes: 30, note-font-size: 12, …)`; export the `.pdfpc` sidecar with (0.15) `typst eval --in slides.typ 'query(<pdfpc-file>).first().value' > slides.pdfpc` (old `typst query` is gone). `pympress` and `typst-preview` also work.
- Fit content: `utils.fit-to-height(1fr)[BIG]`, `utils.fit-to-width(1fr)[title]` (`grow`, `shrink`, `width`, `prescale-width` options).
- Page layout: slides are normal pages (`paper: "presentation-16-9"`); headers/footers span full width with negative padding; margins `(x: 4em, y: 2em)`; `header-ascent: 0em`.

## Integrations

`cetz`, `fletcher` (via `touying-reducer`), `theorion` (theorem boxes: `#import "@preview/theorion:0.6.0": *; #import cosmos.clouds: *; #show: show-theorion`), `codly` (2.x API), `mitex` (`touying-mitex`), `pinit` (pinned annotations over text/math), `numbly` (heading numbering), `zebraw`, equations with `touying-equation("a + pause b")` or `#pause` in `$ ... $`.

## Article mode (0.8)

The same source can compile to a flowing document (animations collapse to final state): use the `article` theme (`#import themes.article: *`) — see the package manual for options.

## Polylux (alternative)

```typ-x
#import "@preview/polylux:0.4.0": *
#set page(paper: "presentation-16-9")
#slide[
  = Title
  Content #pause more content
]
```

Polylux has `slide`, `pause`, `uncover`, `only`, `one-by-one`, `later`, `line-by-line`, `polylux-slide`, theme packages, and `pdfpc` support. Choose Touying when you want themes, sections, handouts, and heading-driven slides.

## Plain Typst slides

Use `#set page(paper: "presentation-16-9")`, one `= Heading` per slide with `#show heading.where(level: 1): it => { pagebreak(weak: true); it }`, `#set text(size: 24pt)`, and PDF viewers in full-screen. See `examples/slides-plain.typ`. Animations aren't available without packages (one page per step: duplicate content or use a loop generating pages).
