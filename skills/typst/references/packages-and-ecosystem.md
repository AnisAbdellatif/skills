# Packages and ecosystem (snapshot of Typst Universe, 2026-10-28)

Universe has ~1,700 packages (≈260 thesis templates, ≈250 report, ≈150 paper, ≈130 presentation, ≈90 CV). Versions below were the latest in the index on the snapshot date — **re-check** with `python3 scripts/search-packages.py <name>` (writes/reads a 1-day cache) before pinning. Always import with `#import "@preview/<name>:<version>"`. Many packages are 0.x with breaking API changes: read the matching manual/README.

## Pick by task

| Task | Packages (version at snapshot) |
| --- | --- |
| Drawing / diagrams | `cetz` 0.5.3 (TikZ-like canvas), `fletcher` 0.5.8 (nodes & arrows, commutative diagrams), `diagraph` 0.3.8 (Graphviz), `pintorita` (sequence/ER diagrams), `mmdr`/`oxdraw` (Mermaid), `syntree` (parse trees), `treet` (tree lists), `curryst` (inference rules), `quill` (quantum circuits), `tiptoe` (arrow tips), `alchemist` (skeletal formulas) |
| Plots / charts | `lilaq` 0.6.0 (scientific, own data model), `cetz-plot` 0.1.4, `plotsy-3d`, `neoplot` (gnuplot) |
| Slides | `touying` 0.8.0 (themes, animations, `pause`/`meanwhile`; most used), `polylux` 0.4.0, `typslides`, `diatypst`, `minideck`, `presentate`; speaker notes via `pdfpc`/`pympress`; `pinit` for pinned annotations |
| Theorems / proofs | `theorion` 0.6.0, `ctheorems` 2.0.0, `great-theorems`, `frame-it`, `lemmify`, `thmbox` |
| Code blocks | `codly` 2.0.0 (line numbers, annotations, diffs), `zebraw` 0.6.3, `sourcerer`; built-in `raw` + `show` for simple cases |
| Boxes / callouts | `showybox` 2.0.4, `gentle-clues` 1.3.1, `colorful-boxes`, `catppuccin` (palette) |
| Math helpers | `physica` 0.9.8, `mitex` 0.2.7 (LaTeX math → Typst), `equate` 0.3.3 (equation numbering/breaks), `quick-maths` (shorthands), `mannot` (annotate math), `unify`/`zero` (units/numbers), `typsium`/`whalogen`/`chem-par` (chemistry) |
| Algorithms / pseudocode | `lovelace` 0.3.1, `algorithmic` 1.0.7, `algo` 0.3.6 |
| Tables | `tablem` (markdown-like), `tblr` (tabularray-like), `rowmantic`, `pillar`, `tabut`, `rexllent` (xlsx→table); native `table` + `table.cell` usually suffices (`tablex` is deprecated: use built-in) |
| Figures | `subpar` 0.2.2 (subfigures), `wrap-it` (text wrapping), `i-figured` (per-section numbering), `headcount` (counters from headings) |
| Glossary / index / acronyms | `glossarium` 0.5.10, `acrostiche` 0.7.0, `in-dexter` 0.7.2 |
| Bibliography | native `bibliography`; `pergamon` 0.8.0 (BibLaTeX-style), `citegeist` (BibTeX as dict), `alexandria` (legacy multi-bib; now native in 0.15) |
| Headers/footers | `hydra` 0.6.3 (running headings), `chic-hdr` |
| Outlines | `outrageous` 0.4.1 |
| Margin notes | `marginalia` 0.3.1, `drafting` (comments, todo notes), `typearea` (KOMA-like) |
| Lists / checklists | `cheq` 0.4.0 (task lists), `numbly` 0.1.0 (per-level numbering), `itemize` |
| Layout helpers | `pinit`, `wrap-it`, `cuti` (fake bold/italic for CJK), `ctyp`/`rubby` (CJK/ruby), `linguify` (i18n strings), `valkyrie` (type validation), `tidy` (API docs), `mantys` (manuals) |
| Markdown | `cmarker` 0.1.10 (render Markdown inside Typst), `mdbook-typst`, `shiroa` (online books), pandoc (CLI) |
| Codes | `tiaoma` 0.3.0 / `codetastic` (QR/barcodes) |
| Icons | `fontawesome` 0.6.2, `use-tabler-icons`, `octique` |
| Misc | `muchpdf` (embed PDF pages, WASM; native `image` handles PDFs since 0.14), `wordometer` (word counts), `oxifmt` (Rust-like formatting), `based` (base64), `jogs` (JS in WASM), `prequery` (query + preprocessing), `nth` (ordinals), `ansi-render` |

