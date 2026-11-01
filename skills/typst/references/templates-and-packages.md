# Templates, packages, and project structure

## Using packages

```typ-x
#import "@preview/cetz:0.5.3": canvas, draw       // Typst Universe (downloaded + cached on first use)
#import "@preview/codly:2.0.0": *
#import "@local/myutils:0.1.0": helper             // local package, see below
```

- Always pin an exact version. Find current versions: `python3 scripts/search-packages.py <keywords>` (uses `https://packages.typst.org/preview/index.json`) or <https://typst.app/universe>.
- Packages declare a minimum compiler (`compiler = "0.12.0"` in `typst.toml`); a very new compiler can break old packages (removed APIs like `path`, `pattern`, `*.decode`). If an import fails to compile, try a newer package version or check its issue tracker.
- Import specific names (`: draw`) or the module (`#import "@preview/x:1.0.0"` → `x.f`). Rename with `as`.
- Many packages are **show-rule based**: `#show: codly-init` / `#show: theorems-init`, then call their functions. Read the package README.
- Offline: see `export-and-cli.md` (cache path); vendor packages by copying to `@local`.

## Writing a template function

A template is just a function whose last positional param is the document body, applied with `#show: tpl.with(...)`.

```typ
#let article(
  title: none,
  authors: (),
  abstract: none,
  paper: "a4",
  lang: "en",
  body,
) = {
  set document(title: title, author: authors.map(a => a.name))
  set page(paper: paper, margin: (x: 2.2cm, y: 2.5cm), numbering: "1",
    header: context if counter(page).get().first() > 1 { align(right, text(8pt, gray, title)) })
  set text(font: "New Computer Modern", size: 11pt, lang: lang)
  set par(justify: true, leading: 0.62em)
  set heading(numbering: "1.1")
  show heading: set block(above: 1.4em, below: 0.8em)
  show heading.where(level: 1): set text(13pt)

  align(center)[
    #text(17pt, weight: "bold", title) \
    #v(0.6em)
    #authors.map(a => [#a.name #super(a.affiliation)]).join(", ")
  ]
  if abstract != none {
    pad(x: 2em, y: 1em)[*Abstract.* #abstract]
  }
  body
}

#show: article.with(
  title: "A Sample Paper",
  authors: ((name: "Ada Lovelace", affiliation: "1"),),
  abstract: [We show templates are functions.],
)

= Introduction
#lorem(60)
```

Template best practices:
- Defaults for every optional argument; `lang` configurable; no content leaks if parameters are `none`.
- Take structured metadata (`authors: ((name:, email:, affiliation:), ...)`) rather than preformatted content when you need to reuse values (PDF metadata, headers).
- `#show: tpl.with(...)` has to come **before** content and be at top level of the file.
- Prefer show-set rules; scope everything inside the function.
- Separate concerns across files: `template.typ` (exports `article`), `main.typ` (`#import "template.typ": article`), `refs.bib`.
- Provide a variant for `html` target via `context target()` if you need it.
- Document parameters with `///` comments (tidy format).

### Multi-file project layout

```
thesis/
├── main.typ            // #import "template.typ": thesis ; #show: thesis.with(...) ; #include "chapters/intro.typ" ...
├── template.typ
├── refs.bib
├── chapters/
│   ├── intro.typ       // starts with plain content; may `#import "../template.typ": *` for helpers
│   └── methods.typ
├── figures/
└── fonts/              // optional; compile with --font-path fonts
```

Included files cannot see variables of the includer; share helpers through a module (`lib.typ`) imported where needed. Set `heading.offset` or use `= ` levels consistently per chapter: `#set heading(offset: 1)` in an `include`d appendix.

## Making a package

```
my-pkg/
├── typst.toml
├── lib.typ          // entrypoint; re-export the public API
├── src/…
├── template/        // optional: files copied by `typst init` for a template package
│   ├── main.typ
│   └── refs.bib
├── thumbnail.png    // for templates (≥ 1080 px side, ≤ 3 MB)
├── README.md
├── LICENSE
└── docs/ tests/     // excluded from publication via `exclude`
```

`typst.toml`:

```toml
[package]
name = "my-pkg"                 # lowercase, digits, hyphens
version = "0.1.0"               # semver
entrypoint = "lib.typ"
authors = ["Name <name@example.com>", "GitHubUser"]
license = "MIT"                 # SPDX; OSI-approved for Universe
description = "One sentence, no trailing period, don't repeat the name."
repository = "https://github.com/user/my-pkg"
homepage = "https://..."
keywords = ["thesis", "template"]
categories = ["thesis"]         # see below
disciplines = ["computer-science"]
compiler = "0.12.0"             # minimum Typst version
exclude = ["tests/*", "docs/*", "*.pdf"]

[template]                      # only for template packages
path = "template"               # directory copied by `typst init`
entrypoint = "main.typ"         # file to compile inside it
thumbnail = "thumbnail.png"
```

- Categories — document types: `book report paper thesis poster flyer presentation cv office`; function types: `components visualization model layout text scripting integration utility fun languages`.
- A template's `main.typ` should import the package by its **published name** (`#import "@preview/my-pkg:0.1.0": my-template`) and call `#show: my-template.with(...)`; `typst init` rewrites/uses that.
- Inside a package: relative paths and `/…` resolve **within the package**; the user's project files are not visible. Accept file *content/bytes/typed `path`* arguments from users (`path` type, 0.15) when data must come from their project. `read`/`image` inside a package read package files only.
- Public API discipline: `lib.typ` re-exports with `#import "src/x.typ": f, g`; keep the rest internal. No circular imports.
- Local testing: copy/symlink to `…/typst/packages/local/my-pkg/0.1.0/` and import `@local/my-pkg:0.1.0` (or compile with `--package-path ./pkgs`). Try `typst init @local/my-pkg:0.1.0 demo`.
- Quality tooling: `typst-package-check` (official Universe validator), `typstyle` (format), `tytanic` (`tt`, visual regression tests with reference PNGs), `tidy` (docs from `///` comments).
- Publish: fork <https://github.com/typst/packages>, add `packages/preview/my-pkg/0.1.0/…`, open a PR (names must be unique; follow naming/licensing guidelines in the repo's `docs/`). Versions are immutable.

## Typst Universe etiquette for users

- Check license and maintenance activity before depending on a package (last update, open issues, compatible compiler).
- Prefer official/community-standard packages for foundations (cetz, fletcher, touying/polylux, codly/zebraw, glossarium, lilaq, tidy, hydra, theorion/ctheorems, physica, mitex, i-figured, subpar, showybox, gentle-clues).
- Lock versions in the project; update deliberately (the API of 0.x packages changes often).

## Tooling

- **tinymist**: language server (completion, diagnostics, formatting, live preview, export, tracing) for VS Code/Neovim/Helix/Emacs/Zed; VS Code ext "Tinymist Typst". Preview: `tinymist preview main.typ`.
- **typstyle**: formatter (`typstyle -i file.typ`, `--check`, `--diff`, `-l` line width); **typst-package-check**; **tytanic** tests; **typship** (publish helper); **typ2docx/pandoc** for conversion (see `migration.md`).
- **typst.app**: collaborative web editor (limited fonts, no HTML/bundle export).
- Zed/Neovim/Helix: tree-sitter grammar `tree-sitter-typst`.
- Pre-commit: `typstyle --check`, `typst compile` smoke tests.
