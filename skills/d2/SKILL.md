---
name: d2
description: Write, edit, debug, style and render diagrams in D2 (d2lang.com), the text-to-diagram language. Use this skill whenever the user wants a diagram, flowchart, architecture / system / network / cloud diagram, sequence diagram, ER diagram or database schema, UML class diagram, C4 model, state machine, org chart, grid / table / matrix layout, or any "draw / visualize / map out / sketch" request for software or process structure, and whenever they mention D2, d2lang, .d2 files or the `d2` CLI. Also use it to fix D2 compile errors, restyle or theme a D2 diagram, build multi-board diagrams (layers, scenarios, steps), convert Mermaid / PlantUML / Graphviz to D2, or export to SVG, PNG, PDF, GIF, PPTX or ASCII. Prefer D2 over ad-hoc ASCII art or hand-written SVG for any diagram the user may want to keep, edit or render.
---

# D2 diagrams

D2 is a declarative language: you describe shapes and the connections between them, and a layout engine decides where everything goes. You never place coordinates by hand. That is why a D2 diagram is short, diffable and easy to edit later, and also why most errors come from *syntax and layout-engine quirks*, not from design.

This skill is a complete working knowledge of D2 v0.9.x, verified against the real compiler. Every example in `references/` and `assets/templates/` compiles.

## Workflow

1. **Check the tool.** Run `d2 --version` (or `scripts/d2check.sh --version`). If `d2` is missing, tell the user and offer `brew install d2` or `curl -fsSL https://d2lang.com/install.sh | sh -s --`; do not install silently.
2. **Choose the diagram type** and read the matching reference (table below). Start from a template in `assets/templates/` when one fits.
3. **Write the `.d2` file** next to where the user wants it (default: `diagrams/<name>.d2`).
4. **Compile and render with `scripts/d2check.sh <file.d2> [outdir] [pdf|pptx|gif]`** (formats, compiles, renders SVG, puts a PNG preview in `outdir/preview/`, and any extra formats). Never rely on `d2 validate` alone: it only parses syntax. Bad shape names, out-of-range styles, unsupported layout features and missing imports all pass `validate` and fail at compile.
5. **Look at the picture.** Open the PNG in `preview/` (Read tool on the `.png`) and judge it: overlapping labels, tangled edges, wrong flow direction, a lopsided layout. Fix and re-render. A diagram that compiles but is unreadable is not done.
6. **Deliver** the `.d2` source plus the rendered file, and say which layout engine, theme and direction you used so the user can change them.

For a quick one-off with no files: `echo 'a -> b' | d2 - out.svg`.

## Syntax in one screen

```d2
direction: right                    # up | down | right | left (root-level; only TALA allows per-container)

# shapes: key, optional label, optional attributes
web: Web App {shape: rectangle}     # key `web`, label "Web App"
db: Postgres {shape: cylinder}
user: Customer {shape: person}

# connections: -> <- <-> --  (always reference KEYS, never labels)
user -> web: uses
web -> db: SQL {style.stroke-dash: 3}
web -> cache: reads              # undeclared keys are created on the fly

# containers: dots or nested maps
backend: {
  api -> worker: enqueue
  worker -> _.db: writes         # _ = parent scope
}
web -> backend.api: HTTPS

# styling lives in attributes
db.style.fill: "#e6f2ff"         # quote anything starting with #
(web -> db)[0].style.stroke: red # style a connection by index

# reuse: classes, variables, globs
classes: {
  store: {shape: cylinder; style.fill: "#e6f2ff"}
}
cache.class: store
vars: {env: prod}
note: Running in ${env}
*.style.border-radius: 8
```

Semicolons separate items on one line. `#` starts a comment, `""" ... """` is a block comment. Keys are case-insensitive and repeated declarations merge (`API`, `api` and `Api: Gateway` are one shape labeled "Gateway").

## Quoting: the number-one source of errors

Unquoted strings are convenient, but several characters have meaning. Quote the *whole* label (`"..."` or `'...'`) whenever it contains any of these, or the compiler either errors or, worse, silently truncates the label:

