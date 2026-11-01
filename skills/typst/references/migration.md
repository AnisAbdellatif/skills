# Migration: LaTeX, Markdown, Word, and older Typst versions

## LaTeX → Typst concept map

| LaTeX | Typst |
| --- | --- |
| `\documentclass{article}` + packages | `#set` rules, a template function, `#import "@preview/pkg:ver"` |
| `\title \author \date \maketitle` | `#set document(title:, author:)` + `#title()` or a template (`#show: tpl.with(title: ...)`) |
| `\section{X}` `\subsection` | `= X`, `== X` (`#heading(level: 3)[X]`) |
| `\label{a}` `\ref{a}` `\eqref` `\cref` | `<a>` after the element, `@a` (supplement automatic: "Figure 1", "Equation (1)") |
| `\textbf{x}` `\emph{x}` `\texttt{x}` | `*x*` / `#strong[x]`, `_x_` / `#emph[x]`, `` `x` `` / `#raw("x")` |
| `\textsc \underline \textsuperscript` | `#smallcaps[]` `#underline[]` `#super[]` / `#sub[]` |
| `\begin{itemize}`/`enumerate`/`description` | `- `, `+ `, `/ Term: desc` |
| `\begin{figure}\includegraphics\caption\end{figure}` | `#figure(image("x.png", width: 70%), caption: [..]) <fig:x>` |
| `\begin{table}\begin{tabular}` | `#figure(table(columns: 3, ..), caption: [..])`; `\multicolumn` → `table.cell(colspan: n)`; `\hline` → `table.hline()`; booktabs → `stroke: none` + hlines |
| `$..$`, `\[..\]`, `equation`, `align` | `$..$`, `$ .. $`, `$ .. $ <eq>` with `&` and `\` for alignment |
| `\frac{a}{b}` `\sqrt[3]{x}` `\sum_{i=1}^{n}` | `a/b` or `frac(a, b)`, `root(3, x)`, `sum_(i=1)^n` |
| `\left( \right)` `\big` | auto-sizing delimiters; `lr(( ))`, `lr(size: #150%, ..)` |
| `\mathbb{R} \mathcal{L} \mathfrak{g} \mathbf{x} \mathrm{d}` | `RR`/`bb(R)`, `cal(L)`, `frak(g)`, `bold(x)`, `upright(d)` / `dif` |
| `\text{if}` / `\operatorname{rank}` | `"if"` / `op("rank")` |
| `\begin{matrix}` `pmatrix` `bmatrix` `cases` | `mat(1,2;3,4)`, `mat(delim: "[", ..)`, `cases(..)` |
| `\newcommand{\R}{\mathbb{R}}` | `#let R = $bb(R)$` then `$ x in #R $`; with args: `#let f(x) = $...#x...$` |
| `\newtheorem` | `theorion`/`ctheorems`/`frame-it` packages |
| `\bibliography{refs}`, `\cite{k}`, `\citep \citet` | `#bibliography("refs.bib")`, `@k`, `@k` / `#cite(<k>, form: "prose")` (author-year via `style: "apa"`) |
| `\footnote{x}` | `#footnote[x]` |
| `\tableofcontents \listoffigures` | `#outline()`, `#outline(target: figure.where(kind: image))` |
| `\newpage \clearpage` `\vspace{1em}` `\hspace` | `#pagebreak()`, `#v(1em)`, `#h(1em)` |
| `\centering` `\raggedright` | `#align(center)[..]`, `#set par(justify: false)` |
| `\usepackage[margin=2cm]{geometry}` | `#set page(margin: 2cm)` |
| `\usepackage{fontspec}` `\setmainfont` | `#set text(font: "...")` |
| `\usepackage{microtype}` | on by default (+ `par.justification-limits`) |
| `\usepackage{hyperref}` | links are always live; `#link(url)[..]`; `#show link: set text(blue)` |
| `\usepackage{listings}/minted` | `` ```lang `` raw blocks (+ `codly`/`zebraw`) |
| `\usepackage{tikz}/pgfplots` | `cetz`, `fletcher`, `lilaq` |
| `\usepackage{siunitx}` | `unify`, `zero` |
| `\usepackage{biblatex}` | native bibliography + CSL; `pergamon` for biblatex-style control |
| `\usepackage{babel}` | `#set text(lang: "de")` |
| `\usepackage{xcolor}` | `rgb("#...")`, `red.lighten(40%)`, `text(fill: ..)` |
| `\usepackage{multicol}` | `#set page(columns: 2)`, `#columns(2)[..]` |
| `\usepackage{fancyhdr}` | `#set page(header: .., footer: ..)` + `hydra` |
| `\usepackage{beamer}` | `touying` / `polylux` |
| `\usepackage{enumitem}` | `#set enum(...)`, `#set list(...)`, `itemize`/`numbly` |
| `\usepackage{subcaption}` | `subpar` |
| `\usepackage{glossaries}` | `glossarium`, `acrostiche` |
| `\usepackage{algorithm2e}` | `lovelace`, `algorithmic`, `algo` |
| `\input{file}` `\include` | `#include "file.typ"` (content) or `#import "file.typ": *` (definitions) |
| `\def`, macros with `#1` | `#let f(a, b) = [...]` (functions are first class) |
| counters `\newcounter \stepcounter` | `counter("name")`, `.step()`, `.update()`, `.display()` in `context` |
| `\ifthenelse`, `\if` | `#if cond [..] else [..]` |
| `\foreach`/loops | `#for x in array [..]` |
| `\renewcommand\thesection{..}` | `#set heading(numbering: "..")` or function numbering |
| `latexmk` | `typst watch` (compile in milliseconds, no multi-pass) |
| `.aux`/`.toc` | none: Typst resolves references in iterations automatically |

Differences worth knowing:
- No separate "preamble": all configuration is `set`/`show`/`let`, may appear anywhere and is scoped.
- Compilation is incremental and fast; error messages point to source with hints.
- Fonts: OpenType/TrueType only (no Type1/METAFONT); default Libertinus Serif. For a LaTeX look use `New Computer Modern` (embedded) with `#set par(justify: true, leading: 0.55em)`, `#set text(font: "New Computer Modern", size: 10pt)`, `#set page(margin: (x: 1in, y: 1in))` and `#set par(first-line-indent: 1.5em, spacing: 0.55em)`.
- Math is similar but writes without backslashes and with multi-letter symbol names; for pasted LaTeX math use `mitex` (`#mitex(`\frac{a}{b}`)`) or pandoc.
- No `\newcommand`-style text substitution: macros are functions returning content. Arguments in math need `#`: `$ #f(x) $` or call directly `$ f(x) $` only if `f` is in math scope (it is, for functions defined with `#let`).
- Tables/figures don't "float" unless `placement:` is set on `figure`.
- Bibliography: Typst reads `.bib` (BibLaTeX subset) and `.yml` (Hayagriva); styles are CSL.

### Convert existing LaTeX

```bash
pandoc paper.tex -s -o paper.typ --wrap=none        # then fix tables/figures/macros by hand
pandoc paper.md -s -o paper.typ                       # Markdown → Typst
pandoc paper.tex -t typst --citeproc=false ...         # leave citations as @keys
pandoc input.md --pdf-engine=typst -o out.pdf          # use Typst as PDF engine (+ -V papersize=a4 / --template)
```

Post-conversion checklist: labels/refs (`<>`/`@`), figures with `width`, math macros, `\cite` → `@`, bibliography file, packages replaced (`cetz` etc.), fonts, headings numbering, unusual environments. `mitex` can embed leftover LaTeX math verbatim.

## Markdown → Typst

| Markdown | Typst |
| --- | --- |
| `# H1`, `## H2` | `= H1`, `== H2` |
| `**b**` `*i*` | `*b*` `_i_` |
| `` `c` `` and fences | same |
| `- item`, `1. item` | `- item`, `+ item` (numbers → `+`; explicit: `1. item` also works in Typst) |
| `[t](url)` | `#link("url")[t]` (bare URLs auto-link) |
| `![alt](f.png)` | `#image("f.png", alt: "alt")` (or in `figure`) |
| `> quote` | `#quote(block: true)[..]` |
| `---` | `#divider()` (0.15) or `#line(length: 100%)` |
| tables `\|a\|b\|` | `#table(columns: 2, [a], [b])` or `tablem` package |
| footnotes `[^1]` | `#footnote[..]` |
| HTML | no equivalent; use Typst elements |

In-document Markdown: `#import "@preview/cmarker:0.1.10"; #cmarker.render(read("doc.md"), scope: (image: (path, alt: none) => image(path, alt: alt)))`.

Markdown→Typst→PDF is a good pipeline for docs sites (`pandoc`, `quarto format: typst`, `mdbook-typst`).

## Word / HTML → Typst

`pandoc in.docx -o out.typ` (images extracted with `--extract-media`), `pandoc in.html -o out.typ`. Typst → Word: `pandoc` from Markdown or HTML export, or typst→docx converters (lossy). Prefer delivering PDF.

## Upgrading older Typst code

| If you know… | Changes that matter |
| --- | --- |
| ≤ 0.10 | `style(styles => ...)`, `locate(loc => ...)`, `layout`-less `measure` and callback-style `counter.display` → `context` (`style` no longer exists) |
| 0.11–0.12 | `context` introduced (0.11); `#set page(footer: context ...)`; function `style` removed; `box/block` fixed; `pattern` introduced (0.12; renamed `tiling` in 0.13); native `table` gained `table.cell`/`header`/`footer`/`hline`/`vline` so `tablex` is no longer needed |
| 0.13 | `par` vs inline distinction (first-line-indent only on real paragraphs; add `all: true`), new `outline` API (`outline.entry`), `curve` replaces `path`, image `source`/bibliography `sources` rename, bytes accepted in loaders, `.decode` deprecated, plugin API rewritten (`plugin("x.wasm")` module), `pdf.embed`, `enum.reversed`, `ref(form: "page")`, `document.description`, Greek numbering, single-letter math strings not italic |
| 0.14 | Tagged accessible PDF by default; `title` element; `pdf.attach` (renamed), PDF/A standards; PDF as image; character-level justification (`justification-limits`); multi-level table headers; typed HTML; `frac.style`; `--pdf-standard` values `a-2b`, `ua-1`…; `std` access |
| 0.15 | **Removed**: `path`, `pattern`, `pdf.embed`, `*.decode`, `typst query`, backslash paths. **Changed**: baseline of boxes/blocks/list items/equations, math `class` non-recursive, delimiters callable, `lr`/`stretch` ratio resolution, calligraphic letterforms (`stylistic-set: 6` for the old), variable fonts naming, HTML paragraph rules & minified output, `--timings` needs filename, `text.features`/`array.slice`/`str` stricter, symbol renames (warnings), CSL style renames (warnings). **Added**: `within` selector, `divider`, file `path` type, multiple bibliographies, bundle export, spot colors, `list.marker-align`, `eval` CLI, `counter.display(at:)`, `dict.map/filter`, `range(inclusive:)`, `int.min/max`, `int(base:)`, `calc.asinh/acosh/atanh/erf`, `page(bleed:)`, multi-standard PDF |

Polyfill/version gate pattern:

```typ
#let tile = if "tiling" in std { std.tiling } else { std.pattern }
#if sys.version < version(0, 15, 0) { /* old path */ } else { /* new path */ }
```

Check removals quickly: `grep -nE '\b(path\(|pattern\(|pdf\.embed|\.decode\()' *.typ`, and compile with `typst compile` to see deprecation warnings (symbols/styles) before they become errors.
