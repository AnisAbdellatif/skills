# Shapes, styling, text, icons, positioning, themes

Contents: [Shape catalog](#shape-catalog) · [Style keys](#style-keys) · [Root styles](#root-styles) · [Dimensions](#dimensions) · [Text and fonts](#text-and-fonts) · [Icons and images](#icons-and-images) · [Positioning with near](#positioning-with-near) · [Themes](#themes) · [Sketch mode](#sketch-mode)

Blocks tagged `d2` compile as-is.

## Shape catalog

Set with `shape:`. The value is case-insensitive.

| shape | use for | notes |
|---|---|---|
| `rectangle` | default, generic component | |
| `square` | | forced 1:1 ratio; width and height become the larger of the two |
| `circle` | | 1:1 ratio like `square` |
| `oval` | | |
| `diamond` | decision | |
| `hexagon` | service, process | |
| `parallelogram` | input / output | |
| `cylinder` | database, persistent store | |
| `stored_data` | cache, stateful store | |
| `queue` | message queue, buffer | |
| `package` | product, module boundary | |
| `step` | pipeline step, chevron | |
| `callout` | annotation, speech bubble | |
| `page` | output, deliverable | |
| `document` | served document, config file | |
| `cloud` | external service, internet | |
| `person` | human actor | |
| `c4-person` | C4-style person (v0.7.1+) | |
| `text` | free text, no border | |
| `code` | code block | usually produced by `\|go ... \|` |
| `image` | standalone image | needs `icon:` |
| `class` | UML class | see `diagram-types.md` |
| `sql_table` | database table | see `diagram-types.md` |
| `sequence_diagram` | sequence diagram | see `diagram-types.md` |
| `hierarchy` | undocumented / experimental tree layout | cannot combine with `top`/`left`; do not rely on it |

An unknown value is a compile error (`unknown shape "banana"`).

```d2
direction: right
a: rectangle
b: {shape: hexagon}
c: {shape: cylinder}
d: {shape: queue}
e: {shape: cloud}
f: {shape: person}
g: {shape: diamond}
h: {shape: document}
a -> b -> c
d -> e
f -> g -> h
```

## Style keys

Everything lives under `style` (or `style.<key>` dotted). Values below are verified against the compiler.

| key | applies to | value |
|---|---|---|
| `opacity` | all | float 0-1 |
| `stroke` | all | CSS color name, hex (quoted), or a subset of CSS gradients; on `sql_table`/`class` it colors the body |
| `fill` | shapes | same as stroke; on `sql_table`/`class` it colors the header. `transparent` is allowed |
| `fill-pattern` | shapes | `dots`, `lines`, `grain`, `paper`, `none` |
| `stroke-width` | all | number 0-15 |
| `stroke-dash` | all | number 0-10 |
| `border-radius` | shapes and connections | number; high value (e.g. 999) = pill; on connections rounds corners (ELK) |
| `shadow` | shapes | boolean |
| `3d` | rectangle, square, hexagon only | boolean |
| `multiple` | shapes | boolean (stacked look) |
| `double-border` | rectangles and ovals | boolean |
| `font` | text | only `mono` |
| `font-size` | text | integer 8-100 |
| `font-color` | text | color; on `sql_table`/`class` header text only |
| `bold`, `italic`, `underline` | text | boolean |
| `text-transform` | text | `none`, `uppercase`, `lowercase`, `capitalize` (not `title`) |
| `animated` | connections | boolean; moving dashes; only for real runtime flow |
| `filled` | arrowheads (`target-arrowhead.style.filled`) | boolean |

Colors: names (`red`, `cornflowerblue`), hex (`"#44C7B1"`), gradients (`"linear-gradient(red, blue)"`; stops are validated; gradients in sketch mode are fragile).

```d2
direction: right
a: Primary {
  style: {
    fill: "#44C7B1"
    stroke: darkcyan
    stroke-width: 3
    border-radius: 8
    shadow: true
    font-color: white
    bold: true
  }
}
b: Stack {style.multiple: true}
c: Textured {style.fill-pattern: dots}
d: Pill {style.border-radius: 999}
e: Block {style.3d: true}
a -> b: dashed {style.stroke-dash: 3}
b -> c: animated {style.animated: true}
c -> d
d -> e
```

Class-based styling is preferred for anything repeated (see `reuse-and-globs.md`). Change defaults for a whole diagram with triple globs: `***.style.fill: lightblue`.

## Root styles

At the top level, `style.*` styles the *canvas*:

```d2
style: {
  fill: "#f5f5f5"          # background
  fill-pattern: dots
  stroke: "#333"           # frame around the diagram
  stroke-width: 2
  stroke-dash: 3
  double-border: true
}
vars: {d2-config: {pad: 40}}   # leave room for the frame
a -> b
```

## Dimensions

`width` and `height` (pixels) work on non-container shapes in every engine; on containers they need ELK or TALA (TALA may enlarge to fit children). Set both on busy shapes to give edges more surface to attach to; that fixes most cluttered-edge complaints. In grids, widths align per column and heights per row.

```d2
vars: {d2-config: {layout-engine: elk}}
hub: {
  width: 240
  height: 120
}
hub -> a
hub -> b
hub -> c
```

## Text and fonts

- Standalone block strings are Markdown text; use `shape: text` for plain text with styling (`style.font-size`, `italic`).
- Fonts: Source Sans Pro (labels), Source Code Pro (code, class text), hand-drawn pair in sketch mode. CLI flags `--font-regular/-italic/-bold/-semibold`, `--font-mono*` take `.ttf` paths; supply all or none.
- `near: top-center` plus `shape: text` makes a title:

```d2
title: A winning strategy {
  shape: text
  near: top-center
  style: {
    font-size: 40
    italic: true
  }
}
poll -> results -> decision
```

See `language.md` for block strings, Markdown, LaTeX and code.

## Icons and images

`icon:` takes a URL or, on the CLI, a local path (`./logo.png`). Icons need network access at render time (remote images are fetched and embedded; failures are reported, local missing files make the compile fail with "failed to bundle").

```d2
direction: right
deploy: {icon: https://icons.d2lang.com/aws%2FDeveloper%20Tools%2FAWS-CodeDeploy.svg}
backup: {icon: https://icons.d2lang.com/aws%2FStorage%2FAWS-Backup.svg}
deploy -> backup: {icon: https://icons.d2lang.com/infra%2F002-backup.svg}
server: {
  shape: image
  icon: https://icons.d2lang.com/tech/022-server.svg
}
```

- A **free icon library** lives at `https://icons.d2lang.com` (`aws/`, `azure/`, `gcp/`, `tech/`, `dev/`, `infra/`, `essentials/`...). URL-encode `/` inside the path as `%2F` and spaces as `%20`.
- `shape: image` makes a standalone picture (add `label: ""` if you want no caption).
- Placement is automatic (top-left for containers, centered for leaf shapes); override with `icon.near`.
- Connections can carry icons (v0.7.1+). `border-radius` applies to icons.
- Brand logos: Simple Icons (`https://cdn.jsdelivr.net/npm/simple-icons@v16/icons/<slug>.svg`) are monochrome SVGs and render well. Save one-off logos locally and reference them by relative path so the diagram works offline.
- Prefer local files in repos: relative paths are resolved against the `.d2` file's directory.

## Positioning with `near`

Layout is automatic; two mechanisms let you nudge it.

**1. Constants** (all engines). On a shape: `top-left top-center top-right center-left center-right bottom-left bottom-center bottom-right`. Typical uses: titles, legends, explanations.

```d2
title: |md
  # A winning strategy
| {near: top-center}

explanation: |md
  Notes that live outside the flow.
| {near: bottom-right}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people
```

**2. Label and icon positions.** `label.near` and `icon.near` accept the nine inside positions plus, with `outside-` and `border-` prefixes, positions outside or on the border: `outside-top-left`, `outside-top-center`, `outside-top-right`, `outside-left-top`, `outside-left-center`, `outside-left-bottom`, `outside-right-top`/`-center`/`-bottom`, `outside-bottom-left`/`-center`/`-right`, and the same set with `border-`. Note the naming order of the side variants (`outside-left-center`, not `outside-center-left`). Also `center-center`.

```d2
vars: {d2-config: {layout-engine: elk}}
env: Your environment {
  label.near: outside-bottom-center
  app: Application {
    label.near: border-top-center
    workflow
    sdk
  }
}
```

**3. Tooltips with `near`** stay permanently visible: `x.tooltip.near: center-left`.

**4. TALA-only:** `near: <absolute shape id>` to hover next to another object, and `top`/`left` (set both) to pin an object at a position while TALA arranges the rest. Other engines raise a compile error for these.

## Themes

Set with `theme-id` in `vars.d2-config` or `-t`/`--theme`. Full catalog (verified from the D2 source):

| id | name | character |
|---|---|---|
| 0 | Neutral Default | the default |
| 1 | Neutral Grey | clean, sober (docs, science, gov) |
| 3 | Flagship Terrastruct | D2's modern branded look |
| 4 | Cool Classics | blues/greys, corporate |
| 5 | Mixed Berry Blue | vibrant |
| 6 | Grape Soda | saturated purple |
| 7 | Aubergine | purple, warm |
| 8 | Colorblind Clear | accessibility-first |
| 100 | Vanilla Nitro Cola | warm |
| 101 | Orange Creamsicle | warm orange |
| 102 | Shirley Temple | pink |
| 103 | Earth Tones | earthy |
| 104 | Everglade Green | green |
| 105 | Buttered Toast | yellow-brown |
| 200 | Dark Mauve | dark |
| 201 | Dark Flagship Terrastruct | dark |
| 300 | Terminal | all caps, mono, dotted containers, double outer border |
| 301 | Terminal Grayscale | same, grayscale |
| 302 | Origami | paper-fold look |
| 303 | C4 | for C4 diagrams |

`d2 themes` lists what your binary ships. Dark themes (200, 201) can be passed as the main `theme-id` for an always-dark diagram. `dark-theme-id` instead makes the SVG switch to that theme when the *viewer's OS* is in dark mode; leave it unset unless the user asks.

Special themes (300, 301, 302) change defaults (caps, radius, font, patterns); override with `text-transform: none` and similar.

### Customizing a theme

`theme-overrides` replaces palette slots; `dark-theme-overrides` does the same for the dark variant. Quote hex values.

```d2
vars: {
  d2-config: {
    theme-id: 0
    theme-overrides: {
      B1: "#2E7D32"
      B2: "#66BB6A"
      B3: "#A5D6A7"
      B4: "#C5E1A5"
      B5: "#E6EE9C"
      B6: "#FFF59D"
      AA2: "#0D47A1"
      AA4: "#42A5F5"
      AA5: "#90CAF9"
      AB4: "#F44336"
      AB5: "#FFCDD2"
    }
  }
}
a -> b -> c
```

Slots: `N1`-`N7` neutrals (dark to light: text, strokes, backgrounds), `B1`-`B6` base/primary ramp (shape strokes and fills, containers), `AA2 AA4 AA5` accent A, `AB4 AB5` accent B. Not every theme uses every slot.

This keeps the dark pairing and theme-consistent colors intact, unlike hard-coded fills on every shape.

## Sketch mode

`--sketch` / `-s` or `vars.d2-config.sketch: true` gives a hand-drawn look. Good for whiteboard-style, informal docs; avoid for formal or compliance material. Gradients can misbehave.