| Character | What happens unquoted | Example fix |
|---|---|---|
| `#` anywhere | rest of line becomes a comment: `a: C# language` renders "C" | `a: "C# language"` |
| `[` at the start | parsed as an array: `a: [JSON/HTTPS]` renders just "a" | `a: "[JSON/HTTPS]"` |
| `.` in a **key** | creates a container: `svc v1.2` becomes `svc v1` > `2` | `"svc v1.2"` |
| `&` or `[ ]` in a **key** | parse error (`&` is the glob filter marker) | `"R&D"`, `"svc[0]"` |
| `$` followed by anything but `{` | "substitutions must begin on {" | single quotes: `'costs $5'` |
| `{ }` `|` at label start | opens a map or block string | quote it |
| reserved words as shape keys (`label`, `link`, `class`, `top`, `style`, `shape`, `icon`, `near`, `direction`, `vars` ...) | "reserved keywords are prohibited in edges" | `"link" -> b`, or pick a different key |
| `->` or `:` inside an **edge label** | fine in practice (`a -> b: Time: 10s` works) | no quoting needed |
| non-ASCII punctuation such as `：` (full-width colon) | not recognised as a colon | use ASCII `:` `;` `.` |

Hex colors must be quoted (`"#fff"`) because `#` starts a comment. Single quotes also disable `${...}` substitution.

Newlines in labels: `\n` in a quoted or unquoted label, or a block string `|md ... |` for rich text.

## Things that bite (read before debugging)

- **Dagre, the default layout engine, cannot draw a connection between a container and its own descendant** (`a -> a.b`), cannot size containers (`width`/`height`), and cannot use `near: <object>`. It errors at compile time. Switch to `--layout=elk` (or `vars.d2-config.layout-engine: elk`) instead of rewriting the diagram.
- **Reserved words are matched case-insensitively.** A shape or UML class named `Shape`, `Label`, `Class`, `Style`, `Link`, `Icon`... collides with the keyword (`reserved field shape does not accept composite`). Rename it.
- **Connect keys, not labels.** After `be: Backend`, `Backend -> x` makes a *new* shape named Backend. Use `be -> x`.
- **Repeated connections do not merge**; `a -> b` twice draws two arrows. Address them as `(a -> b)[0]`, `(a -> b)[1]`.
- **`d2-legend` is a variable**, not a shape: put it inside `vars: { d2-legend: { ... } }`. A top-level `d2-legend: ""` is just an ordinary shape named "d2-legend".
- **Sequence diagrams**: order of declaration is order on screen, actors should be declared first, and inside groups you can only reference actors that exist at the top level.
- **SQL tables and UML classes**: connect *rows* (`orders.user_id -> users.id`), and use ELK or TALA so edges land on the exact row.
- **Arrowhead shapes only render on an end that has an arrow**: `A -> B` with `source-arrowhead.shape: diamond` draws nothing at A (and `--` draws no shapes at all). Flip the edge so the shape is on the target, or use `<->`.
- **`d2 fmt` rewrites reserved-word labels** (`lnk: Link` becomes `lnk: link`), and `scripts/d2check.sh` runs fmt on your file in place. Quote such labels (`lnk: "Link"`).
- **Block strings** `|md ... |` end at the next `|`. A literal pipe inside needs a longer delimiter: `|`md ... `|` or `||md ... ||`.
- **Numeric style ranges are enforced**: `stroke-width` 0-15, `opacity` 0-1, `font-size` 8-100. `text-transform` takes `none|uppercase|lowercase|capitalize` (the website says `title`; the compiler rejects it). `3d` works only on rectangle, square and hexagon.
- **Don't add `animated: true` or `dark-theme-id` unless asked.** Animation implies runtime data flow; a dark theme silently flips colors for viewers whose OS is in dark mode.
- **Fill colors on shapes override the theme.** Prefer the theme and a few `classes`; use explicit colors only when color carries meaning (and then add a legend).
- **PNG/PDF/PPTX/GIF render without a browser in v0.9+.** Older versions (<0.8) need Playwright/Chromium, which downloads on first use. Check `d2 --version`.
- **TALA** is bundled in v0.9 (`--layout=tala`) but non-deterministic: a tiny label change can reshuffle the layout. Pin it with `data.tala-seeds` if reproducibility matters.
- **Multi-board files (`layers`/`scenarios`/`steps`) export SVG and PNG as *directories*** (`x/index.svg`, `x/layers/a.svg`), and rendering PNG to the same name replaces the SVG directory. Keep formats in separate folders (the script does). For a drill-down deliverable use **PDF** (one page per board, clickable `link: layers.x`) and do not hand-draw "Back" shapes: the exporter adds a breadcrumb bar automatically. See `references/composition.md`.
- **Output file existing does not mean success.** D2 may write a partial render on error. Check the exit code (the script does).