> **Verified on 0.15.1** (see `examples/packages-demo.typ`): `cetz 0.5.3`, `fletcher 0.5.8`, `lilaq 0.6.0`, `theorion 0.6.0` (`#import cosmos.clouds: *`, `#show: show-theorion`), `codly 2.0.0`, `touying 0.8.0` (`#import themes.simple: *`; `#show: simple-theme.with(aspect-ratio: "16-9")`, `#pause`). **`codly` 2.x changed API**: `#import "@preview/codly:2.0.0" as codly`, `#show raw.where(block: true): codly.new`, `#show: codly.lang-set_(languages: codly-languages)` with `@preview/codly-languages`, `codly.set_(..)`, `codly.theme(..)`; the 1.x `#show: codly-init` / `#codly(...)` no longer exist. Packages' APIs move fast — read the README that matches the pinned version (cached copies live in the package cache dir, e.g. `~/Library/Caches/typst/packages/preview/<name>/<version>/README.md`).

## Templates (use with `typst init @preview/<name>:<ver>`)

| Kind | Packages |
| --- | --- |
| Papers | `charged-ieee` 0.1.4 (IEEE), `arkheion` 0.1.2 (arXiv-like), `clean-math-paper` 0.2.8, `unequivocal-ams` (AMS), `elsearticle` 3.1.0 (Elsevier), `clean-acmart` (ACM), `rubber-article` 0.5.2 (LaTeX-article look), Springer LNCS ports (search "lncs"), journal-specific ports (search the journal name) |
| Reports/books | `ilm` 2.1.1 (notes/non-fiction), `min-book` 1.5.1, `basic-report` 0.5.0, `bubble` 0.2.2, `scripst`, `problemst` (homework), `springer-spaniel` |
| Theses | ~260 packages: search by university (`modern-nju-thesis` etc.) or `--category thesis` |
| CV / cover letter | `modern-cv` 0.10.0, `brilliant-cv` 4.1.1, `grotesk-cv` 1.0.5, plus ~90 others (`--category cv`) |
| Posters | `peace-of-posters` 0.6.0 (`--category poster`) |
| Gantt/Timeline | `timeliney` 0.4.0, `gantty` 0.5.1 |

## Searching Universe from the CLI

```bash
python3 scripts/search-packages.py "ieee paper"              # keyword search over name/description/keywords/categories
python3 scripts/search-packages.py --category cv --top 10
python3 scripts/search-packages.py --name cetz --versions    # latest + all versions
python3 scripts/search-packages.py --list-categories
```

The index is `https://packages.typst.org/preview/index.json` (array of `{name, version, entrypoint, authors, license, description, repository, keywords, categories, disciplines, compiler, updatedAt, template?}`).

## Non-package tools

| Tool | Use |
| --- | --- |
| `tinymist` | LSP + preview + export + formatter + profiler (VS Code ext, Neovim, Helix, Emacs, Zed) |
| `typstyle` | formatter; `typstyle -i`, `--check`, `-l 80` |
| `typst-package-check` | validate before publishing to Universe |
| `tytanic` (`tt`) | test runner with reference-image comparison |
| `typship` | package publishing helper |
| `pandoc` | Markdown/LaTeX/HTML/DOCX ↔ Typst (`pandoc in.md -o out.typ`, `-t typst`; Typst as PDF engine: `--pdf-engine=typst`) |
| `typst-ts` / `typst.ts`, `typst-wasm` | run Typst in the browser/Node (JS API) |
| `typst-py` (`pip install typst`) | Python bindings: `typst.compile("main.typ", output="out.pdf", sys_inputs={...})` |
| `typst` crate (`typst-kit`) | embed Typst in Rust (0.15 reworked `typst-kit`) |
| `quarto` | Typst output format (`format: typst`) for `.qmd` documents |
| `sphinx`/`mdBook` ports | `sphinx-typst`, `mdbook-typst` for doc sets |
| `docx` bridging | `typ2docx`/pandoc for Word interchange (lossy) |
| `zathura`/`sioyek`/`Skim`/`pdfpc` | PDF viewers (auto-reload with `typst watch`); `pdfpc` for slide presenting |
| `prettypst`, `typstfmt` | older formatters (superseded by `typstyle`) |

## Language ecosystem notes

- CJK: install a CJK font; `#set text(lang: "zh", region: "cn", font: ("Libertinus Serif", "Noto Serif CJK SC"))`; `cjk-latin-spacing`; `ctyp`, `cuti`, `rubby`.
- RTL: `#set text(lang: "ar")`; direction auto from lang or `dir: rtl`; numbering systems for Arabic/Armenian/Tibetan in 0.15.
- Hyphenation covers most Latin/Cyrillic/Greek languages; set `lang` and `region`.
- Right-to-left math is not mirrored; use LTR math inside RTL text.