## Choosing layout, direction, theme

- **Layout engine**: `dagre` (default, fast, curvy edges) -> `elk` (orthogonal routing, best for architecture, SQL tables, container-to-container edges) -> `tala` (symmetry, per-container `direction`, `near: object`, locked `top`/`left`). Default to **ELK** for anything with containers or tables.
- **Direction**: `right` for pipelines, request flows and wide screens; `down` for hierarchies and org charts. Pick one for the whole board.
- **Theme**: `theme-id: 0` default; `4` Cool classics and `3` Flagship Terrastruct look modern; `1` neutral grey for sober docs; `8` is colorblind-safe; `300`/`301` terminal; `303` C4; `200`/`201` dark. Full table in `references/cli-and-rendering.md`.
- Put render settings in the file so they travel with it:

```d2
vars: {
  d2-config: {
    layout-engine: elk
    theme-id: 4
    pad: 40
  }
}
```

(CLI flags and `D2_*` env vars override this block.)

## Design guidance

- **3 to 12 shapes per board.** Past that, split with `layers` (zoom in), `scenarios` (variants) or `steps` (build-up), or use containers to group.
- **Name by key, label for humans**: short stable keys (`pg`, `auth`), readable labels (`pg: PostgreSQL`).
- **Edge labels are verbs or protocols** (`reads`, `publishes`, `HTTPS`), not sentences and not the target's name.
- **Match shape to meaning**: `cylinder` store, `queue`, `person`, `cloud` external, `diamond` decision, `hexagon` service, `document`/`page`, `package`, `step`. Don't leave everything a rectangle.
- **Color encodes meaning or nothing.** At most ~5 categories, applied through `classes`, with a `d2-legend` only when the colors carry information the labels don't.
- **One abstraction level per board.**
- D2 is for documenting software and systems at whiteboard scale (up to a few hundred shapes). It deliberately has no Gantt charts, mind maps, Venn diagrams, Sankey, pie/bar charts or geographic maps, and an object cannot live in two containers. Say so and suggest another tool rather than contorting D2.

## Reference map

Read only what the task needs.

| Task | Read |
|---|---|
| Any syntax doubt: keys, labels, connections, containers, strings, escaping, comments, reserved keywords | `references/language.md` |
| Shapes, every style key and its range, arrowheads, text/markdown/LaTeX/code, icons, `near` positioning, sizes, themes | `references/shapes-and-styling.md` |
| Sequence diagrams, SQL tables (ERD), UML classes, grids, legends, tooltips/links, C4 | `references/diagram-types.md` |
| Classes, variables, globs and filters, overrides and `null`, imports, `suspend` models | `references/reuse-and-globs.md` |
| Layers, scenarios, steps, linking boards, imports for large diagrams, multi-board export | `references/composition.md` |
| CLI flags, layout engines, themes table, export formats, `d2-config`, embedding in docs/CI, D2.js | `references/cli-and-rendering.md` |
| Ready-made patterns per diagram family (architecture, flowchart, state, ERD, C4, org chart...) | `references/recipes.md` + `assets/templates/*.d2` |
| Converting from Mermaid / PlantUML / Graphviz | `references/recipes.md` (conversion section) |
| An error message or a diagram that renders wrong | `references/troubleshooting.md` |

## When the compile fails

Run `scripts/d2check.sh file.d2`. Errors come as `file:LINE:COL: message`. Look the message up in `references/troubleshooting.md`; the usual culprits are quoting (above), a layout-engine limit (switch to ELK), an unknown shape or out-of-range style, and indentation of block strings. Fix one error at a time and re-run: later errors are often consequences of the first.
